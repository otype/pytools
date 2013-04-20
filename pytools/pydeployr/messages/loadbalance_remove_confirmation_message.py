# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
import time


class LoadbalanceRemoveConfirmationMessage(object):
    """
        A message object that is used for confirming a successful removal in loadbalancer
    """

    def __init__(self, api_id):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.created_at = time.strftime('%d %b %Y %H:%M:%S +0000', time.gmtime())

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'LOADBALANCE_REMOVE_CONFIRMATION',
            'api_id': self.api_id,
            'created_at': self.created_at
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
