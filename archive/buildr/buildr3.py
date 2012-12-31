# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 28.12.12, 13:44 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import pika
from archive.lib.mq.rabbitmq.rabbitmq_config import LOGGING_EXCHANGE, LP_BUILDR_EXCHANGE, BUILDR_EXCHANGE_TYPE, BUILDR_DEPLOYR_EXCHANGE, BUILDR_BALANCR_EXCHANGE

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
LOGGER = logging.getLogger(__name__)

class ChannelHolder(object):
    def __init__(self, channel, exchange, callback=None, queue=None, exchange_type='topic', topic_key='#'):
        self._channel = channel
        self._exchange = exchange
        self._callback = callback
        self._queue = queue
        self._exchange_type = exchange_type
        self._topic_key = topic_key
        self.channelReady = False

    def setup_exchange(self):
        LOGGER.info('Declaring exchange %s', self._exchange)
        self._channel.exchange_declare(
            callback=self.on_exchange_declareok,
            exchange=self._exchange,
            exchange_type=self._exchange_type
        )

    def on_exchange_declareok(self, unused_frame):
        """Exchange is declared. Now, declare queue."""
        LOGGER.info('Exchange declared')
        if self._queue is None:
            LOGGER.info('Declaring queue')
            self._channel.queue_declare(self.on_queue_declareok, exclusive=True)
        else:
            LOGGER.info('Declaring queue %s', self._queue)
            self._channel.queue_declare(self.on_queue_declareok, self._queue)

    def on_queue_declareok(self, method_frame):
        """Queue is declared. Now, bind to queue."""
        self._queue = method_frame.method.queue
        LOGGER.info('Binding %s to %s with %s', self._exchange, self._queue, self._topic_key)
        self._channel.queue_bind(
            callback=self.on_bindok,
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._topic_key
        )

    def on_bindok(self, unused_frame):
        """Queue is bound."""
        LOGGER.info('Queue bound')
        self.channelReady = True
        self._callback()

    def publish(self, topic_key, message):
        """Send the message"""
        self._channel.basic_publish(exchange=self._exchange, routing_key=topic_key, body=message)

    def consume(self, callback):
        """Called when RabbitMQ has told us our Queue has been declared, frame is
        the response from RabbitMQ"""
        self._channel.basic_consume(consumer_callback=callback, queue=self._queue)


class Buildr(object):

    _exchange_type = BUILDR_EXCHANGE_TYPE
    lp_buildr_exchange = LP_BUILDR_EXCHANGE
    buildr_deployr_exchange = BUILDR_DEPLOYR_EXCHANGE
    buildr_balancr_exchange = BUILDR_BALANCR_EXCHANGE
    logging_exchange = LOGGING_EXCHANGE

    def __init__(self, amqp_url):
        self._url = amqp_url
        self.connection = None
        self.lp_buildr_channel = None
        self.buildr_deployr_channel = None
        self.buildr_balancr_channel = None
        self.logging_channel = None

    def connect(self):
        """Connect to RabbitMQ"""
        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(pika.URLParameters(self._url), self.on_connected)

    def on_connected(self, connection):
        """Called when we are fully connected to RabbitMQ. Opens a channel for tx and rx."""
        LOGGER.info('Connected! Now opening channels.')
        self.connection.channel(on_open_callback=self.declare_channel)
        self.connection.channel(on_open_callback=self.declare_channel)

    def declare_channel(self, new_channel):
        if self.lp_buildr_channel is None:
            self.declare_lp_buildr_channel(new_channel)
        elif self.buildr_deployr_channel is None:
            self.declare_buildr_deployr_channel(new_channel)
        elif self.buildr_balancr_channel is None:
            self.declare_buildr_balancr_channel(new_channel)
        elif self.logging_channel is None:
            self.declare_buildr_loggr_channel(new_channel)

    def declare_lp_buildr_channel(self, channel):
        LOGGER.info("Declaring LP-BUILDR channel")
        self.lp_buildr_channel = ChannelHolder(channel=channel, exchange=self.lp_buildr_exchange, callback=self.start)
        self.lp_buildr_channel.setup_exchange()

    def declare_buildr_deployr_channel(self, channel):
        LOGGER.info("Declaring LP-BUILDR channel")
        self.buildr_deployr_channel = ChannelHolder(channel=channel, exchange=self.buildr_deployr_exchange, callback=self.start)
        self.buildr_deployr_channel.setup_exchange()

    def declare_buildr_balancr_channel(self, channel):
        LOGGER.info("Declaring LP-BUILDR channel")
        self.buildr_balancr_channel = ChannelHolder(channel=channel, exchange=self.buildr_balancr_exchange, callback=self.start)
        self.buildr_balancr_channel.setup_exchange()

    def declare_buildr_loggr_channel(self, channel):
        LOGGER.info("Declaring LP-BUILDR channel")
        self.logging_channel = ChannelHolder(channel=channel, exchange=self.logging_exchange, callback=self.start)
        self.logging_channel.setup_exchange()

    def start(self):
        if self.lp_buildr_channel.channelReady \
        and self.buildr_deployr_channel.channelReady \
        and self.buildr_balancr_channel.channelReady \
        and self.logging_channel.channelReady:
            LOGGER.info('Channels ready. Starting to consume.')
            self.lp_buildr_channel.consume(callback=self.handle_consume)

    def handle_consume(self, channel, method, properties, body):
        queue_name = method.routing_key
        LOGGER.info('Received message on queue: {}'.format(queue_name))
        # TODO: Do something here!
        self.logging_channel.publish(topic_key='#', message='auto auto')

    def start_consumer(self):
        self.connection = self.connect()
        try:
            LOGGER.info('Starting ioloop')
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # Connect to localhost:5672 as staging with the password guest and virtual host "/" (%2F)
    combined_client = Buildr(amqp_url='amqp://staging:staging@localhost:5672/%2F')
    combined_client.start_consumer()

if __name__ == '__main__':
    main()