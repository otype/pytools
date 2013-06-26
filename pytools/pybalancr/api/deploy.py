# -*- coding: utf-8 -*-
"""

    pybalancr

    created by hgschmidt on 17.04.2013, 23:10 CET

    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pytools.pybalancr import balancr_tasks
from pytools.pydeployr.messages.loadbalance_update_message import LoadbalanceUpdateMessage

DEPLOY_ROUTING_KEY = 'deploy.deploy'
DEPLOY_QUEUE = 'balancr.deploy'


def loadbalance_deploy(api_id, api_host, api_port):
    loadbalance_update_message = LoadbalanceUpdateMessage(api_id=api_id, api_host=api_host, api_port=api_port)
    logging.debug("Received Loadbalance update message: {}".format(loadbalance_update_message.to_json()))

    return balancr_tasks.deploy.apply_async(
        args=[loadbalance_update_message.to_dict()],
        queue=DEPLOY_QUEUE,
        routing_key=DEPLOY_ROUTING_KEY
    ).get()
