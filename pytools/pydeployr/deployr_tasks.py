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
from pydeployr.conf.config_loader import ConfigLoader
from pydeployr.messages.deploy_confirmation_message import DeployConfirmationMessage
from pydeployr.messages.undeploy_confirmation_message import UndeployConfirmationMessage
from pydeployr.services import config_service
from pydeployr.services.deploy_service import DeployService
from pydeployr.services.undeploy_service import UndeployService

config = ConfigLoader(config=config_service.load_configuration())
broker_address = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config.rmq_broker_username,
    password=config.rmq_broker_password,
    host=config.rmq_broker_host,
    port=config.rmq_broker_port
)

celery = Celery('deployr_tasks', broker=broker_address, backend=broker_address, include=['pydeployr.deployr_tasks'])
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
    undeploy_service = UndeployService(config=config)
    status = undeploy_service.undeploy_api(api_id=api_id)
    return UndeployConfirmationMessage(api_id=api_id, status=status).to_dict()


@celery.task
def deploy(deploy_task):
    """
        DEPLOY an API
    """
    logging.info('Using Rabbitmq host:{} on port:{}'.format(config.rmq_broker_host, config.rmq_broker_port))

    # TODO: Validate the deploy_task
    logging.info("Processing task: {}".format(deploy_task))

    deploy_service = DeployService(config=config)
    status_code, host_ip, port = deploy_service.deploy_api(
        api_id=deploy_task['api_id'],
        db_host=deploy_task['db_host'],
        genapi_version=deploy_task['genapi_version'],
        log_level=deploy_task['log_level'],
        environment=config.environment,
        entities=deploy_task['entities'],
        api_key=deploy_task['api_key']
    )

    return DeployConfirmationMessage(
        api_id=deploy_task['api_id'],
        genapi_version=deploy_task['genapi_version'],
        host=host_ip,
        port=port,
        status=status_code
    ).to_dict()

#########################################################################
#
# MAIN
#
#########################################################################

if __name__ == '__main__':
    celery.start()
