# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json

class UndeployMessage(object):
    """
        An undeploy message
    """

    def __init__(self, api_id):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'UNDEPLOY',
            'api_id': self.api_id
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
