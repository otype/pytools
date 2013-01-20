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

enable_pretty_logging()

def main():
    """
        Create and start new Loggr broker
    """
    define("bind_address", default="tcp://*:5555", help="Loggr's Connect address", type=str)
    define("debug", default=False, help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    broker = MajorDomoBroker(options.debug)
    broker.bind(options.bind_address)
    broker.mediate()

if __name__ == '__main__':
    main()