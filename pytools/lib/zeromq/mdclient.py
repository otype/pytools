# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
from tornado.options import define, options, logging
from zmq.eventloop import ioloop
from lib.zeromq.majordomo_client import MajorDomoClient

class LoggrClient(object):
    def __init__(self, zmq_connect_address="tcp://localhost:5555", verbose=False):
        super(LoggrClient, self).__init__()
        self.zmq_connect_address = zmq_connect_address
        self.verbose = verbose
        self.message_counter = 0
        self.connect()

    def connect(self):
        self.client = MajorDomoClient(self.zmq_connect_address, verbose=self.verbose)

    def zlog(self, service, message):
        self.client.send(service=service, request=message)
        self.message_counter += 1
        self.flush_queue()

    def flush_queue(self):
        print "flushing queue"
        count = 0
        while count < self.message_counter:
            try:
                reply = self.client.recv()
            except KeyboardInterrupt:
                break
            else:
                # also break on failure to reply:
                if reply is None:
                    break
            count += 1
        print "%i requests/replies processed" % count


def main():
    define("loggr_broker", default="tcp://localhost:5555", help="Loggr's broker address", type=str)
    define("verbose", default=False, help="verbose", type=bool)
    define("debug", default=False, help="Debugging flag", type=bool)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    loggr = LoggrClient(zmq_connect_address=options.loggr_broker)
    loggr.zlog('some_service', 'a nice message')

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.warning("CTRL-C pressed, closing down ...")
        ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    main()