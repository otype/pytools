#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    deployr

    Copyright (c) 2012 apitrary

"""
import logging
import sys
import argparse
from deployr_service.config.logging_config import LOG_FORMAT
from deployr_service.globals.environments import ENVIRONMENT
from deployr_service.services import logging_service
from deployr_service.services.config_service import ConfigService


# Logger
logging.basicConfig(format=LOG_FORMAT)
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
    logger.info('Deployr mode: {}'.format(args.mode))
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
        "-M",
        "--mode",
        help="Deployr mode",
        type=str,
        choices=['deploy', 'balance'],
        default='deploy'
    )

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
    if args.mode == 'deploy':
        from deployr_service.deploy_mq_rx import start_consumer
#    elif args.mode == 'balance':
#        from lb_deployr.loadbalance_update_mq_rx import start_consumer
    else:
        from deployr_service.deploy_mq_rx import start_consumer

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
