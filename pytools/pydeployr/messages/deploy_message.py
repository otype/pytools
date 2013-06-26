# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 - 2013 apitrary

"""
import json


class DeployMessage(object):
    """
        A Deploy message
    """

    task_type = 'DEPLOY'

    def __init__(self, api_id, db_host, db_port, genapi_version, log_level, entities, api_key):
        self.api_id = api_id
        self.db_host = db_host
        self.db_port = db_port
        self.genapi_version = genapi_version
        self.log_level = log_level
        self.entities = entities
        self.api_key = api_key

    def to_dict(self):
        """
            Return a dictionary from this object
        """
        return {
            'task_type': self.task_type,
            'api_id': self.api_id,
            'db_host': self.db_host,
            'db_port': self.db_port,
            'genapi_version': self.genapi_version,
            'log_level': self.log_level,
            'entities': self.entities,
            'api_key': self.api_key
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
