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

ctx = zmq.Context(1)

s = ctx.socket(zmq.REP)
s.bind('tcp://*:5555')
stream = ZMQStream(s)
def echo2(msg):
    print msg
    stream.send_multipart(msg)
stream.on_recv(echo2)

s1 = ctx.socket(zmq.REP)
s1.bind('tcp://*:5556')
stream1 = ZMQStream(s1)

s2 = ctx.socket(zmq.REP)
s2.bind('tcp://*:5557')
stream2 = ZMQStream(s2)

def echo(msg, stream):
    print msg
    stream.send_multipart(msg)

stream1.on_recv_stream(echo)
stream2.on_recv_stream(echo)

ioloop.IOLoop.instance().start()