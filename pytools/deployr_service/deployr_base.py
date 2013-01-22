# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from loggr_service.loggr_client import LoggrClient

class DeployrBase(object):
    """
        Deployr base object. Used for configurations.
    """

    def __init__(self, config):
        """
            Transfer configuration object into this class.
        """
        super(DeployrBase, self).__init__()
        self.config = config
        self.read_config()
        self.setup_loggr()

    def get(self, name):
        """
            Get a single variable from the config object
        """
        if name in self.config:
            return self.config[name]
        else:
            logging.error("Config variable:{} does not exist.".format(name))
            return ''

    def read_config(self):
        """
            Read out the config object
        """
        self.loggr_broker = self.get('LOGGR_BROKER_ADDRESS')
        self.supervisord_host = self.get("SUPERVISORD_HOST")
        self.supervisord_web_port = self.get("SUPERVISORD_WEB_PORT")
        self.supervisord_xml_rpc_username = self.get("SUPERVISOR_XML_RPC_USERNAME")
        self.supervisord_xml_rpc_password = self.get("SUPERVISOR_XML_RPC_PASSWORD")
        self.supervisord_xml_rpc_server = self.get("SUPERVISOR_XML_RPC_SERVER_ADDRESS")
        self.loggr_broker = self.get("LOGGR_BROKER_ADDRESS")
        self.deployr_broker = self.get("DEPLOYR_BROKER_ADDRESS")
        self.logging_level = self.get("LOGGING")
        self.environment = self.get("ENV")
        self.config_file = self.get("DEPLOYR_CONFIG_FILE")
        self.service_name = self.get("SERVICE")
        self.debug = True if self.get("DEBUG") == "1" or self.get("DEBUG") == True else False

    def show_all_settings(self):
        """
            Show all configured constants
        """
        logging.info('Starting service: deployr')
        logging.info('Deployr Broker: {}'.format(self.deployr_broker))
        logging.info('Loggr Broker: {}'.format(self.loggr_broker))
        logging.info('Environment: {}'.format(self.environment))
        logging.info('Logging: {}'.format(self.logging_level))
        logging.info('Config file: {}'.format(self.config_file))
        logging.info('Service: {}'.format(self.service_name))
        logging.info('Debug: {}'.format("ON" if self.debug == True else "OFF"))
        logging.info('Supervisor host: {}'.format(self.supervisord_host))
        logging.info('Supervisor web port: {}'.format(self.supervisord_web_port))
        logging.info('Supervisor XML-RPC Server address: {}'.format(self.supervisord_xml_rpc_server))
        logging.info('Supervisor XML-RPC Server user: {}'.format(self.supervisord_xml_rpc_username))


        self.loggr.info("deployr.start[broker:{broker}, loggr:{loggr}, env:{env}, debug:{debug}]".format(
            broker=self.deployr_broker,
            loggr=self.loggr_broker,
            env=self.environment,
            debug=self.debug
        ))

    def setup_loggr(self):
        self.loggr = LoggrClient(
            loggr_broker=self.loggr_broker,
            daemon_name=self.service_name,
            service_name=self.service_name,
            verbose=self.debug
        )
