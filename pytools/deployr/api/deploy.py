# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr import tasks
from deployr.messages.deploy_message import DeployMessage

DEPLOY_ROUTING_KEY = 'deploy.deploy'
DEPLOY_QUEUE = 'deployr.deploy'


def deploy_api(api_id, entities, api_key, db_host, db_port=8098, genapi_version=1, log_level='info'):
    deploy_message = DeployMessage(
        api_id=api_id,
        entities=entities,
        api_key=api_key,
        db_host=db_host,
        db_port=db_port,
        genapi_version=genapi_version,
        log_level=log_level
    )
    result = tasks.deploy.apply_async(
        args=[deploy_message.to_dict()],
        queue=DEPLOY_QUEUE,
        routing_key=DEPLOY_ROUTING_KEY
    )
    return result.get()