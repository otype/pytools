# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 00:09 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import logging
import socket
import xmlrpclib
from pydeployr.conf.returncodes import RETURNCODE


class SupervisorXmlRpcService(object):
    """
        API for the Supervisor XML-RPC server.
    """

    def __init__(self, supervisord_xml_rpc_server):
        self.supervisord_xml_rpc_server = supervisord_xml_rpc_server
        self.server = xmlrpclib.Server(self.supervisord_xml_rpc_server)

    def reload_config(self):
        """
            Reread the supervisor_api configuration files
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting reload of all configs'.format(self.supervisord_xml_rpc_server)
        )
        try:
            self.server.supervisor.reloadConfig()
        except xmlrpclib.Fault, e:
            logging.error('Could not reload config! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        except socket.error, e:
            logging.error('Socket error: {}'.format(e.message))
            return RETURNCODE.OS_ERROR
        return RETURNCODE.OS_SUCCESS

    def start(self, app_name):
        """
            Start given application via supervisor_api
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting start of application: {}'.format(self.supervisord_xml_rpc_server,
                                                                                 app_name)
        )
        try:
            if self.server.supervisor.startProcess(app_name):
                return RETURNCODE.OS_SUCCESS
        except xmlrpclib.Fault, e:
            logging.error('Could not start process \'{}\'! Error: {}'.format(app_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def stop(self, app_name):
        """
            Stop given application via supervisor_api
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting stop of application: {}'.format(self.supervisord_xml_rpc_server,
                                                                                app_name))
        try:
            if self.server.supervisor.stopProcess(app_name):
                return RETURNCODE.OS_SUCCESS
        except xmlrpclib.Fault, e:
            logging.error('Could not stop process \'{}\'! Error: {}'.format(app_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def restart(self, app_name):
        """
            Start given application via supervisor_api
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting restart of application: {}'.format(self.supervisord_xml_rpc_server,
                                                                                   app_name))

        stop_state = self.stop(app_name)
        start_state = self.start(app_name)

        if (stop_state + start_state) > RETURNCODE.OS_SUCCESS:
            logging.error('Could not restart process \'{}\'!'.format(app_name))
            return RETURNCODE.OS_ERROR

        return RETURNCODE.OS_SUCCESS

    def add_group(self, group_name):
        """
            Add new application to supervisor_api configuration
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting addition of application: {}'.format(self.supervisord_xml_rpc_server,
                                                                                    group_name))
        try:
            if self.server.supervisor.addProcessGroup(group_name):
                return RETURNCODE.OS_SUCCESS
        except xmlrpclib.Fault, e:
            logging.error('Could not add process group \'{}\'! Error: {}'.format(group_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def status(self):
        """
            Request status of given application
        """
        logging.debug('SUPERVISOR XML-RPC({}): Requesting status'.format(self.supervisord_xml_rpc_server))
        try:
            response = self.server.supervisor.getState()
            if 'statename' in response:
                if response['statename'] == 'RUNNING':
                    logging.debug('SUPERVISOR XML-RPC({}): Status \'{}\''.format(response['statename']))
                    return RETURNCODE.OS_SUCCESS
            return RETURNCODE.OS_ERROR
        except xmlrpclib.Fault, e:
            logging.error('Could not get status! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def get_all_process_info(self):
        """
            Request status of given application
        """
        logging.debug('SUPERVISOR XML-RPC({}): Requesting all process info'.format(self.supervisord_xml_rpc_server))
        try:
            return self.server.supervisor.getAllProcessInfo()
        except xmlrpclib.Fault, e:
            logging.error('Could not get all process info! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def get_process_info(self, app_name):
        """
            Request status of given application
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting process info for api_id: {}'.format(self.supervisord_xml_rpc_server,
                                                                                    app_name))
        try:
            all_processes = self.server.supervisor.getAllProcessInfo()
            for process in all_processes:
                if 'name' in process:
                    if process['name'] == app_name:
                        return process
            return None
        except xmlrpclib.Fault, e:
            logging.error('Could not get the process info for: {}! Error: {}'.format(app_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def remove_group(self, group_name):
        """
            Remove application from supervisor_api context
        """
        logging.debug(
            'SUPERVISOR XML-RPC({}): Requesting removal of group: {}'.format(self.supervisord_xml_rpc_server,
                                                                             group_name))
        try:
            if self.server.supervisor.removeProcessGroup(group_name):
                return RETURNCODE.OS_SUCCESS
        except xmlrpclib.Fault, e:
            logging.error('Could not remove process group \'{}\'! Error: {}'.format(group_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def get_all_config_info(self):
        """
            Remove application from supervisor_api context
        """
        logging.debug('SUPERVISOR XML-RPC({}): Requesting all config info'.format(self.supervisord_xml_rpc_server))
        try:
            return self.server.supervisor.getAllConfigInfo()
        except xmlrpclib.Fault, e:
            logging.error('Could not get all config info! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def get_config_info(self, app_name):
        """
            Remove application from supervisor_api context
        """
        logging.debug('SUPERVISOR XML-RPC({}): Requesting all config info'.format(self.supervisord_xml_rpc_server))
        try:
            all_configs = self.server.supervisor.getAllConfigInfo()
            for config in all_configs:
                if 'group' in config:
                    if config['group'] == app_name:
                        return config
            return None
        except xmlrpclib.Fault, e:
            logging.error('Could not get config info for API: {}! Error: {}'.format(app_name, e))
            return RETURNCODE.OS_ERROR
        except Exception, e:
            logging.error('Unknown error! Call the administrator! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR

    def help_method(self, method_name):
        """
            Simple helper method to show the method's parameters and response values.
            Used purely for Development!
        """
        try:
            print self.server.system.methodHelp(method_name)
        except xmlrpclib.Fault, e:
            logging.warning('Received no result on given method! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        return RETURNCODE.OS_SUCCESS

    def list_methods(self):
        """
            List all methods
        """
        try:
            print self.server.system.listMethods()
        except xmlrpclib.Fault, e:
            logging.warning('Received no result on given method! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        return RETURNCODE.OS_SUCCESS
