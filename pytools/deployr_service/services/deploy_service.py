# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:45 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
from deployr_service.config.template_config import GENAPI_TEMPLATES_CONFIG
from deployr_service.lib.deployr_base import DeployrBase
from deployr_service.services.network_service import NetworkService
from deployr_service.services.supervisor_xml_rpc_service import SupervisorXmlRpcService
from deployr_service.sortout.environments import RETURNCODE
from deployr_service.services import template_service

class DeployService(DeployrBase):
    """
        Deploy service.
    """

    def __init__(self, config):
        """
            Init & setup supervisor
        """
        super(DeployService, self).__init__(config)
        self.supervisor_xml_rpc_service = SupervisorXmlRpcService(config=self.config)
        self.network_service = NetworkService(self.config)

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
            self.loggr.error('API is not running or connection to supervisor failed!')
            return False

        if process_info['statename'] != 'RUNNING':
            return False

        return True

    def deploy_api(self, api_id, db_host, genapi_version, log_level, environment, entities, api_key):
        """
            Deploy an GenAPI
        """

        assigned_port = self.network_service.get_open_port()
        self.loggr.debug('Assigning port: {}'.format(assigned_port))

        application_host = self.network_service.get_local_public_ip_address()
        self.loggr.debug('Current host is {}'.format(application_host))

        config_file_name = self.define_supervisor_config_file(api_id=api_id)
        self.loggr.debug('Configuration file name is {}'.format(config_file_name))

        # Write the supervisor config
        self.loggr.info('Writing configuration for API: {}'.format(api_id))
        template_service.write_genapi_base_tpl(
            genapi_api_id=api_id,
            python_interpreter=GENAPI_TEMPLATES_CONFIG['GENAPI_BASE']['GENAPI_PYTHON_EXEC'],
            genapi_start=GENAPI_TEMPLATES_CONFIG['GENAPI_BASE']['GENAPI_START_SCRIPT'],
            logging_level=log_level,
            riak_host=db_host,
            app_port=assigned_port,
            genapi_version=genapi_version,
            genapi_env=environment,
            genapi_entity_list=entities,
            genapi_api_key=api_key,
            genapi_home_directory=GENAPI_TEMPLATES_CONFIG['GENAPI_BASE']['GENAPI_HOME_DIRECTORY'],
            genapi_user=GENAPI_TEMPLATES_CONFIG['GENAPI_BASE']['GENAPI_USER'],
            genapi_log_file='{}/genapi_{}.log'.format(
                GENAPI_TEMPLATES_CONFIG['GENAPI_BASE']['GENAPI_HOME_DIRECTORY'],
                api_id
            ),
            config_file_name=config_file_name
        )

        # If an API with given API ID is already running, we stop that one, first.
        if self.is_already_running(api_id=api_id):
            self.loggr.info('An API with API ID=\'{}\' is already running! Stopping it, first.'.format(api_id))
            self.supervisor_xml_rpc_service.stop(api_id)

            self.loggr.info('Removing API ID=\'{}\''.format(api_id))
            self.supervisor_xml_rpc_service.remove_group(api_id)

        # Re-read the configuration files
        self.supervisor_xml_rpc_service.reload_config()

        # add the config (implicitly starts the genapi)
        self.loggr.info('Adding (deploying) new API with API ID=\'{}\' on host=\'{}\' on port=\'{}\''.format(
            api_id, application_host, assigned_port)
        )
        self.supervisor_xml_rpc_service.add_group(api_id)

        return RETURNCODE.OS_SUCCESS, application_host, assigned_port
