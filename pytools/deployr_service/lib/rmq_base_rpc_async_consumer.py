# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 18:16 CET
    
    Copyright (c) 2012 apitrary

"""
import pika
from tornado.options import enable_pretty_logging, logging

enable_pretty_logging()

class RmqBaseRpcAsyncConsumer(object):
    """
        RPC Worker
    """

    def __init__(self, amqp_url, queue, callback, debug=False):
        self._connection = None
        self._channel = None
        self._consumer_tag = None
        self._url = amqp_url
        self._queue = queue
        self._callback = callback
        self._debug = debug

    def connect(self):
        """
            This method connects to RabbitMQ
        """
        logging.info("Creating SelectConnection")
        return pika.SelectConnection(pika.URLParameters(self._url), self.on_connection_open)

    def on_connection_open(self, unused_connection):
        """
            This method is called by pika once the connection to RabbitMQ has
            been established. It passes the handle to the connection object in
            case we need it, but in this case, we'll just mark it unused.
        """
        logging.info('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """
            When RabbitMQ closes the connection to the publisher unexpectedly
        """
        logging.info("Adding on-close-callback")
        self._connection.add_on_close_callback(self.on_connection_closed)

    def open_channel(self):
        """
            Open a new channel with RabbitMQ by issuing the Channel.Open RPC
            command. When RabbitMQ responds that the channel is open, the
            on_channel_open callback will be invoked by pika.
        """
        logging.info('Opening channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_closed(self, method_frame):
        """
            This method is invoked by pika when the connection to RabbitMQ is
            closed unexpectedly. Since it is unexpected, we will reconnect to
            RabbitMQ if it disconnects.
        """
        logging.warning('Server closed connection, reopening: (%s) %s',
            method_frame.method.reply_code,
            method_frame.method.reply_text)
        self._channel = None
        self._connection = self.connect()

    def on_channel_open(self, channel):
        """
            This method is invoked by pika when the channel has been opened.
            The channel object is passed in so we can make use of it.
        """
        logging.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_queue()

    def add_on_channel_close_callback(self):
        """
            This method tells pika to call the on_channel_closed method if
            RabbitMQ unexpectedly closes the channel.
        """
        self._channel.add_on_close_callback(self.on_channel_closed)

    def setup_queue(self):
        """
            Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
            command. When it is complete, the on_queue_declareok method will
            be invoked by pika.
        """
        logging.info('Declaring queue')
        self._channel.queue_declare(callback=self.on_queue_declareok, queue=self._queue)

    def on_channel_closed(self, method_frame):
        """
            Invoked by pika when RabbitMQ unexpectedly closes the channel.
            Channels are usually closed if you attempt to do something that
            violates the protocol, such as re-declare an exchange or queue with
            different parameters. In this case, we'll close the connection
            to shutdown the object.
        """
        logging.warning('Channel was closed: (%s) %s',
            method_frame.method.reply_code,
            method_frame.method.reply_text)
        self._connection.close()

    def on_queue_declareok(self, method_frame):
        """
            Method invoked by pika when the Queue.Declare RPC call made in
            setup_queue has completed. In this method we will bind the queue
            and exchange together with the routing key by issuing the Queue.Bind
            RPC command. When this command is complete, the on_bindok method will
            be invoked by pika.
        """
        self._channel.basic_qos(callback=self.on_basic_qos_ok, prefetch_count=1)

    def on_basic_qos_ok(self, method_frame):
        logging.info('Basic QOS fetch set %s', method_frame)
        self.start_consuming()

    def start_consuming(self):
        """
            This method sets up the consumer by first calling
            add_on_cancel_callback so that the object is notified if RabbitMQ
            cancels the consumer. It then issues the Basic.Consume RPC command
            which returns the consumer tag that is used to uniquely identify the
            consumer with RabbitMQ. We keep the value to use it when we want to
            cancel consuming. The on_message method is passed in as a callback pika
            will invoke when a message is fully received.
        """
        logging.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message, self._queue)

    def add_on_cancel_callback(self):
        """
            Add a callback that will be invoked if RabbitMQ cancels the consumer
            for some reason. If RabbitMQ does cancel the consumer,
            on_consumer_cancelled will be invoked by pika.
        """
        logging.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """
            Invoked by pika when a message is delivered from RabbitMQ. The
            channel is passed for your convenience. The basic_deliver object that
            is passed in carries the exchange, routing key, delivery tag and
            a redelivered flag for the message. The properties passed in is an
            instance of BasicProperties with the message properties and the body
            is the message that was sent.
        """
        if self._debug:
            logging.info('Received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body)
        response = self.handle_message(body=body)
        self._channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(response)
        )
        self.acknowledge_message(basic_deliver.delivery_tag)

    def on_consumer_cancelled(self, method_frame):
        """
            Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
            receiving messages.
        """
        logging.info('Consumer was cancelled remotely, shutting down: %r', method_frame)
        self._channel.close()

    def handle_message(self, body):
        """
            Message handler! Define here what to do with the body.
        """
        return self._callback(body)

    def acknowledge_message(self, delivery_tag):
        """
            Acknowledge the message delivery from RabbitMQ by sending a
            Basic.Ack RPC method for the delivery tag.
        """
        if self._debug:
            logging.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def close_connection(self):
        """
            This method closes the connection to RabbitMQ.
        """
        self._connection.close()

    def on_cancelok(self, unused_frame):
        """
            This method is invoked by pika when RabbitMQ acknowledges the
            cancellation of a consumer. At this point we will close the connection
            which will automatically close the channel if it's open.
        """
        logging.info('RabbitMQ acknowledged the cancellation of the consumer')
        self.close_connection()

    def stop_consuming(self):
        """
            Tell RabbitMQ that you would like to stop consuming by sending the
            Basic.Cancel RPC command.
        """
        logging.info('Sending a Basic.Cancel RPC command to RabbitMQ')
        self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def close_channel(self):
        """
            Call to close the channel with RabbitMQ cleanly by issuing the
            Channel.Close RPC command.
        """
        logging.info('Closing the channel')
        self._channel.close()

    def run(self):
        """
            Run the example consumer by connecting to RabbitMQ and then
            starting the IOLoop to block and allow the SelectConnection to operate.
        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """
            Cleanly shutdown the connection to RabbitMQ by stopping the consumer
            with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
            will be invoked by pika, which will then closing the channel and
            connection. The IOLoop is started again because this method is invoked
            when CTRL-C is pressed raising a KeyboardInterrupt exception. This
            exception stops the IOLoop which needs to be running for pika to
            communicate with RabbitMQ. All of the commands issued prior to starting
            the IOLoop will be buffered but not processed.
        """
        logging.info('Stopping')
        self.stop_consuming()
        self._connection.ioloop.start()


def echo(body):
    print ">>> body: {}".format(body)
    return "result of worker"

def main():
    base_async_consumer = RmqBaseRpcAsyncConsumer(
        amqp_url='amqp://guest:guest@localhost:5672/%2F',
        queue='rpc_queue',
        callback=echo,
        debug=True
    )
    try:
        base_async_consumer.run()
    except KeyboardInterrupt:
        print "CTRL-C pressed."
        base_async_consumer.stop()


if __name__ == '__main__':
    main()