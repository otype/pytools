# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 00:09 CET
    
    Copyright (c) 2012 apitrary

"""
import xmlrpclib
from deployr_service.globals.environments import RETURNCODE
from deployr_service.services import logging_service
from deployr_service.services.config_service import ConfigService

logger = logging_service.get_logger()

def get_supervisor_xml_rpc_server():
    """
        Get the Supervisor XML-RPC server address
    """
    # Load configuration
    configuration = ConfigService.load_configuration()

    # Contact XML-RPC on given address
    xml_rpc_address = configuration['SUPERVISOR_XML_RPC_SERVER_ADDRESS']

    return xmlrpclib.Server(xml_rpc_address), xml_rpc_address


def reload_config():
    """
        Reread the supervisor_api configuration files
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting reload of all configs'.format(xml_rpc_address))
    try:
        server.supervisor.reloadConfig()
    except xmlrpclib.Fault, e:
        logger.error('Could not reload config! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    return RETURNCODE.OS_SUCCESS


def start(app_name):
    """
        Start given application via supervisor_api
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting start of application: {}'.format(xml_rpc_address, app_name))
    try:
        if server.supervisor.startProcess(app_name):
            return RETURNCODE.OS_SUCCESS
    except xmlrpclib.Fault, e:
        logger.error('Could not start process \'{}\'! Error: {}'.format(app_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def stop(app_name):
    """
        Stop given application via supervisor_api
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting stop of application: {}'.format(xml_rpc_address, app_name))
    try:
        if server.supervisor.stopProcess(app_name):
            return RETURNCODE.OS_SUCCESS
    except xmlrpclib.Fault, e:
        logger.error('Could not stop process \'{}\'! Error: {}'.format(app_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def restart(app_name):
    """
        Start given application via supervisor_api
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting restart of application: {}'.format(xml_rpc_address, app_name))

    stop_state = stop(app_name)
    start_state = start(app_name)

    if (stop_state + start_state) > RETURNCODE.OS_SUCCESS:
        logger.error('Could not restart process \'{}\'!'.format(app_name))
        return RETURNCODE.OS_ERROR

    return RETURNCODE.OS_SUCCESS


def add_group(group_name):
    """
        Add new application to supervisor_api configuration
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting addition of application: {}'.format(xml_rpc_address, group_name))
    try:
        if server.supervisor.addProcessGroup(group_name):
            return RETURNCODE.OS_SUCCESS
    except xmlrpclib.Fault, e:
        logger.error('Could not add process group \'{}\'! Error: {}'.format(group_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def status():
    """
        Request status of given application
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting status'.format(xml_rpc_address))
    try:
        response = server.supervisor.getState()
        if 'statename' in response:
            if response['statename'] == 'RUNNING':
                logger.debug('SUPERVISOR XML-RPC({}): Status \'{}\''.format(response['statename']))
                return RETURNCODE.OS_SUCCESS
        return RETURNCODE.OS_ERROR
    except xmlrpclib.Fault, e:
        logger.error('Could not get status! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def get_all_process_info():
    """
        Request status of given application
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting all process info'.format(xml_rpc_address))
    try:
        return server.supervisor.getAllProcessInfo()
    except xmlrpclib.Fault, e:
        logger.error('Could not get all process info! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def get_process_info(app_name):
    """
        Request status of given application
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting process info for api_id: {}'.format(xml_rpc_address, app_name))
    try:
        all_processes = server.supervisor.getAllProcessInfo()
        for process in all_processes:
            if 'name' in process:
                if process['name'] == app_name:
                    return process
        return None
    except xmlrpclib.Fault, e:
        logger.error('Could not get the process info for: {}! Error: {}'.format(app_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def remove_group(group_name):
    """
        Remove application from supervisor_api context
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting removal of group: {}'.format(xml_rpc_address, group_name))
    try:
        if server.supervisor.removeProcessGroup(group_name):
            return RETURNCODE.OS_SUCCESS
    except xmlrpclib.Fault, e:
        logger.error('Could not remove process group \'{}\'! Error: {}'.format(group_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def get_all_config_info():
    """
        Remove application from supervisor_api context
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting all config info'.format(xml_rpc_address))
    try:
        return server.supervisor.getAllConfigInfo()
    except xmlrpclib.Fault, e:
        logger.error('Could not get all config info! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def get_config_info(app_name):
    """
        Remove application from supervisor_api context
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    logger.debug('SUPERVISOR XML-RPC({}): Requesting all config info'.format(xml_rpc_address))
    try:
        all_configs = server.supervisor.getAllConfigInfo()
        for config in all_configs:
            if 'group' in config:
                if config['group'] == app_name:
                    return config
        return None
    except xmlrpclib.Fault, e:
        logger.error('Could not get config info for API: {}! Error: {}'.format(app_name, e))
        return RETURNCODE.OS_ERROR
    except Exception, e:
        logger.error('Unknown error! Call the administrator! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR


def help_method(method_name):
    """
        Simple helper method to show the method's parameters and response values.
        Used purely for Development!
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    try:
        print server.system.methodHelp(method_name)
    except xmlrpclib.Fault, e:
        logger.warning('Received no result on given method! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    return RETURNCODE.OS_SUCCESS


def list_methods():
    """
        List all methods
    """
    server, xml_rpc_address = get_supervisor_xml_rpc_server()
    try:
        print server.system.listMethods()
    except xmlrpclib.Fault, e:
        logger.warning('Received no result on given method! Error: {}'.format(e))
        return RETURNCODE.OS_ERROR
    return RETURNCODE.OS_SUCCESS
