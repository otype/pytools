# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:45 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
from deployr_service.config.template_config import GENAPI_TEMPLATES_CONFIG
from deployr_service.globals.environments import RETURNCODE
from deployr_service.services import logging_service, supervisor_xml_rpc_service, network_service, template_service

#
# Logger
#
logger = logging_service.get_logger()


def define_supervisor_config_file(api_id):
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


def is_already_running(api_id):
    """
        Check if API with given API ID is running or not.
    """
    process_info = supervisor_xml_rpc_service.get_process_info(api_id)
    if process_info is None:
        return False

    if process_info == RETURNCODE.OS_ERROR:
        logger.error('API is not running or connection to supervisor failed!')
        return False

    if process_info['statename'] != 'RUNNING':
        return False

    return True


def deploy_api(api_id, db_host, genapi_version, log_level, environment, entities, api_key):
    """
        Deploy an GenAPI
    """
    assigned_port = network_service.get_open_port()
    logger.debug('Assigning port: {}'.format(assigned_port))

    application_host = network_service.get_local_public_ip_address()
    logger.debug('Current host is {}'.format(application_host))

    config_file_name = define_supervisor_config_file(api_id=api_id)
    logger.debug('Configuration file name is {}'.format(config_file_name))

    # Write the supervisor config
    logger.info('Writing configuration for API: {}'.format(api_id))
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
    if is_already_running(api_id=api_id):
        logger.info('An API with API ID=\'{}\' is already running! Stopping it, first.'.format(api_id))
        supervisor_xml_rpc_service.stop(api_id)

        logger.info('Removing API ID=\'{}\''.format(api_id))
        supervisor_xml_rpc_service.remove_group(api_id)

    # Re-read the configuration files
    supervisor_xml_rpc_service.reload_config()

    # add the config (implicitly starts the genapi)
    logger.info('Adding (deploying) new API with API ID=\'{}\' on host=\'{}\' on port=\'{}\''.format(
        api_id, application_host, assigned_port)
    )
    supervisor_xml_rpc_service.add_group(api_id)

    return RETURNCODE.OS_SUCCESS, application_host, assigned_port