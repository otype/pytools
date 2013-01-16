# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import options
from tornado.options import define
from tornado.options import enable_pretty_logging
from loggr_service.loggr_manager import LoggrManager
from loggr_service.settings import ZMQ
from loggr_service.settings import MONGODB
from loggr_service.settings import DEBUG


enable_pretty_logging()

def main():
    """
        Run all steps and config checks, then start the server
    """
    define("bind_address", default=ZMQ['LOGGR_CONNECT_ADDRESS'], help="Loggr's Connect address", type=str)
    define("service", default=ZMQ['SERVICE'], help="Broker Service name", type=str)
    define("debug", default=DEBUG, help="Debugging flag", type=bool)
    define("db_host", default=MONGODB['HOST'], help="MongoDB host", type=str)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    loggr = LoggrManager(
        publisher_endpoint=options.bind_address,
        mongodb_host=options.db_host,
        service_name=options.service,
        debug=options.debug
    )
    loggr.run()


if __name__ == "__main__":
    main()
