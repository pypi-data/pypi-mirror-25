# -*- coding: utf-8 -*-
import copy
import logging
from time import sleep
from celery import shared_task
from notification.models import TaskHistory
from simple_audit.models import AuditRequest
from dbaas_aclapi import helpers
from dbaas_aclapi.acl_base_client import get_acl_client
from dbaas_aclapi.models import (ERROR, DatabaseBind, DatabaseInfraInstanceBind)
import util
import exceptions


logging.basicConfig()
LOG = logging.getLogger("AclTask")
LOG.setLevel(logging.DEBUG)


@shared_task(bind=True)
def bind_address_on_database(
    self, database_bind, user=None, retries=1, exponential_factor=2,
    time_factor_in_seconds=60
):
    user = helpers.get_user(self.request, user, "permit")

    AuditRequest.new_request("create_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.databaseinfra
    bind_info = (None, None)

    task_history.update_details(
        persist=True, details="Creating binds for {}.".format(
            database_bind
        )
    )

    try:
        acl_client = get_acl_client(database.environment)

        for attempt in (i**exponential_factor for i in range(0, retries)):
            sleep(attempt * time_factor_in_seconds)

            operation_completed, bind_info = helpers.bind_address(
                database_bind, acl_client,
                instance_bind_list=bind_info[0], bind_data=bind_info[1]
            )
            if operation_completed:
                task_history.update_status_for(
                    TaskHistory.STATUS_SUCCESS,
                    details='Bind succesfully created'
                )
                return True

        raise exceptions.MAXIMUM_RETRIES_EXCEPTION

    except Exception as e:
        error_message = "Database bind ERROR: {}".format(e)
        LOG.info(error_message)

        task_history.update_status_for(
            TaskHistory.STATUS_ERROR,
            details='Bind could not be created. ' + error_message
        )

        DatabaseBind.objects.filter(
            id=database_bind.id
        ).delete()

        DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=databaseinfra,
            bind_address=database_bind.bind_address,
        ).delete()

        return False
    finally:
        AuditRequest.cleanup_request()


@shared_task(bind=True)
def unbind_address_on_database(self, database_bind, user=None):
    action = "permit"
    user = helpers.get_user(self.request, user, action)

    AuditRequest.new_request("destroy_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.infra

    try:
        acl_client = get_acl_client(database.environment)
        task_history.update_details(
            persist=True,
            details="Removing binds for {} from {}".format(
                database_bind, database_bind.database
            )
        )

        infra_instances_binds = DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=databaseinfra, bind_address=database_bind.bind_address
        )

        if helpers.unbind_address(
                database_bind, acl_client, infra_instances_binds, True
        ):
            task_history.update_status_for(
                TaskHistory.STATUS_SUCCESS,
                details='Bind succesfully destroyed'
            )
            return True
    except Exception as e:
        LOG.info("Database unbind ERROR: {}".format(e))
        task_history.update_status_for(
            TaskHistory.STATUS_ERROR,
            details='Bind could not be removed'
        )
        return False
    finally:
        AuditRequest.cleanup_request()


@shared_task(bind=True)
def monitor_aclapi_jobs(self,):
    from dbaas_aclapi.models import (
        AclApiJob, ERROR, PENDING, RUNNING, JOB_STATUS
    )

    user = helpers.get_user(action='monitor job')

    AuditRequest.new_request("monitor_aclapi_jobs", user, "localhost")
    task_history = register_task(self.request, user)

    try:
        task_history.update_details(
            persist=True, details="Monitoring binds..."
        )

        for job in AclApiJob.objects.filter(
            job_status__in=[PENDING, RUNNING, ERROR]
        ):
            acl_client = get_acl_client(job.environment)

            try:
                response = acl_client.get_job(job_id=job.job_id)
            except Exception as e:
                LOG.warn(e)

            if 'jobs' in response:
                status = response["jobs"]["status"]
                if status in ["PENDING", "ERROR"]:
                    try:
                        response = acl_client.run_job(job_id=job.job_id)
                    except Exception as e:
                        LOG.warn(e)

                job_status = util.get_description_from_tupple(JOB_STATUS, status)
                job.job_status = job_status
                job.save(update_fields=['job_status', 'updated_at'])

        task_history.update_status_for(
            TaskHistory.STATUS_SUCCESS, details='Monitoring finished')
    except Exception as e:
        LOG.info("Database unbind ERROR: {}".format(e))
        task_history.update_status_for(
            TaskHistory.STATUS_ERROR,
            details='Erro while monitoring Jobs: {}'.format(e)
        )
    finally:
        AuditRequest.cleanup_request()


def replicate_acl_for(database, old_ip, new_ip):
    acl_client = get_acl_client(database.environment)
    for rule in helpers.iter_on_acl_rules(acl_client, {"destination": old_ip}):
        try:
            copy_acl_rule(rule, new_ip, acl_client, database)
            LOG.info("Rule copied: {}".format(rule))
        except Exception as e:
            LOG.warn("Rule could not be copied: {}. {}".format(rule, e))


def destroy_acl_for(database, ip):
    from dbaas_aclapi.models import UNBIND
    acl_client = get_acl_client(database.environment)
    job_list = []

    for environment_id, vlan_id, rule_id in helpers.iter_on_acl_query_results(
        acl_client, {"destination": ip}
    ):
        try:
            response = acl_client.delete_acl(environment_id, vlan_id, rule_id)
        except Exception as e:
            LOG.warn("Rule could not be deleted! {}".format(e))
        else:
            if 'job' in response:
                job_list.append(response['job'])

    helpers.save_jobs(job_list, UNBIND, database)


def copy_acl_rule(rule, new_ip, acl_client, database):
    from dbaas_aclapi.models import BIND

    data = {"kind": "object#acl", "rules": []}
    new_rule = copy.deepcopy(rule)
    new_rule['destination'] = '{}/32'.format(new_ip)
    data['rules'].append(new_rule)
    acl_environment, vlan = new_rule['source'].split('/')

    response = acl_client.grant_acl_for(
        environment=acl_environment, vlan=vlan, payload=data
    )

    helpers.save_jobs(response.get('jobs', []), BIND, database)


def register_task(request, user):
    LOG.info(
        "id: {} | task: {} | kwargs: {} | args: {}".format(
            request.id,
            request.task,
            request.kwargs,
            str(request.args)
        )
    )

    task_history = TaskHistory.register(
        request=request, user=user,
        worker_name=get_worker_name()
    )
    task_history.update_details(persist=True, details="Loading Process...")

    return task_history


def get_worker_name():
    from billiard import current_process
    p = current_process()
    return p.initargs[1].split('@')[1]
