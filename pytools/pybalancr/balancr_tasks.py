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
from pybalancr.repositories.loadbalance_update_repository import loadbalance_update_api
from pydeployr.conf.config_loader import ConfigLoader
from pydeployr.conf.returncodes import RETURNCODE
from pydeployr.messages.loadbalance_update_confirmation_message import LoadbalanceUpdateConfirmationMessage
from pydeployr.services import config_service

config = ConfigLoader(config=config_service.load_configuration())
broker_address = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config.rmq_broker_username,
    password=config.rmq_broker_password,
    host=config.rmq_broker_host,
    port=config.rmq_broker_port
)

celery = Celery(
    'pybalancr.balancr_tasks',
    broker=broker_address,
    backend=broker_address,
    include=['pybalancr.balancr_tasks']
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

    # TODO: do smart stuff here
    # TODO: create confirmation message

    # loadbalance_update_confirmation_message = LoadbalanceUpdateConfirmationMessage(
    #     api_id=api_id,
    #     lb_host='some.host',
    #     lb_api_port=80,
    #     api_domainname='some.com'
    # )

    return '>>>>>>>>>>>>>>>>>>>>>> undeploy_task'


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
        lb_host='api.apitrary.com',
        lb_api_port=80,
        api_domainname='{}.api.apitrary.com'.format(deploy_task['api_id'])
    )

#########################################################################
#
# MAIN
#
#########################################################################

if __name__ == '__main__':
    celery.start()
