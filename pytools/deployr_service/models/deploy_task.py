# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
from deployr_service.event_reporter_service.event_reporter import EventReporter
from deployr_service.globals.environments import RETURNCODE
from deployr_service.models.deploy_confirmation_message import DeployConfirmationMessage
from deployr_service.services import deploy_service
from deployr_service.models.base_task import BaseTask
from deployr_service.models.blocking_message_tx import BlockingMessageTx
from deployr_service.services import logging_service

#
# Logger
#
logger = logging_service.get_logger()


class DeployTask(BaseTask):
    """
        Deploy task definition
    """

    def __init__(self, message, config):
        """
            Initialize the Deploy task
        """
        attribute_list = ['task_type', 'api_id', 'db_host', 'db_port', 'genapi_version', 'log_level',
                          'entities', 'api_key']
        self.config = config
        super(DeployTask, self).__init__(message, attribute_list, config)

    def parse_parameters(self):
        """
            Read out all parameters needed to run the deploy task

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
        self.task_type = self.get_task_type()
        self.api_id = self.message['api_id']
        self.db_host = self.message['db_host']
        self.genapi_version = self.message['genapi_version']
        self.log_level = self.message['log_level']
        self.entities = self.message['entities']
        self.api_key = self.message['api_key']

    def run(self):
        """
            Hooked-up method to run when deploying an API
        """
        status_code, application_host, assigned_port = deploy_service.deploy_api(
            api_id=self.api_id,
            db_host=self.db_host,
            genapi_version=self.genapi_version,
            log_level=self.log_level,
            environment=self.config['NAME'],
            entities=self.entities,
            api_key=self.api_key
        )

        self.last_execution_status = status_code
        self.application_host = application_host
        self.assigned_port = assigned_port

        return self.last_execution_status

    def send_confirmation(self):
        """
            Send confirmation message
        """
        if self.last_execution_status == RETURNCODE.OS_ERROR:
            logger.error('Cannot send confirmation. Last run had an error.')
            return RETURNCODE.OS_ERROR

        deploy_confirmation_message = DeployConfirmationMessage(
            api_id=self.api_id,
            genapi_version=self.genapi_version,
            host=self.application_host,
            port=self.assigned_port,
            status=self.last_execution_status
        )

        # Report this deployment back to Event Reporter
        event_reporter = EventReporter()
        event_reporter.send(deploy_confirmation_message)

        # Now, send the message to rmq
        message_tx = BlockingMessageTx(config=self.config)
        return message_tx.send(message=deploy_confirmation_message)
