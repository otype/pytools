# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import options, logging
from tornado.options import define
from tornado.options import enable_pretty_logging
from zmq.eventloop import ioloop
from deployr_service.config.logging_config import LOGGING
from loggr_service.loggr_manager import LoggrManager
from loggr_service.settings import ZMQ
from loggr_service.settings import MONGODB
from loggr_service.settings import DEBUG


# Enable pretty logging
enable_pretty_logging()
## Logger
logging.basicConfig(format=LOGGING.LOG_FORMAT)
#logger = logging_service.get_logger()



def main():
    """
        Run all steps and config checks, then start the server
    """
    define("bind_address", default=ZMQ['LOGGR_CONNECT_ADDRESS'], help="Loggr's Connect address", type=str)
    define("topic", default=ZMQ['TOPIC'], help="Topic to subscribe", type=str)
    define("debug", default=DEBUG, help="Debugging flag", type=bool)
    define("db_host", default=MONGODB['HOST'], help="MongoDB host", type=str)

    # This needs to be done, first, before we do anything with tornado.
    ioloop.install()

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    topic = options.topic if options.topic else ""
    loggr = LoggrManager(
        publisher_endpoint=options.bind_address,
        topic=topic,
        mongodb_host=options.db_host,
        debug=options.debug
    )
    loggr.run()


if __name__ == "__main__":
    main()
