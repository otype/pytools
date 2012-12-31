# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq

def main():
    """ main method """

    context = zmq.Context(1)
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt(zmq.SUBSCRIBE, "B")

    poller = zmq.Poller()
    poller.register(subscriber, zmq.POLLIN)

    try:
        while True:
            socks = dict(poller.poll(timeout=300))

            if subscriber in socks and socks[subscriber] == zmq.POLLIN:
                # Read envelope with address
                [address, contents] = subscriber.recv_multipart()
                print("[%s] %s\n" % (address, contents))

            print "not received"
    except KeyboardInterrupt:
        subscriber.close()
        context.term()

if __name__ == "__main__":
    main()