# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 27.12.12, 19:36 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import pika

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class BaseAsyncCombined(object):
    """
        Combines both publisher and consumer.
    """

    def __init__(
            self,
            amqp_url,
            exchange='base_exchange',
            exchange_type='topic',
            publish_interval=1,
            queue='base_queue',
            routing_key='base_consumer.base_queue',
            debug=False

    ):
        """Setup the publisher object, passing in the URL we will use to connect to RabbitMQ.

        :param str amqp_url: The URL for connecting to RabbitMQ

        """
        self._connection = None
        self._channel = None
        self._deliveries = []
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
        self._stopping = False
        self._url = amqp_url
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._publish_interval = publish_interval
        self._queue = queue
        self._routing_key = routing_key
        self._debug = debug


    def connect(self):
        """
            Connect via SelectConnection
        """
        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(pika.URLParameters(self._url), self.on_connection_open)

    def on_connection_open(self, unused_connection):
        """
            When connection is open ...
        """
        LOGGER.info('Connection opened')
        LOGGER.info('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_closed(self, method_frame):
        """Connection has been closed."""
        LOGGER.warning('Server closed connection, reopening: (%s) %s',
            method_frame.method.reply_code,
            method_frame.method.reply_text)
        self._channel = None
        self._connection = self.connect()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        LOGGER.info('Closing connection')
        self._connection.close()

    def on_channel_closed(self, method_frame):
        """Channel has been closed. Close the connection, too."""
        LOGGER.warning('Channel was closed: (%s) %s', method_frame.method.reply_code, method_frame.method.reply_text)
        self._connection.close()

    def on_channel_open(self, channel):
        """Channel has been opened. Now, add close callback and declare exchange."""
        LOGGER.info('Channel opened')
        self._channel = channel
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)
        LOGGER.info('Declaring exchange %s', self._exchange)
        self._channel.exchange_declare(self.on_exchange_declareok, self._exchange, self._exchange_type)

    def on_exchange_declareok(self, unused_frame):
        """Exchange is declared. Now, declare queue."""
        LOGGER.info('Exchange declared')
        LOGGER.info('Declaring queue %s', self._queue)
        self._channel.queue_declare(self.on_queue_declareok, self._queue)

    def on_queue_declareok(self, method_frame):
        """Queue is declared. Now, bind to queue."""
        LOGGER.info('Binding %s to %s with %s', self._exchange, self._queue, self._routing_key)
        self._channel.queue_bind(self.on_bindok, self._queue, self._exchange, self._routing_key)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('Received %s for delivery tag: %i', confirmation_type, method_frame.method.delivery_tag)

        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1

        self._deliveries.remove(method_frame.method.delivery_tag)
        LOGGER.info('Published %i messages, %i have yet to be confirmed, %i were acked and %i were nacked',
            self._message_number,
            len(self._deliveries),
            self._acked, self._nacked
        )

    def publish_message(self):
        """Publish a defined message."""
        if self._stopping:
            return

        message = 'A SAMPLE MESSAGE'
        properties = pika.BasicProperties(app_id='AsyncPublisher', content_type='text/plain')
        self._channel.basic_publish(self._exchange, self._routing_key, message, properties)
        self._message_number += 1
        self._deliveries.append(self._message_number)
        LOGGER.info('Published message # %i', self._message_number)
        self.schedule_next_message()

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds."""
        if self._stopping:
            return
        LOGGER.info('Scheduling next message for %0.1f seconds', self._publish_interval)
        self._connection.add_timeout(self._publish_interval, self.publish_message)

    def on_bindok(self, unused_frame):
        """Queue is bound. Now, let each delivery be confirmed and schedule next message."""
        LOGGER.info('Queue bound')
        LOGGER.info('Issuing Confirm.Select RPC command')
        self._channel.confirm_delivery(self.on_delivery_confirmation)
        LOGGER.debug('Scheduling next message')
        self.schedule_next_message()

    def close_channel(self):
        """Close channel."""
        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self):
        """Run the AsyncPublisher code by connecting and then starting the IOLoop."""
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Stop the AsyncPublisher by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.
        """
        LOGGER.info('Stopping')
        self._stopping = True
        self.close_channel()
        self.close_connection()
        self._connection.ioloop.start()

def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    base_async_combined = BaseAsyncCombined('amqp://guest:guest@localhost:5672/%2F', debug=True)
    try:
        base_async_combined.run()
    except KeyboardInterrupt:
        base_async_combined.stop()

if __name__ == '__main__':
    main()