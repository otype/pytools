# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado

from loggr_service.loggr import Loggr
from tornado.options import options
from tornado.options import define
from tornado.options import enable_pretty_logging
from zmq.eventloop import ioloop

# Enable pretty logging
enable_pretty_logging()


def main():
    """
        Run all steps and config checks, then start the server
    """
    define("endpoint", default="tcp://localhost:5555", help="Publisher's address", type=str)
    define("topic", default="", help="Topic to subscribe", type=str)
    define("debug", default=False, help="Debugging flag", type=bool)
    define("db_host", default="127.0.0.1", help="MongoDB host", type=str)

    # This needs to be done, first, before we do anything with tornado.
    ioloop.install()

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    topic = options.topic if options.topic else ""
    loggr = Loggr(
        publisher_endpoint=options.endpoint,
        topic=topic,
        mongodb_host=options.db_host,
        debug=options.debug
    )
    loggr.run()


if __name__ == "__main__":
    main()
