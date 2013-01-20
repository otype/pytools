# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
from deployr_service.lib.deployr_base import DeployrBase

class DeployTask(DeployrBase):
    """
        Deploy task definition:

        {
            “task_type”: ”DEPLOY”,
            “api_id”: “88sdhv98shdvlh123”,
            “db_host”: “db1.apitrary.net”,
            “db_port”: 8098,
            “genapi_version”: 1,
            “log_level”: “debug”,
            “entities”: [ “user”, “object”, “contact” ],
            “api_key”: “iis9nd9vnsdvoijsdvoin9s8dv”
        }
    """

    def __init__(self, message, config):
        """
            Initialize the Deploy task
        """
        super(DeployTask, self).__init__(config)
        self.message = message
        self.parse_parameters()

    def parse_parameters(self):
        """
            Read out all parameters
        """
        self.task_type = DeployTask.get_task_type()
        self.api_id = self.message['api_id']
        self.db_host = self.message['db_host']
        self.genapi_version = self.message['genapi_version']
        self.log_level = self.message['log_level']
        self.entities = self.message['entities']
        self.api_key = self.message['api_key']

    @staticmethod
    def get_task_type():
        return 'DEPLOY'
