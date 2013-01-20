# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr_service.lib.deployr_base import DeployrBase
from lib.zeromq.majordomo_worker import MajorDomoWorker

class ZmqMessageManager(DeployrBase):

    def __init__(self, config, callback):
        super(ZmqMessageManager, self).__init__(config)
        self.callback = callback

    def setup_worker(self):
        """Setup the zmq worker"""
        self.worker = MajorDomoWorker(broker=self.deployr_broker, service=self.service_name, verbose=self.debug)

    def close(self):
        """Close the connection"""
        self.worker.destroy()

    def run(self):
        """Start the deployr daemon here."""
        self.setup_worker()

        reply = None
        status = None
        while True:
            request = self.worker.recv(reply)
            if request is None:
                break # Worker was interrupted
            reply = request
            status = self.callback(message=reply[0])
