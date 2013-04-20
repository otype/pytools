# -*- coding: utf-8 -*-
"""

    pybalancr

    created by hgschmidt on 17.04.2013, 23:10 CET

    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pybalancr import balancr_tasks
from pydeployr.messages.loadbalance_remove_message import LoadbalanceRemoveMessage

DEPLOY_ROUTING_KEY = 'undeploy.undeploy'
DEPLOY_QUEUE = 'balancr.undeploy'


def loadbalance_undeploy(api_id):
    loadbalance_remove__message = LoadbalanceRemoveMessage(api_id=api_id)
    logging.debug("Received Loadbalance API remove message: {}".format(loadbalance_remove__message.to_json()))

    return balancr_tasks.undeploy.apply_async(
        args=[loadbalance_remove__message.to_dict()],
        queue=DEPLOY_QUEUE,
        routing_key=DEPLOY_ROUTING_KEY
    ).get()
