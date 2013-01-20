# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
from deployr_service.lib.deployr_base import DeployrBase


class UndeployTask(DeployrBase):
    """Undeploy task definition"""

    def __init__(self, message, config):
        """Initialize the Deploy task"""
        super(UndeployTask, self).__init__(config)
        self.message = message
        self.parse_parameters()

    def parse_parameters(self):
        """Read out all parameters"""
        self.task_type = UndeployTask.get_task_type()
        self.api_id = self.message['api_id']

    @staticmethod
    def get_task_type():
        return 'UNDEPLOY'
