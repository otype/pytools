#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
import sys
import argparse

from tornado.options import logging
from deployr_service.config.logging_config import LOGGING
from deployr_service.deploy_mq_rx import start_consumer
from deployr_service.globals.environments import ENVIRONMENT
from deployr_service.services import logging_service
from deployr_service.services.config_service import ConfigService


#enable_pretty_logging()
## Logger
logging.basicConfig(format=LOGGING.LOG_FORMAT)
logger = logging_service.get_logger()

##############################################################################
#
# FUNCTIONS
#
##############################################################################


def show_all_settings(config):
    """
        Show all configured constants
    """
    logger.info('Starting service: deployr')
    logger.info('Remote Broker: {}:{}'.format(config['BROKER_HOST'], config['BROKER_PORT']))
    logger.info('Environment: {}'.format(config['NAME']))

    config_to_show = ConfigService.strip_out_sensitive_data(config)
    logger.info('Configuration: {}'.format(config_to_show))
    logger.info('Logging level: {}'.format(config['LOGGING']))


def parse_shell_args():
    """
        Parse the shell arguments
    """
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-w",
        "--write_config",
        help="Write the configuration file",
        type=str,
        choices=[ENVIRONMENT.DEV, ENVIRONMENT.LIVE]
    )

    args = parser.parse_args()


def check_for_config_write():
    """
        Write configuration file if called via shell param
    """
    config_env = args.write_config
    ConfigService.write_configuration(config_env)
    logger.info("Configuration file written! Now, edit config file and start deployr!")
    sys.exit(0)


def main():
    """
        Start the Tornado Web server
    """
#    define("loggr", default=ZMQ['LOGGR_CONNECT_ADDRESS'], help="Publisher's address", type=str)
#    define("endpoint", default=ZMQ['DEPLOYR_BIND_ADDRESS'], help="Publisher's address", type=str)
#    define("topic", default=ZMQ['TOPIC'], help="Topic to subscribe", type=str)
#    define("debug", default=DEBUG, help="Debugging flag", type=bool)
#    define("db_host", default=MONGODB['HOST'], help="MongoDB host", type=str)
#
#    # This needs to be done, first, before we do anything with tornado.
#    ioloop.install()
#
#    try:
#        tornado.options.parse_command_line()
#    except tornado.options.Error, e:
#        sys.exit('ERROR: {}'.format(e))
#
#    topic = options.topic if options.topic else ""
#    loggr = LoggrManager(
#        publisher_endpoint=options.endpoint,
#        topic=topic,
#        mongodb_host=options.db_host,
#        debug=options.debug
#    )
#    loggr.run()

    # Parse the shell arguments, first.
    parse_shell_args()

    # Check if config write has been requested. If yes, bail out afterwards.
    if args.write_config:
        check_for_config_write()

    # Load configuration
    config = ConfigService.load_configuration()

    # Show all configured handlers
    show_all_settings(config)

    # start the MQ consumer
    start_consumer(
        broker_host=config['BROKER_HOST'],
        broker_port=int(config['BROKER_PORT']),
        username=config['BROKER_USER'],
        password=config['BROKER_PASSWORD'],
        activate_prefetch=config['BROKER_PREFETCH_COUNT']
    )

##############################################################################
#
# MAIN
#
##############################################################################

if __name__ == '__main__':
    main()
