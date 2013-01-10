# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
import json
from deployr_service.globals.environments import TASKALIAS
from deployr_service.models.deploy_task import DeployTask
from deployr_service.models.errors import InvalidTaskTypeException, UnacceptableMessageException
from deployr_service.models.undeploy_task import UndeployTask
from deployr_service.services import logging_service
from deployr_service.services.config_service import ConfigService

logger = logging_service.get_logger()


class TaskFactory(object):
    """
        A generic task as basis for all task type classes
    """

    def __init__(self):
        """
            We need the configuration upon task creation
        """
        self.config = ConfigService.load_configuration()

    def load_message(self, message):
        """
           Loads the message.

           Will throw ValueError if this is no valid JSON
        """
        self.message = json.loads(message)

        # Validate the task! This fails if it's not a valid task.
        self.validate_task()

    def get_task(self):
        """
            Create the corresponding task object
        """
        try:
            if self.task_type() == TASKALIAS.DEPLOY_TASK:
                return DeployTask(self.message, self.config)
            elif self.task_type() == TASKALIAS.UNDEPLOY_TASK:
                return UndeployTask(self.message, self.config)
        except InvalidTaskTypeException, e:
            logger.error('Could not create a valid task! Error: {}'.format(e))
            return None
        except TypeError, e:
            logger.error('Task type is not identifiable! Error: {}'.format(e))
            return None

    def validate_task(self):
        """
            Is the incoming message a valid task?
        """
        if 'task_type' not in self.message:
            logger.error('Missing task type in message: {}'.format(self.message))
            raise UnacceptableMessageException('Missing task type in message')

        logger.debug('Valid task of type: {}'.format(self.task_type()))

    def task_type(self):
        """
            Parse the message and read the task type
        """
        return self.message['task_type'].upper()
