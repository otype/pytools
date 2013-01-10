# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
from deployr_service.event_reporter_service.event_reporter import EventReporter
from deployr_service.models.base_task import BaseTask
from deployr_service.models.blocking_message_tx import BlockingMessageTx
from deployr_service.models.undeploy_confirmation_message import UndeployConfirmationMessage
from deployr_service.services import undeploy_service


class UndeployTask(BaseTask):
    """
        Undeploy task definition
    """

    def __init__(self, message, config):
        """
            Initialize the Deploy task
        """
        attribute_list = ['task_type', 'api_id']
        super(UndeployTask, self).__init__(message, attribute_list, config)

    def parse_parameters(self):
        """
            Read out all parameters needed to run the deploy task
        """
        self.task_type = self.get_task_type()
        self.api_id = self.message['api_id']

    def run(self):
        """
            Hooked-up method to run when undeploying an API
        """
        self.last_execution_status = undeploy_service.undeploy_api(api_id=self.api_id)
        return self.last_execution_status

    def send_confirmation(self):
        """
            Send confirmation message
        """
        undeploy_confirmation_message = UndeployConfirmationMessage(
            api_id=self.api_id,
            status=self.last_execution_status
        )

        # Report this deployment back to Event Reporter
        event_reporter = EventReporter()
        event_reporter.send(undeploy_confirmation_message)

        message_tx = BlockingMessageTx(config=self.config)
        return message_tx.send(message=undeploy_confirmation_message)
