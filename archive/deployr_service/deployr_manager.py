# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging

from pika import exceptions
import pika
from deployr_service.deployr_base import DeployrBase

from deployr_service.deployr_api import DeployrApi
from archive.deployr_service.lib.errors import UnacceptableMessage
from archive.deployr_service.lib.errors import InvalidTaskType
from archive.deployr_service.lib.returncodes import RETURNCODE
from archive.deployr_service.lib.rmq_base_rpc_async_consumer import RmqBaseRpcAsyncConsumer


class DeployrManager(DeployrBase):
    """
        Manages the Deployr life-cycle.
    """

    def __init__(self, config):
        """
            Setup MessageManager with callback method
        """
        super(DeployrManager, self).__init__(config=config)
        self.amqp_url = str('amqp://{username}:{password}@{broker_host}:{broker_port}/%2F'.format(
            username=self.rmq_broker_username,
            password=self.rmq_broker_password,
            broker_host=self.rmq_broker_host,
            broker_port=self.rmq_broker_port
        ))
        self.deployr_api = DeployrApi(config=self.config)

    def setup_worker(self):
        """
            Setup RabbitMQ worker
        """
        self.worker = RmqBaseRpcAsyncConsumer(
            amqp_url=self.amqp_url,
            queue='deployr_rpc',
            callback=self.process_incoming_request
        )

    def process_incoming_request(self, message):
        """
            Process an incoming request from the ZMQ broker.
        """
        try:
            task = json.loads(message)
            status_set = self.deployr_api.execute_task(task)

            if type(status_set) == json:
                status = status_set.to_dict()
            elif type(status_set) == dict:
                status = status_set
            else:
                status = str(status_set)

            self.loggr.info("Executed task status: {}".format(status))
            return status_set
        except UnacceptableMessage, e:
            self.loggr.error('Could not create task factory for spawning tasks! Error: {}'.format(e.message))
            return RETURNCODE.OS_ERROR
        except InvalidTaskType, e:
            self.loggr.error(e.message)
            return RETURNCODE.OS_ERROR
        except AttributeError, e:
            self.loggr.error(e.message)
            return RETURNCODE.OS_ERROR

    def run(self):
        """
            Start the deployr daemon here.
        """
        try:
            self.show_all_settings()
            self.setup_worker()
            self.worker.run()
        except KeyboardInterrupt:
            logging.warning("CTRL-C pressed, closing down ...")
            self.worker.stop()
        except pika.exceptions.AMQPConnectionError, e:
            logging.error(e)
