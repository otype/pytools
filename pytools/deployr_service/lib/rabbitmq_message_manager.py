# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr_service.deployr_base import DeployrBase
from lib.rabbitmq.rabbitmq_worker import RabbitMqWorker

class RabbitMqMessageManager(DeployrBase):
    """RabbitMQ message manager"""

    deployment_queue = 'genapi_deployment'

    def __init__(self, config, callback):
        super(RabbitMqMessageManager, self).__init__(config)
        self.callback = callback

    def setup_worker(self):
        """Setup RabbitMQ worker"""
        self.worker = RabbitMqWorker(
            broker_host=self.rmq_broker_host,
            broker_port=self.rmq_broker_port,
            username=self.rmq_broker_username,
            password=self.rmq_broker_password,
            queue=self.deployment_queue,
            activate_prefetch=self.rmq_broker_prefetch_count,
            callback=self.callback
        )

    def close(self):
        if self.worker:
            self.worker.disconnect()

    def run(self):
        if self.worker:
            self.worker.run()

