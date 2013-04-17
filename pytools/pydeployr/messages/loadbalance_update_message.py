# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
import time

LOADBALANCE_UPDATE_CONFIRMATION_QUEUE = 'loadbalance_update_confirmation_queue'
LOADBALANCE_UPDATE_CONFIRMATION_ROUTING_KEY = LOADBALANCE_UPDATE_CONFIRMATION_QUEUE

class LoadbalanceUpdateMessage(object):
    """
        A message object that is used for confirming a successful deployment
    """

    # the routing key for deploy confirmation
    routing_key = LOADBALANCE_UPDATE_CONFIRMATION_ROUTING_KEY

    # the exchange to use
    queue = LOADBALANCE_UPDATE_CONFIRMATION_QUEUE

    def __init__(self, api_id, api_host, api_port):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.api_host = api_host
        self.api_port = api_port
        self.created_at = time.strftime('%d %b %Y %H:%M:%S +0000', time.gmtime())

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'LOADBALANCE_UPDATE',
            'api_id': self.api_id,
            'api_host': self.api_host,
            'api_port': self.api_port,
            'created_at': self.created_at
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
