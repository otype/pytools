# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
from deployr_service.lib.errors import InvalidTaskTypeException
from deployr_service.services import logging_service

#
# Logger
#
logger = logging_service.get_logger()


class BaseTask(object):
    """
        Undeploy task definition
    """

    def __init__(self, message, attribute_list, config):
        """
            Initialize the Deploy task
        """
        self.message = message
        self.config = config
        if not self.is_valid_deploy_message(attribute_list=attribute_list):
            logger.error('Task type {} is unknown.'.format(self.get_task_type()))
            raise InvalidTaskTypeException('Task type {} is unknown.'.format(self.get_task_type()))

        # parse the message for necessary parameters
        self.parse_parameters()

    def get_task_type(self):
        """
            Parse the message and read the task type
        """
        return self.message['task_type'].upper()

    def parse_parameters(self):
        """
            Read out all parameters needed to run the deploy task.

            Overwrite this!
        """
        pass

    def is_valid_deploy_message(self, attribute_list):
        """
            Parses an incoming message for all attributes.

            Only if all attributes have been provided, we will
            pass on to the next step: deploy.
        """
        for item in attribute_list:
            if item not in self.message:
                logger.warning('Missing attribute {} in message.'.format(item))
                return False

        return True

    def run(self):
        """
            Hooked-up method to run when undeploying an API

            Overwrite this!
        """
        pass

    def send_confirmation(self):
        """
            Send confirmation message

            Overwrite this!
        """
        pass
