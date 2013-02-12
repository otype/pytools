# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from deployr import tasks
from deployr.messages.undeploy_message import UndeployMessage

UNDEPLOY_ROUTING_KEY = 'undeploy.undeploy'
UNDEPLOY_QUEUE = 'deployr.undeploy'


def undeploy_api(api_id, app_host):
    undeploy_message = UndeployMessage(api_id=api_id)
    logging.debug('Preparing UndeployMessage: {}'.format(undeploy_message.to_dict()))
    result = tasks.undeploy.apply_async(
        args=[undeploy_message.to_dict()],
        exchange='C.dq',
        routing_key=app_host
    )
    return result.get()
