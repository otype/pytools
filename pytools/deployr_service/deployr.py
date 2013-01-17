# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import enable_pretty_logging, define, options, logging
from deployr_service.lib.deployr_manager import DeployrManager
from deployr_service.services.config_service import ConfigService

enable_pretty_logging()

def main():
    """
        Start the Tornado Web server
    """
    define("write_config", default=False, help="Write config files (overwrites existing)", type=bool)
    define("env", default="dev", help="Environment: (dev|staging|live)", type=str)
    define("loggr_broker", default="tcp://localhost:5555", help="Loggr ZMQ (broker) address", type=str)
    define("deployr_broker", default="tcp://localhost:5557", help="Deployr ZMQ (broker) address", type=str)
    define("debug", default=False, help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    if options.write_config:
        ConfigService.write_configuration(options.env)
        logging.info("Configuration file written! Now, edit config file and start deployr!")
        sys.exit(0)

    config = ConfigService.load_configuration()
    deployr_manager = DeployrManager(config)
    deployr_manager.run()


# MAIN
#
#
if __name__ == "__main__":
    main()
