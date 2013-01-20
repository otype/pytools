# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json

class UndeployConfirmationMessage(object):
    """
        An undeploy message
    """

    def __init__(self, api_id, status):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.status = status

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'UNDEPLOY_CONFIRMATION',
            'api_id': self.api_id,
            'status': self.status
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
