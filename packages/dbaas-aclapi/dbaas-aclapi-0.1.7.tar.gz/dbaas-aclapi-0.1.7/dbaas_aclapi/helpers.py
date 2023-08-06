# -*- coding: utf-8 -*-
import logging
import copy
from acl_base_client import get_credential

logging.basicConfig()
LOG = logging.getLogger("AclHelpers")
LOG.setLevel(logging.DEBUG)

PERMIT = "permit"


def build_data_default_options_dict(
    action, bind_address, database_name, database_environment
):
    description = "{} {} access for database {} in {}".format(
        action, bind_address, database_name, database_environment
    )

    data = {"kind": "object#acl", "rules": []}
    dafault_options = {"protocol": "tcp",
                       "source": "",
                       "destination": "",
                       "description": description,
                       "action": action,
                       "l4-options": {"dest-port-start": "",
                                      "dest-port-op": "eq"}
                       }
    LOG.info("Default options: {}".format(dafault_options))
    return data, dafault_options


def iter_on_acl_query_results(acl_client, rule):
    query_results = acl_client.query_acls(rule)
    for environment in query_results.get('envs', []):
        for vlan in environment.get('vlans', []):
            environment_id = vlan['environment']
            vlan_id = vlan['num_vlan']
            for rule in vlan.get('rules', []):
                rule_id = rule['id']
                yield environment_id, vlan_id, rule_id


def save_jobs(job_list, job_operation, database):
    from dbaas_aclapi.models import AclApiJob, PENDING
    for job in job_list:
        aclapi_job = AclApiJob(
            job_id=job, job_status=PENDING, job_operation=job_operation,
            database=database, environment=database.environment
        )
        try:
            aclapi_job.save()
        except Exception as e:
            LOG.warn(e)


def run_jobs(job_list, acl_client, database):
    credential = get_credential(database.environment)
    if credential.get_parameter_by_name('execute_job') != 'True':
        return

    for job in job_list:
        acl_client.run_job(job)


def get_user(request=None, user=None, action=None):
    from account.models import User
    if not user:
        try:
            user = request.args[-1]
        except AttributeError:
            user = User.objects.get(username='admin')

    LOG.info("User: {}, action: {}".format(user, action))
    return user


def add_instance_bind(
    default_options, databaseinfra, database_bind, instance_address,
    instance_port
):
    from dbaas_aclapi.models import DatabaseInfraInstanceBind

    custom_options = copy.deepcopy(default_options)
    custom_options['source'] = database_bind.bind_address
    custom_options['destination'] = instance_address + '/32'
    custom_options['l4-options']['dest-port-start'] = instance_port

    LOG.debug("Creating bind for instance: {}".format(instance_address))

    instance_bind = DatabaseInfraInstanceBind(
        instance=instance_address, databaseinfra=databaseinfra,
        bind_address=database_bind.bind_address, instance_port=instance_port
    )
    LOG.debug("InstanceBind: {}".format(instance_bind))

    return custom_options, instance_bind


def build_new_binds(
    default_options, database_bind, databaseinfra, instances,
    infra_attr_instances, infra_vips
):
    from dbaas_cloudstack.models import DatabaseInfraAttr

    if instances is None:
        instances = databaseinfra.instances.all()

    port = instances[0].port

    for instance in instances:
        custom_options, instance_bind = add_instance_bind(
            default_options, databaseinfra, database_bind,
            instance_address=instance.address, instance_port=instance.port
        )
        yield custom_options, instance_bind

    if infra_attr_instances is None:
        infra_attr_instances = DatabaseInfraAttr.objects.filter(
            databaseinfra=databaseinfra
        )

    for instance in infra_attr_instances:
        custom_options, instance_bind = add_instance_bind(
            default_options, databaseinfra, database_bind,
            instance_address=instance.ip, instance_port=port
        )
        yield custom_options, instance_bind

    if infra_vips is None:
        infra_vips = databaseinfra.vip_databaseinfra.all()

    for infra_vip in infra_vips:
        custom_options, instance_bind = add_instance_bind(
            default_options, databaseinfra, database_bind,
            instance_address=infra_vip.vip_ip,
            instance_port=port
        )
        yield custom_options, instance_bind


def bind_address(
    database_bind, acl_client, instances=None, infra_attr_instances=None,
    instance_bind_list=None, bind_data=None, infra_vips=None
):
    from dbaas_aclapi import models

    database = database_bind.database
    databaseinfra = database.databaseinfra
    acl_environment, acl_vlan = get_bind_env_and_vlan(database_bind)

    if instance_bind_list is None:
        instance_bind_list = []
        bind_data, default_options = build_data_default_options_dict(
            PERMIT, database_bind.bind_address, database.name,
            database.environment.name
        )

        for custom_option, instance_bind in build_new_binds(
            default_options, database_bind, databaseinfra, instances,
            infra_attr_instances, infra_vips
        ):
            bind_data['rules'].append(custom_option)
            instance_bind_list.append(instance_bind)

    try:
        response = acl_client.grant_acl_for(
            environment=acl_environment, vlan=acl_vlan, payload=bind_data
        )
    except Exception as e:
        return False, (instance_bind_list, bind_data)

    if 'jobs' in response:
        save_jobs(response['jobs'], models.BIND, database)

        run_jobs(response['jobs'], acl_client, database)

        for instance_bind in instance_bind_list:
            try:
                instance_bind.save()
            except Exception as e:
                LOG.warn(e)

        models.DatabaseBind.objects.filter(
            id=database_bind.id
        ).update(bind_status=models.CREATED)

        models.DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=database.databaseinfra,
            bind_address=database_bind.bind_address
        ).update(bind_status=models.CREATED)

        return True, (True, True)
    else:
        return False, (instance_bind_list, bind_data)


def unbind_address(
    database_bind, acl_client, infra_instances_binds,
    delete_database_bind=True
):
    from dbaas_aclapi.models import UNBIND

    database = database_bind.database
    _, default_options = build_data_default_options_dict(
        PERMIT, database_bind.bind_address, database.name,
        database.environment.name)

    job_list = []
    for infra_instance_bind in infra_instances_binds:
        custom_options = copy.deepcopy(default_options)
        custom_options['source'] = database_bind.bind_address
        custom_options['destination'] = infra_instance_bind.instance + '/32'
        custom_options['l4-options']['dest-port-start'] = infra_instance_bind.instance_port

        for environment_id, vlan_id, rule_id in iter_on_acl_query_results(
            acl_client, custom_options
        ):
            try:
                response = acl_client.delete_acl(
                    environment_id, vlan_id, rule_id
                )
            except Exception as e:
                LOG.info(
                    "Access {} could not be deleted! Error: {}".format(
                        infra_instance_bind, e
                    )
                )
            else:
                if 'job' in response:
                    job_list.append(response['job'])

        infra_instance_bind.delete()
    save_jobs(job_list, UNBIND, database)

    if delete_database_bind:
        database_bind.delete()
    return True


def get_bind_env_and_vlan(database_bind):
    return database_bind.bind_address.split('/')


def iter_on_acl_rules(acl_client, rule):
    query_results = acl_client.query_acls(rule)
    for environment in query_results.get('envs', []):
        for vlan in environment.get('vlans', []):
            for rule in vlan.get('rules', []):
                yield rule
