# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
import time


class LoadbalanceUpdateConfirmationMessage(object):
    """
        A message object that is used for confirming a successful deployment
    """

    # the routing key for deploy confirmation
    routing_key = 'loadbalance_update_confirmation_queue'

    # the exchange to use
    queue = routing_key

    def __init__(self, api_id, lb_host, lb_api_port, api_domainname):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.lb_host = lb_host
        self.lb_api_port = lb_api_port
        self.api_domainname = api_domainname
        self.created_at = time.strftime('%d %b %Y %H:%M:%S +0000', time.gmtime())

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'LOADBALANCE_UPDATE_CONFIRMATION',
            'api_id': self.api_id,
            'lb_host': self.lb_host,
            'lb_api_port': self.lb_api_port,
            'api_domainname': self.api_domainname,
            'created_at': self.created_at
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
