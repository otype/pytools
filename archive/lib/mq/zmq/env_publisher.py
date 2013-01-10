# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
from time import sleep
import datetime
import sys
import zmq

def main():
    """ main method """

    context   = zmq.Context(1)
    publisher = context.socket(zmq.DEALER)
#    publisher.bind("tcp://*:5555")
#    publisher = context.socket(zmq.REQ)
    publisher.connect("tcp://localhost:5555")

    if len(sys.argv) <= 1:
        sender = "DEFAULT_MESSAGE"
    else:
        sender = sys.argv[1]

    try:
        while True:
            # Write two messages, each with an envelope and content
            print "sending {}".format(sender)
#            publisher.send_multipart(["INFO", str(datetime.datetime.utcnow()), sender, "localhost", "{} has sent a message".format(sender)])

            message = {
                "level": "INFO",
                "incident_time": str(datetime.datetime.utcnow()),
                "service": sender,
                "host": "localhost",
                "message": "{} has sent a message".format(sender)
            }

            publisher.send("", zmq.SNDMORE)
            publisher.send(json.dumps(message))
            print(publisher.recv())
            sleep(1.0)
    except KeyboardInterrupt:
        publisher.close()
        context.term()

if __name__ == "__main__":
    main()
