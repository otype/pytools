# -*- coding: utf-8 -*-
"""

    pydeployr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
from __future__ import absolute_import
import logging
from celery import Celery
from kombu.entity import Queue
from pytools.pybalancr.loadbalance_update_repository import loadbalance_update_api, loadbalance_remove_api
from pytools.pydeployr.config_loader import ConfigLoader
from pytools.pydeployr.returncodes import RETURNCODE
from pytools.pydeployr.messages.loadbalance_remove_confirmation_message import LoadbalanceRemoveConfirmationMessage
from pytools.pydeployr.messages.loadbalance_update_confirmation_message import LoadbalanceUpdateConfirmationMessage
from pytools.pydeployr.services import config_service

config = ConfigLoader(config=config_service.load_configuration())
broker_address = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config.rmq_broker_username,
    password=config.rmq_broker_password,
    host=config.rmq_broker_host,
    port=config.rmq_broker_port
)

celery = Celery(
    'pytools.pybalancr.balancr_tasks',
    broker=broker_address,
    backend=broker_address,
    include=['pytools.pybalancr.balancr_tasks']
)
celery.conf.update(
    CELERY_DEFAULT_QUEUE='balancr.default',
    CELERY_DEFAULT_EXCHANGE='balancr.tasks',
    CELERY_QUEUES=(
        Queue('balancr.deploy', routing_key='deploy.#'),
        Queue('balancr.undeploy', routing_key='undeploy.#'),
    ),
    CELERY_DEFAULT_EXCHANGE_TYPE='topic',
    CELERY_TASK_RESULT_EXPIRES=300,
    CELERY_TIMEZONE='Europe/Berlin',
    CELERY_WORKER_DIRECT='true',
)

#########################################################################
#
# TASKS
#
#########################################################################


@celery.task
def undeploy(undeploy_task):
    """
        UNDEPLOY an API
    """
    logging.info('Using Rabbitmq host:{} on port:{}'.format(config.rmq_broker_host, config.rmq_broker_port))
    logging.info("Processing task: {}".format(undeploy_task))

    status = loadbalance_remove_api(api_id=undeploy_task['api_id'])
    if status == RETURNCODE.OS_ERROR:
        return {
            'error': 'Removing API:{} from loadbalancer failed. '
                     'Ask administrator for help.'.format(undeploy_task['api_id'])
        }

    return LoadbalanceRemoveConfirmationMessage(api_id=undeploy_task['api_id'])


@celery.task
def deploy(deploy_task):
    """
        DEPLOY an API
    """
    logging.info('Using Rabbitmq host:{} on port:{}'.format(config.rmq_broker_host, config.rmq_broker_port))
    logging.info("Processing task: {}".format(deploy_task))

    status = loadbalance_update_api(
        api_id=deploy_task['api_id'],
        api_host=deploy_task['api_host'],
        api_port=deploy_task['api_port']
    )
    if status == RETURNCODE.OS_ERROR:
        return {'error': 'Loadbalance update failed.'}

    return LoadbalanceUpdateConfirmationMessage(
        api_id=deploy_task['api_id'],
        lb_host=config.loadbalancer_api_base_name,
        lb_api_port=80,
        api_domainname='{}.{}'.format(deploy_task['api_id'], config.loadbalancer_api_base_name)
    )

#########################################################################
#
# MAIN
#
#########################################################################

if __name__ == '__main__':
    celery.start()
