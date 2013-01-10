# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from time import sleep
import zmq

def main():
    """ main method """

    context   = zmq.Context(1)
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5555")

    try:
        while True:
            # Write two messages, each with an envelope and content
            print "sending A"
            publisher.send_multipart(["loggr.INFO", "env_publisher", "localhost", "We don't want to see this"])
            print "sending B"
            publisher.send_multipart(["loggr.DEBUG", "env_publisher_sim", "localhost", "We would like to see this"])
            sleep(1.0)
    except KeyboardInterrupt:
        publisher.close()
        context.term()

if __name__ == "__main__":
    main()
