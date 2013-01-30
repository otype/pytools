# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
import sys
from deployr_service.deployr_base import DeployrBase
from deployr_service.lib.returncodes import RETURNCODE
from deployr_service.services import os_service


class SuperVisorCtlService(DeployrBase):
    SUPERVISORCTL_CONFIG = {
        'START': 'start',
        'STOP': 'stop',
        'RESTART': 'restart',
        'ADD': 'add',
        'REMOVE': 'remove',
        'STATUS': 'status',
        'REREAD': 'reread'
    }

    def __init__(self, config):
        super(SuperVisorCtlService, self).__init__(config)

    def get_supervisorctl_executable(self):
        """The executable for calling supervisorctl"""
        if sys.platform == 'darwin':
            # Do nothing! Mac ain't got no supervisor! We are just faking it here.
            return 'supervisorctl'
        elif sys.platform == 'linux2':
            return '/usr/bin/supervisorctl'
        else:
            return 'supervisorctl'

    def parse_supervisorctl_params(self, params):
        """
            subprocess.call is a bit picky with the argument list. For this, we need
            to make sure that we don't pass in empty strings and we don't pass in strings
            with whitespaces.

            Make a few checks on the params list:
                - if it's a string as csv, run split() on it and strip() all elements
                - if it's a list, strip all elements

            Otherwise just return the params back.
        """
        if type(params) == str:
            return [element.strip() for element in params.split(',')]

        if type(params) == list:
            return [element.strip() for element in params]

        return params

    def run_supervisorctl_command(self, command, params=None):
        """Reread the supervisor_api configuration files"""
        if command is None:
            self.loggr.error('Missing supervisorctl command as parameter!')
            return RETURNCODE.OS_INVALID_ARGUMENT

        # all supervisorctl commands are lower case ... just in case:
        command = command.lower().split()

        # check if command is an acceptable one ...
        if command[0].upper() not in self.SUPERVISORCTL_CONFIG.keys():
            self.loggr.error('Unknown supervisorctl command: {}'.format(command))
            return RETURNCODE.OS_CANNOT_INVOKE_COMMAND_ERROR

        if params:
            checked_params = self.parse_supervisorctl_params(params)
            self.loggr.debug('Adding command params: {}'.format(checked_params))
            command += checked_params

        self.loggr.debug('Running supervisorctl command: {}'.format(command))
        return os_service.execute_shell_command([self.get_supervisorctl_executable()] + command)

    def supervisorctl_reread(self):
        """Reread the supervisor_api configuration files"""
        self.loggr.debug('SUPERVISORCTL: Reread the supervisor_api configurations files')
        return self.run_supervisorctl_command('REREAD')

    def supervisorctl_start(self, app_name):
        """Start given application via supervisor_api"""
        self.loggr.debug('SUPERVISORCTL: Requesting start of application: {}'.format(app_name))
        return self.run_supervisorctl_command('START', app_name)

    def supervisorctl_stop(self, app_name):
        """Stop given application via supervisor_api"""
        self.loggr.debug('SUPERVISORCTL: Requesting stop of application: {}'.format(app_name))
        return self.run_supervisorctl_command('STOP', app_name)

    def supervisorctl_restart(self, app_name):
        """Start given application via supervisor_api"""
        self.loggr.debug('SUPERVISORCTL: Requesting restart of application: {}'.format(app_name))
        return self.run_supervisorctl_command('RESTART', app_name)

    def supervisorctl_add(self, app_name):
        """Add new application to supervisor_api configuration"""
        self.loggr.debug('SUPERVISORCTL: Requesting addition of application: {}'.format(app_name))
        return self.run_supervisorctl_command('ADD', app_name)

    def supervisorctl_status(self, app_name):
        """Request status of given application"""
        self.loggr.debug('SUPERVISORCTL: Requesting status of application: {}'.format(app_name))
        return self.run_supervisorctl_command('STATUS', app_name)

    def supervisorctl_remove(self, app_name):
        """Remove application from supervisor_api context"""
        self.loggr.debug('SUPERVISORCTL: Requesting removal of application: {}'.format(app_name))
        return self.run_supervisorctl_command('REMOVE', app_name)
