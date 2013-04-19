# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 - 2013 apitrary

"""
import json
import time

class DeployConfirmationMessage(object):
    """
        A message object that is used for confirming a successful deployment
    """

    def __init__(self, api_id, genapi_version, api_host, api_port, status):
        """
            Setting the base variables for this message object
        """
        self.api_id = api_id
        self.genapi_version = genapi_version
        self.api_host = api_host
        self.api_port = api_port
        self.status = status
        self.created_at = time.strftime('%d %b %Y %H:%M:%S +0000', time.gmtime())

    def to_dict(self):
        """
            Return a dictionary (JSON) from this object
        """
        return {
            'task_type': 'DEPLOY_CONFIRMATION',
            'api_id': self.api_id,
            'genapi_version': self.genapi_version,
            'api_host': self.api_host,
            'api_port': self.api_port,
            'status': self.status,
            'created_at': self.created_at
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
