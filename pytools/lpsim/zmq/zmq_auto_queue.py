# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
from zmq.devices import monitored_queue

print("Starting queue ...")
ctx = zmq.Context(1)

ins = ctx.socket(zmq.ROUTER)
outs = ctx.socket(zmq.DEALER)
mons = ctx.socket(zmq.PUB)
ins.bind("tcp://*:5555") # For clients
outs.bind("tcp://*:5556")  # For workers
mons.bind("tcp://*:5557")  # For monitors
#configure_sockets(ins,outs,mons)
monitored_queue(ins, outs, mons, in_prefix='in', out_prefix='out')