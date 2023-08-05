from __future__ import absolute_import

from datetime import datetime

import jenkins
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

logger = get_task_logger(__name__)

JENKINS_CLIENT = None


def _get_jenkins_client(jenkins_config):
    global JENKINS_CLIENT
    if JENKINS_CLIENT is None:
        JENKINS_CLIENT = jenkins.Jenkins(jenkins_config.jenkins_api,
                                 username=jenkins_config.jenkins_user,
                                 password=jenkins_config.jenkins_pass)
    return JENKINS_CLIENT

def get_job_status(jenkins_config, jobname):
    ret = {
        'active': None,
        'succeeded': None,
        'job_number': None,
        'blocked_build_time': None,
    }
    client = _get_jenkins_client(jenkins_config)
    try:
        job = client.get_job_info(jobname)
        last_build = client.get_build_info(jobname, job['lastCompletedBuild']['number'])

        ret['status_code'] = 200
        ret['job_number'] = last_build['number']
        ret['active'] = job['color'] != 'disabled'
        ret['succeeded'] = ret['active'] and last_build['result'] == 'SUCCESS'

        if job['inQueue']:
            in_queued_since = job['queueItem']['inQueueSince']
            time_blocked_since = datetime.utcfromtimestamp(
                float(in_queued_since) / 1000).replace(tzinfo=timezone.utc)
            ret['blocked_build_time'] = (timezone.now() - time_blocked_since).total_seconds()
            ret['queued_job_number'] = job['lastBuild']['number']
        return ret
    except jenkins.NotFoundException:
        ret['status_code'] = 404
        return ret
