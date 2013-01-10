# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
from deployr_service.globals.queue_settings import DEPLOY_ROUTING_KEY, GENAPI_DEPLOYMENT_QUEUE


class DeployMessage(object):
    """
        A Deploy message
    """

    # the routing key for deploy confirmation
    routing_key = DEPLOY_ROUTING_KEY

    # the queue name
    queue = GENAPI_DEPLOYMENT_QUEUE

    def __init__(self, api_id, db_host, db_port, genapi_version, log_level, entities, api_key):
        """
            Setting the base variables for this message object
        """
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
            'task_type': 'DEPLOY',
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
