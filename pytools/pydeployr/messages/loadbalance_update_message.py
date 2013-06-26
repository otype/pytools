# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
import time


class LoadbalanceUpdateMessage(object):
    """
        A message object that is used for confirming a successful deployment
    """

    # the exchange to use
    queue = 'loadbalance_update_confirmation_queue'

    # the routing key for deploy confirmation
    routing_key = queue

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
