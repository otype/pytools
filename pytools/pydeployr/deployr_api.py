# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pytools.pydeployr import deployr_tasks
from pytools.pydeployr.messages.undeploy_message import UndeployMessage
from pytools.pydeployr.messages.deploy_message import DeployMessage


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
        queue='deployr.deploy',
        routing_key='deploy.deploy'
    ).get()


def undeploy_api(api_id, api_host):
    """
        Undeploy a given API from given app host
    """
    logging.info('Undeploying API ID:{} on API HOST:{}'.format(api_id, api_host))
    undeploy_message = UndeployMessage(api_id=api_id, api_host=api_host)
    logging.info('Preparing UndeployMessage: {}'.format(undeploy_message.to_dict()))

    return deployr_tasks.undeploy.apply(
        args=[undeploy_message.to_dict()],
        exchange='C.dq',
        routing_key=api_host
    ).get()
