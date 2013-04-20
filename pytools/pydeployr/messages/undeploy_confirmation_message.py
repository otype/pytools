# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 - 2013 apitrary

"""
import json


class UndeployConfirmationMessage(object):
    """
        An undeploy message
    """

    def __init__(self, api_id, api_host, status):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.api_host = api_host
        self.status = status

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'UNDEPLOY_CONFIRMATION',
            'api_id': self.api_id,
            'api_host': self.api_host,
            'status': self.status
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
