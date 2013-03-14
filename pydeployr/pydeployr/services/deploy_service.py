# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:45 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import sys
import logging
from pydeployr.conf.returncodes import RETURNCODE
from pydeployr.services import os_service, network_service
from pydeployr.services.supervisor_xml_rpc_service import SupervisorXmlRpcService
from pydeployr.services.template_service import TemplateService

class DeployService(object):
    """
        Deploy service.
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
            # Use this for Debian 6
#            config_file_name = '/etc/supervisor.d/{}.conf'.format(api_id)
            # Use this for Ubuntu
            config_file_name = '/etc/supervisor/conf.d/{}.conf'.format(api_id)
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

    def get_required_params(self, api_id):
        """
            Get required parameter set
        """
        assigned_port = network_service.get_open_port()
        application_host = network_service.get_local_public_ip_address()
        config_file_name = self.define_supervisor_config_file(api_id=api_id)

        logging.debug('Assigning port: {}'.format(assigned_port))
        logging.debug('Current host is {}'.format(application_host))
        logging.debug('Configuration file name is {}'.format(config_file_name))
        return assigned_port, application_host, config_file_name

    def deploy_api(self, api_id, db_host, genapi_version, log_level, environment, entities, api_key):
        """
            Deploy an GenAPI
        """
        assigned_port, application_host, config_file_name = self.get_required_params(api_id=api_id)

        logging.info('Writing configuration for API: {}'.format(api_id))
        self.template_service.write_genapi_base_tpl(
            genapi_api_id=api_id,
            python_interpreter=os_service.python_interpreter_path(),
            # Debian
#            genapi_start='/usr/bin/genapi_runner.py',
            # Ubuntu
            genapi_start='/usr/local/bin/genapi_runner.py',
            logging_level=log_level,
            riak_host=db_host,
            app_port=assigned_port,
            genapi_version=genapi_version,
            genapi_env=environment,
            genapi_entity_list=entities,
            genapi_api_key=api_key,
            genapi_home_directory='/home/genapi',
            genapi_user='genapi',
            genapi_log_file='{}/genapi_{}.log'.format('/home/genapi', api_id),
            config_file_name=config_file_name
        )

        if self.is_already_running(api_id=api_id):
            logging.info('An API with API ID=\'{}\' is already running! Stopping it, first.'.format(api_id))
            self.supervisor_xml_rpc_service.stop(api_id)
            logging.info('Removing API ID=\'{}\''.format(api_id))
            self.supervisor_xml_rpc_service.remove_group(api_id)

        self.supervisor_xml_rpc_service.reload_config()
        logging.info('Adding (deploying) new API with API ID=\'{}\' on host=\'{}\' on port=\'{}\''.format(
            api_id, application_host, assigned_port)
        )
        self.supervisor_xml_rpc_service.add_group(api_id)

        return RETURNCODE.OS_SUCCESS, application_host, assigned_port
