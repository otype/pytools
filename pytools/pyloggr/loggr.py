# -*- coding: utf-8 -*-
"""

    loggr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import sys
import tornado
from tornado.options import options
from tornado.options import define
from tornado.log import enable_pretty_logging
from pyloggr.loggr_manager import LoggrManager

enable_pretty_logging()

def main():
    """
        Run all steps and config checks, then start the server
    """
    define("loggr_broker", default="tcp://localhost:5555", help="Loggr ZMQ (broker) address", type=str)
    define("mongodb_host", default='127.0.0.1', help="MongoDB host", type=str)
    define("service", default='loggr', help="Broker Service name", type=str)
    define("debug", default=False, help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    loggr = LoggrManager(
        loggr_broker=options.loggr_broker,
        mongodb_host=options.mongodb_host,
        service_name=options.service,
        debug=options.debug
    )
    loggr.run()


# MAIN
#
#
if __name__ == "__main__":
    main()
