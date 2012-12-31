# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 15:42 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
import time
from random import randint
from lib.mq.zeromq.zeromq_config import HEARTBEAT_LIVENESS
from lib.mq.zeromq.zeromq_config import HEARTBEAT_INTERVAL
from lib.mq.zeromq.zeromq_config import INTERVAL_INIT
from lib.mq.zeromq.zeromq_config import INTERVAL_MAX
from lib.mq.zeromq.zeromq_config import PPP_READY
from lib.mq.zeromq.zeromq_config import PPP_HEARTBEAT


def worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    worker = context.socket(zmq.DEALER) # DEALER
    identity = "%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect("tcp://localhost:5556")
    worker.send(PPP_READY)
    return worker

context = zmq.Context(1)
poller = zmq.Poller()

liveness = HEARTBEAT_LIVENESS
interval = INTERVAL_INIT
heartbeat_at = time.time() + HEARTBEAT_INTERVAL

worker = worker_socket(context, poller)
count = 0
while True:
    socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))
    if socks.get(worker) == zmq.POLLIN:
        #  Get message
        #  - 3-part envelope + content -> request
        #  - 1-part HEARTBEAT -> heartbeat
        frames = worker.recv_multipart()
        if not frames:
            break # Interrupted

        if len(frames) == 3:
            count += 1
            print "I: ({}) Message: {}".format(count, frames[2])
            worker.send_multipart(frames)
            liveness = HEARTBEAT_LIVENESS
            time.sleep(1)  # Do some heavy work
        elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
            print "I: Queue heartbeat: {}".format(time.time())
            liveness = HEARTBEAT_LIVENESS
        else:
            print "E: Invalid message: %s" % frames
        interval = INTERVAL_INIT
    else:
        liveness -= 1
        if liveness == 0:
            print "W: Heartbeat failure, can't reach queue"
            print "W: Reconnecting in %0.2fs…" % interval
            time.sleep(interval)

            if interval < INTERVAL_MAX:
                interval *= 2
            poller.unregister(worker)
            worker.setsockopt(zmq.LINGER, 0)
            worker.close()
            worker = worker_socket(context, poller)
            liveness = HEARTBEAT_LIVENESS
            count = 0

    if time.time() > heartbeat_at:
        heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        print "I: Worker heartbeat"
        worker.send(PPP_HEARTBEAT)