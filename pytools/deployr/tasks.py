# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from __future__ import absolute_import
from celery import Celery
from kombu.entity import Queue
from tornado.options import enable_pretty_logging
from deployr.conf.config_loader import ConfigLoader
from deployr.messages.deploy_confirmation_message import DeployConfirmationMessage
from deployr.services import config_service
from deployr.services.deploy_service import DeployService

enable_pretty_logging()

config = ConfigLoader(config=config_service.load_configuration())
broker_address = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config.rmq_broker_username,
    password=config.rmq_broker_password,
    host=config.rmq_broker_host,
    port=config.rmq_broker_port
)

celery = Celery('deployr',
#    broker='amqp://guest:guest@localhost',
    broker=broker_address,
#    backend='amqp://guest:guest@localhost',
    backend=broker_address,
    include=['deployr.tasks'])

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
    return undeploy_task


@celery.task
def deploy(deploy_task):
    # TODO: Validate the deploy_task

    print("Processing task: {}".format(deploy_task))

    deploy_service = DeployService(config=config)
    deploy_service.deploy_api(
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
        host='local.example.com',
        port=19999,
        status=0
    ).to_dict()


#########################################################################
#
# MAIN
#
#########################################################################

if __name__ == '__main__':
    celery.start()
