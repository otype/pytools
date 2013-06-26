# -*- coding: utf-8 -*-
"""

    pybalancr

    created by hgschmidt on 17.04.2013, 23:10 CET

    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pytools.pybalancr import balancr_tasks
from pytools.pydeployr.messages.loadbalance_remove_message import LoadbalanceRemoveMessage
from pytools.pydeployr.messages.loadbalance_update_message import LoadbalanceUpdateMessage


def loadbalance_deploy(api_id, api_host, api_port):
    """
        Send a loadbalance update message to the message queue.

        :param api_id:
        :param api_host:
        :param api_port:
        :return:
    """
    loadbalance_update_message = LoadbalanceUpdateMessage(api_id=api_id, api_host=api_host, api_port=api_port)
    logging.debug("Received Loadbalance update message: {}".format(loadbalance_update_message.to_json()))

    return balancr_tasks.deploy.apply_async(
        args=[loadbalance_update_message.to_dict()],
        queue='balancr.deploy',
        routing_key='deploy.deploy'
    ).get()


def loadbalance_undeploy(api_id):
    """
        Send a loadbalance remove message to the message queue

        :param api_id:
        :return:
    """
    loadbalance_remove_message = LoadbalanceRemoveMessage(api_id=api_id)
    logging.debug("Received Loadbalance API remove message: {}".format(loadbalance_remove_message.to_json()))

    return balancr_tasks.undeploy.apply_async(
        args=[loadbalance_remove_message.to_dict()],
        queue='balancr.undeploy',
        routing_key='undeploy.undeploy'
    ).get()
