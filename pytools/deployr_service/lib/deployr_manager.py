# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from deployr_service.lib.deployr_base import DeployrBase
from deployr_service.sortout.environments import RETURNCODE
from deployr_service.lib.errors import UnacceptableMessageException, InvalidTaskTypeException
from deployr_service.lib.task_factory import TaskFactory
from lib.zeromq.majordomo_worker import MajorDomoWorker

class DeployrManager(DeployrBase):
    """
        Manages the Deployr life-cycle.
    """

    def __init__(self, config):
        """
            Init DeployrManager
        """
        super(DeployrManager, self).__init__(config=config)

    def setup_worker(self):
        """
            Setup the zmq subscriber and connect to publisher
        """
        self.worker = MajorDomoWorker(
            broker=self.deployr_broker,
            service=self.service_name,
            verbose=self.debug
        )

    def close(self):
        """
            Close the connection
        """
        self.worker.destroy()

    def process_incoming_request(self, message):
        """
            Process an incoming request from the ZMQ broker.
        """
        status = self.run_task(message)
        if status == RETURNCODE.OS_SUCCESS:
            self.loggr.debug('Acknowledging received message.')
        else:
            self.loggr.error('Error running task!')

    def run_task(self, message):
        """
            Run the task from the given message
        """
        try:            
            task_factory = TaskFactory()
            task_factory.load_message(message)
            task = task_factory.get_task()
    
            self.loggr.info('Running task: {}'.format(task_factory.message))
            status = task.run()
            self.loggr.info('Task status: {}'.format(status))
    
            # Send out the confirmation message
            self.loggr.info('Confirming task execution for API: {}'.format(task.api_id))
            task.send_confirmation()
    
            return RETURNCODE.OS_SUCCESS
        except UnacceptableMessageException, e:
            self.loggr.error('Could not create task factory for spawning tasks! Error: {}'.format(e))
            return RETURNCODE.OS_ERROR
        except InvalidTaskTypeException, e:
            self.loggr.error(e)
            return RETURNCODE.OS_ERROR
        except AttributeError, e:
            self.loggr.error(e)
            return RETURNCODE.OS_ERROR

    def run(self):
        """
            Start the deployr daemon here.
        """
        self.show_all_settings()
        self.setup_worker()

        try:
            reply = None
            while True:
                request = self.worker.recv(reply)
                if request is None:
                    break # Worker was interrupted
                reply = request
                self.process_incoming_request(message=reply[0])
        except KeyboardInterrupt:
            logging.warning("CTRL-C pressed, closing down ...")
            self.close()
