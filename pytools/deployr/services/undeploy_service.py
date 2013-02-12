# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:45 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import logging
from deployr.conf.returncodes import RETURNCODE
from deployr.services import filesystem_service
from deployr.services.supervisor_xml_rpc_service import SupervisorXmlRpcService
from deployr.services.template_service import TemplateService

class UndeployService(object):
    """
        Undeploy service.
    """

    def __init__(self, config):
        self.config = config
        self.template_service = TemplateService()
        self.supervisor_xml_rpc_service = SupervisorXmlRpcService(self.config.supervisord_xml_rpc_server)

    def define_supervisor_config_file(self, api_id):
        """
            Define the config file name depending on the platform.
        """
        if sys.platform == 'darwin':
            config_file_name = '{}.conf'.format(api_id)
        elif sys.platform == 'linux2':
            config_file_name = '/etc/supervisor.d/{}.conf'.format(api_id)
        else:
            config_file_name = '{}.conf'.format(api_id)
        return config_file_name

    def is_already_running(self, api_id):
        """
            Check if API with given API ID is running or not.
        """
        process_info = self.supervisor_xml_rpc_service.get_process_info(api_id)
        if process_info is None:
            return False

        if process_info == RETURNCODE.OS_ERROR:
            logging.error('API is not running or connection to supervisor failed!')
            return False

        if process_info['statename'] != 'RUNNING':
            return False

        return True

    def stop_api(self, api_id):
        logging.info('Stopping API: {}'.format(api_id))
        process_info = self.supervisor_xml_rpc_service.stop(app_name=api_id)
        if process_info is None:
            return False

        if process_info == RETURNCODE.OS_ERROR:
            logging.error('API is not running or connection to supervisor failed!')
            return False

#        if process_info['statename'] != 'STOPPED':
#            return False
        logging.info('>>>>> PROCESSINFO: {}'.format(process_info))

        return True

    def remove_api(self, api_id):
        logging.info('Removing API: {} from supervisor'.format(api_id))
        process_info = self.supervisor_xml_rpc_service.remove_group(group_name=api_id)
        if process_info is None:
            return False

        if process_info == RETURNCODE.OS_ERROR:
            logging.error('API is not running or connection to supervisor failed!')
            return False

#        if process_info['statename'] != 'REMOVED':
#            return False
        logging.info('>>>>> PROCESSINFO: {}'.format(process_info))

        return True

    def delete_api_config(self, api_id):
        """
            Deleting the supervisor config file for given API
        """
        logging.info("Deleting supervisor config for API: {}".format(api_id))
        config_file = self.define_supervisor_config_file(api_id=api_id)
        filesystem_service.delete_file(config_file)

    def undeploy_api(self, api_id):
        """
            Undeploy an GenAPI
        """
        logging.info("Undeploying API: {}".format(api_id))

        logging.info('1')
        if self.is_already_running(api_id=api_id):
            logging.info('2')
            self.stop_api(api_id=api_id)

        logging.info('3')
        self.remove_api(api_id=api_id)
        logging.info('4')
        self.delete_api_config(api_id=api_id)
        logging.info('5')
        self.supervisor_xml_rpc_service.reload_config()
        logging.info('6')
        return RETURNCODE.OS_SUCCESS
