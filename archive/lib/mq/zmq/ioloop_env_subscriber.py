# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

ioloop.install()

context = zmq.Context(1)
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5555")

subscriber.setsockopt(zmq.SUBSCRIBE, "")        # Subscribe to all
#subscriber.setsockopt(zmq.SUBSCRIBE, "B")      # Subscribe to "B"


def echo(msg):
    [address, contents] = msg
    print("[%s] %s\n" % (address, contents))


def main():
    """ main method """
    stream = ZMQStream(subscriber)
    stream.on_recv(echo)

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        subscriber.close()
        context.term()
        ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    main()
