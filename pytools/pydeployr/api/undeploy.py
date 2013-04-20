# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pydeployr import deployr_tasks
from pydeployr.messages.undeploy_message import UndeployMessage

UNDEPLOY_ROUTING_KEY = 'undeploy.undeploy'
UNDEPLOY_QUEUE = 'deployr.undeploy'


def undeploy_api(api_id, api_host):
    """
        Undeploy a given API from given app host
    """
    logging.info('Undeploying API ID:{} on API HOST:{}'.format(api_id, api_host))
    undeploy_message = UndeployMessage(api_id=api_id, api_host=api_host)
    logging.info('Preparing UndeployMessage: {}'.format(undeploy_message.to_dict()))

    return deployr_tasks.undeploy.apply_async(
        args=[undeploy_message.to_dict()],
        exchange='C.dq',
        routing_key=api_host
    ).get()
