# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 18:17 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import pika
from rabbitmq_config import LOGGING_EXCHANGE, RPC_QUEUE

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
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


class BaseAsyncCombined(object):
    def __init__(self, amqp_url, consumer_exchange, publisher_exchange):
        self._url = amqp_url
        self._consumer_exchange = consumer_exchange
        self._publisher_exchange = publisher_exchange
        self.channel_rx = None
        self.channel_tx = None
        self.connection = None

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
        if self.channel_tx is None:
            LOGGER.info('Declaring TX channel')
            self.channel_tx = ChannelHolder(channel=new_channel, exchange=self._publisher_exchange, callback=self.start)
            self.channel_tx.setup_exchange()
        elif self.channel_rx is None:
            LOGGER.info('Declaring RX channel')
            self.channel_rx = ChannelHolder(channel=new_channel, exchange=self._consumer_exchange, callback=self.start)
            self.channel_rx.setup_exchange()

    def start(self):
        if self.channel_rx.channelReady and self.channel_tx.channelReady:
            LOGGER.info('Channels ready. Starting to consume.')
            self.channel_rx.consume(callback=self.handle_consume)

    def handle_consume(self, channel, method, properties, body):
        queue_name = method.routing_key
        LOGGER.info('Received message on queue: {}'.format(queue_name))
        # TODO: Do something here!
        self.channel_tx.publish(topic_key='#', message='auto auto')

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
    combined_client = BaseAsyncCombined(
        amqp_url='amqp://staging:staging@localhost:5672/%2F',
        consumer_exchange=RPC_QUEUE,
        publisher_exchange=LOGGING_EXCHANGE
    )
    combined_client.start_consumer()

if __name__ == '__main__':
    main()