# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 18:49 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from archive.lib.mq.rabbitmq.base_async_consumer import BaseAsyncConsumer
from archive.lib.mq.rabbitmq.rabbitmq_config import LOGGING_EXCHANGE_TYPE
from archive.lib.mq.rabbitmq.rabbitmq_config import LOGGING_EXCHANGE

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -20s %(funcName) -25s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger('loggr')


class Loggr(BaseAsyncConsumer):
    """
        The Loggr service, responsible for collecting logs from all services and persisting
        the logs into a database (capped collections in MongoDB).
    """

    def __init__(self, amqp_url, debug=False):
        """
            Create a new instance of the consumer class, passing in the AMQP
            URL used to connect to RabbitMQ.
        """
        super(Loggr, self).__init__(
            amqp_url=amqp_url,
            exchange=LOGGING_EXCHANGE,
            exchange_type=LOGGING_EXCHANGE_TYPE,
            debug=debug
        )
        self._topic_key = "#" # bind to all topics

    def setup_exchange(self):
        """
            Setup our exchange
        """
        LOGGER.info('Declaring exchange %s', self._exchange)
        self._channel.exchange_declare(self.on_exchange_declareok, self._exchange, self._exchange_type)


    def setup_queue(self, queue_name):
        """
            Declare an exclusive queue
        """
        LOGGER.info('Declaring queue')
        self._channel.queue_declare(callback=self.on_queue_declareok, exclusive=True)


    def on_queue_declareok(self, method_frame):
        """
            Bind to queue if declaring the queue was fine.
        """
        self._queue = method_frame.method.queue
        LOGGER.info('Binding %s to %s', self._exchange, self._queue)
        self._channel.queue_bind(
            callback=self.on_bindok,
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._topic_key
        )

    def handle_message(self, body):
        """
            The actual message handler!
        """
        super(Loggr, self).handle_message(body)
        # TODO: Store the message to MongoDB
        print(">>> WOULD STORE TO MONGODB HERE!!!")


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    # TODO: Remove debug flag once going into production
    loggr = Loggr(amqp_url='amqp://staging:staging@localhost:5672/%2F', debug=True)
    try:
        loggr.run()
    except KeyboardInterrupt:
        loggr.stop()


if __name__ == '__main__':
    main()