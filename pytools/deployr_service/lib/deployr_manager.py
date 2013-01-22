# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
from deployr_service.lib.deployr_api import DeployrApi
from deployr_service.lib.deployr_base import DeployrBase
from deployr_service.lib.errors import UnacceptableMessageException, InvalidTaskTypeException
from deployr_service.lib.returncodes import RETURNCODE
from deployr_service.lib.zmq_message_manager import ZmqMessageManager

class DeployrManager(DeployrBase):
    """Manages the Deployr life-cycle."""

    def __init__(self, config):
        """Setup ZmqMessageManager with callback method"""
        super(DeployrManager, self).__init__(config=config)
        self.zmq_message_manager = ZmqMessageManager(config=self.config, callback=self.process_incoming_request)
        self.deployr_api = DeployrApi(config=self.config)

    def process_incoming_request(self, message):
        """Process an incoming request from the ZMQ broker."""
        try:
            task = json.loads(message)
            status = self.deployr_api.execute_task(task)
            print ">>>>>>>> Status: {}".format(status)
            self.loggr.info("Executed task status: {}".format(status))
            return RETURNCODE.OS_SUCCESS
        except UnacceptableMessageException, e:
            self.loggr.error('Could not create task factory for spawning tasks! Error: {}'.format(e.message))
            return RETURNCODE.OS_ERROR
        except InvalidTaskTypeException, e:
            self.loggr.error(e.message)
            return RETURNCODE.OS_ERROR
        except AttributeError, e:
            self.loggr.error(e.message)
            return RETURNCODE.OS_ERROR

    def run(self):
        """Start the deployr daemon here."""
        try:
            self.show_all_settings()
            self.zmq_message_manager.run()
        except KeyboardInterrupt:
            logging.warning("CTRL-C pressed, closing down ...")
            self.zmq_message_manager.close()
