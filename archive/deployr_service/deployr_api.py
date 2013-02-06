# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from archive.deployr_service.deployr_base import DeployrBase
from archive.deployr_service.lib.errors import InvalidTaskType
from archive.deployr_service.lib.returncodes import RETURNCODE
from archive.deployr_service.messages.deploy_confirmation_message import DeployConfirmationMessage
from archive.deployr_service.messages.undeploy_confirmation_message import UndeployConfirmationMessage
from archive.deployr_service.services.deploy_service import DeployService
from archive.deployr_service.services.undeploy_service import UndeployService
from archive.deployr_service.task_types.deploy_task import DeployTask
from archive.deployr_service.task_types.undeploy_task import UndeployTask

class DeployrApi(DeployrBase):
    """
        Official API for Deployr. Call execute_task to run one of the defined task types.
    """

    def __init__(self, config):
        super(DeployrApi, self).__init__(config)
        self.deploy_service = DeployService(config=self.config)
        self.undeploy_service = UndeployService(config=self.config)

    def execute_task(self, task):
        """
            Execute task depending on task type
        """
        if type(task) != dict:
            self.loggr.error("Not a valid task! Cannot execute task!")
            return RETURNCODE.OS_INVALID_ARGUMENT

        if 'task_type' not in task:
            self.loggr.error("Not a valid task! Cannot execute task!")
            return RETURNCODE.OS_INVALID_ARGUMENT

        task_type = task['task_type']
        return_status_set = None
        try:
            if task_type == DeployTask.get_task_type():
                deploy_task = DeployTask(message=task, config=self.config)
                return_status_set = self.deploy(task=deploy_task)
            elif task_type == UndeployTask.get_task_type():
                undeploy_task = UndeployTask(message=task, config=self.config)
                return_status_set = self.undeploy(task=undeploy_task)
            else:
                self.loggr.warning("Unknown task type: {}".format(task.task_type))
        except InvalidTaskType, e:
            self.loggr.error('Could not create a valid task! Error: {}'.format(e))
        except TypeError, e:
            self.loggr.error('Task type is not identifiable! Error: {}'.format(e))

        return return_status_set

    def deploy(self, task):
        """
            Execute the deploy task
        """
        status_code, application_host, assigned_port = self.deploy_service.deploy_api(
            api_id=task.api_id,
            db_host=task.db_host,
            genapi_version=task.genapi_version,
            log_level=task.log_level,
            environment=self.config['ENV'],
            entities=task.entities,
            api_key=task.api_key
        )
        return DeployConfirmationMessage(
            api_id=task.api_id,
            genapi_version=task.genapi_version,
            host=application_host,
            status=status_code,
            port=assigned_port
        ).to_dict()

    def undeploy(self, task):
        """
            Execute the undeploy task
        """
        status_code = self.undeploy_service.undeploy_api(api_id=task.api_id)
        return UndeployConfirmationMessage(api_id=task.api_id, status=status_code).to_dict()

