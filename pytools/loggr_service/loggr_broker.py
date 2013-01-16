# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import define
from tornado.options import enable_pretty_logging
from tornado.options import options
from lib.zeromq.majordomo_broker import MajorDomoBroker
from loggr_service.settings import ZMQ
from loggr_service.settings import DEBUG

enable_pretty_logging()

def main():
    """
        Create and start new Loggr broker
    """
    define("bind_address", default=ZMQ['LOGGR_BROKER_BIND_ADDRESS'], help="Loggr's Connect address", type=str)
    define("debug", default=DEBUG, help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    broker = MajorDomoBroker(options.debug)
    broker.bind(ZMQ['LOGGR_BROKER_BIND_ADDRESS'])
    broker.mediate()

if __name__ == '__main__':
    main()