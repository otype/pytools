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
from pytools.pydeployr.config_loader import ConfigLoader
from pytools.pydeployr.messages.deploy_confirmation_message import DeployConfirmationMessage
from pytools.pydeployr.messages.undeploy_confirmation_message import UndeployConfirmationMessage
from pytools.pydeployr.services import config_service
from pytools.pydeployr.services.deploy_service import DeployService
from pytools.pydeployr.services.undeploy_service import UndeployService

config = ConfigLoader(config=config_service.load_configuration())
broker_address = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config.rmq_broker_username,
    password=config.rmq_broker_password,
    host=config.rmq_broker_host,
    port=config.rmq_broker_port
)

celery = Celery(
    'pytools.pydeployr.deployr_tasks',
    broker=broker_address,
    backend=broker_address,
    include=['pytools.pydeployr.deployr_tasks']
)
celery.conf.update(
    CELERY_DEFAULT_QUEUE='deployr.default',
    CELERY_DEFAULT_EXCHANGE='deployr.tasks',
    CELERY_QUEUES=(
        Queue('deployr.deploy', routing_key='deploy.#'),
        Queue('deployr.undeploy', routing_key='undeploy.#'),
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

    api_id = undeploy_task['api_id']
    api_host = undeploy_task['api_host']
    undeploy_service = UndeployService(config=config, api_host=api_host)
    status = undeploy_service.undeploy_api(api_id=api_id, api_host=api_host)
    return UndeployConfirmationMessage(api_id=api_id, api_host=api_host, status=status)


@celery.task
def deploy(deploy_task):
    """
        DEPLOY an API
    """
    logging.info('Using Rabbitmq host:{} on port:{}'.format(config.rmq_broker_host, config.rmq_broker_port))

    # TODO: Validate the deploy_task
    logging.info("Processing task: {}".format(deploy_task))

    deploy_service = DeployService(config=config)
    status_code, api_host, api_port = deploy_service.deploy_api(
        api_id=deploy_task['api_id'],
        db_host=deploy_task['db_host'],
        db_port=deploy_task['db_port'],
        genapi_version=deploy_task['genapi_version'],
        log_level=deploy_task['log_level'],
        environment=config.environment,
        entities=deploy_task['entities'],
        api_key=deploy_task['api_key']
    )

    return DeployConfirmationMessage(
        api_id=deploy_task['api_id'],
        genapi_version=deploy_task['genapi_version'],
        api_host=api_host,
        api_port=api_port,
        status=status_code
    )

#########################################################################
#
# MAIN
#
#########################################################################

if __name__ == '__main__':
    celery.start()
