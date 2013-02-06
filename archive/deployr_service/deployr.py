# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import enable_pretty_logging, define, options, logging
from archive.deployr_service.deployr_manager import DeployrManager
from archive.deployr_service.services import config_service

enable_pretty_logging()

def main():
    """
        Start the Tornado Web server
    """
    define("write_config", default=False, help="Write config files (overwrites existing)", type=bool)
    define("env", help="Environment: (dev|staging|live)", type=str)
    define("loggr_broker", help="Loggr ZMQ (broker) address", type=str)
    define("deployr_broker", help="Deployr broker address", type=str)
    define("rmq_host", help="RabbitMQ broker host", type=str)
    define("rmq_port", help="RabbitMQ broker port", type=str)
    define("rmq_username", help="RabbitMQ broker username", type=str)
    define("rmq_password", help="RabbitMQ broker password", type=str)
    define("debug", help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    if options.write_config:
        config_service.write_configuration(options.env)
        logging.info("Configuration file written! Now, edit config file and start deployr!")
        sys.exit(0)

    config = config_service.load_configuration()
    if options.env:
        config['ENV'] = options.env
    if options.loggr_broker:
        config['LOGGR_BROKER_ADDRESS'] = options.loggr_broker
    if options.deployr_broker:
        config['DEPLOYR_BROKER_ADDRESS'] = options.deployr_broker
    if options.rmq_host:
        config['BROKER_HOST'] = options.rmq_host
    if options.rmq_port:
        config['BROKER_PORT'] = options.rmq_port
    if options.rmq_username:
        config['BROKER_USER'] = options.rmq_username
    if options.rmq_password:
        config['BROKER_PASSWORD'] = options.rmq_password
    if options.debug:
        config['DEBUG'] = options.debug

    deployr_manager = DeployrManager(config=config)
    deployr_manager.run()


if __name__ == "__main__":
    main()
