# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:24 CET
    
    Copyright (c) 2012 apitrary

"""
import shutil
import sys
import os
from deployr_service.sortout.environment_config import GLOBAL_CONF
from deployr_service.sortout.environments import ENVIRONMENT
from deployr_service.lib.config_manager import ConfigManager


class ConfigService(object):
    """
        Deployr configuration service
    """

    @staticmethod
    def get_config_file_name():
        """
            Define the configuration file (and path)
        """
        if sys.platform == 'darwin':
            config_file = "{}/.deployr/deployr.conf".format(os.getenv("HOME"))
        elif sys.platform == 'linux2':
            config_file = "/etc/deployr/deployr.conf"
        else:
            config_file = "{}/.deployr/deployr.conf".format(os.getenv("HOME"))

        return config_file


    @staticmethod
    def load_configuration():
        """
            Loading configuration file
        """
        config = ConfigService.get_config_file_name()
        config_manager = ConfigManager(config)
        config_manager.setup_config_dir()

        if not os.path.exists(config):
            config_manager.load_config(config_obj=GLOBAL_CONF[ENVIRONMENT.DEV])
            config_manager.write_config()

        config_manager.load_config_from_file()
        return config_manager.config


    @staticmethod
    def write_configuration(config_env):
        """
            Write the configuration file for the given environment
        """
        config = ConfigService.get_config_file_name()
        # Store existing config to <name>.backup
        if os.path.exists(config):
            shutil.move(config, "{}.backup".format(config))

        config_manager = ConfigManager(config)
        config_manager.setup_config_dir()
        config_manager.load_config(config_obj=GLOBAL_CONF[config_env])
        config_manager.write_config()

