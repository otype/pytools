# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
from pytools.pydeployr import deployr_tasks
from pytools.pydeployr.messages.deploy_message import DeployMessage

DEPLOY_ROUTING_KEY = 'deploy.deploy'
DEPLOY_QUEUE = 'deployr.deploy'


def deploy_api(api_id, entities, api_key, db_host, db_port=8098, genapi_version=1, log_level='info'):
    """
        Deploy an API with given parameters
    """
    deploy_message = DeployMessage(
        api_id=api_id,
        entities=entities,
        api_key=api_key,
        db_host=db_host,
        db_port=db_port,
        genapi_version=genapi_version,
        log_level=log_level
    )

    return deployr_tasks.deploy.apply_async(
        args=[deploy_message.to_dict()],
        queue=DEPLOY_QUEUE,
        routing_key=DEPLOY_ROUTING_KEY
    ).get()

