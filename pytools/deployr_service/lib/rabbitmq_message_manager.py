# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from tornado.options import enable_pretty_logging, logging
from deployr_service.deployr_base import DeployrBase
from deployr_service.services.config_service import ConfigService
from lib.rabbitmq.rabbitmq_base_async_consumer import RabbitMqBaseAsyncConsumer

enable_pretty_logging()

class RabbitMqMessageManager(DeployrBase):
    """RabbitMQ message manager"""

    def __init__(self, config, callback, amqp_url=None):
        super(RabbitMqMessageManager, self).__init__(config)
        self.callback = callback

        self.amqp_url = str('amqp://{username}:{password}@{broker_host}:{broker_port}/%2F'.format(
            username=self.rmq_broker_username,
            password=self.rmq_broker_password,
            broker_host=self.rmq_broker_host,
            broker_port=self.rmq_broker_port
        ))

        if amqp_url:
            self.amqp_url = amqp_url

        self.setup_worker()

    def setup_worker(self):
        """Setup RabbitMQ worker"""
        self.worker = RabbitMqBaseAsyncConsumer(amqp_url=self.amqp_url, exchange='deploy', callback=self.callback)

    def close(self):
        if self.worker:
            self.worker.stop()

    def run(self):
        if self.worker:
            self.worker.run()

def echo(body):
    print ">>>>> body: {}".format(body)

def main():
    config = ConfigService.load_configuration()
    base_async_consumer = RabbitMqMessageManager(
        config=config,
        amqp_url='amqp://guest:guest@localhost:5672/%2F',
        callback=echo,
    )
    try:
        base_async_consumer.run()
    except KeyboardInterrupt:
        logging.info("Pressed CTRL-C")
        base_async_consumer.close()


if __name__ == '__main__':
    main()