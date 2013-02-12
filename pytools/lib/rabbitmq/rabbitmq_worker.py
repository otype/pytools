# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import logging
import socket
import pika
from deployr_service.conf.returncodes import RETURNCODE


class RabbitMqWorker(object):
    """RabbitMQ Worker"""

    def __init__(self, callback, broker_host, broker_port, username, password, queue, activate_prefetch=None):
        self.connection = None
        self.channel = None
        self.callback = callback
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.queue = queue
        self.activate_prefetch = activate_prefetch

    def on_connected(self, connection):
        """Callback method when connection to broker has been established."""
        logging.debug('Connected to Broker! Establishing channel.')
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        """When opening the channel, we declare the queue to use"""
        self.channel = channel
        logging.debug("Declaring queue: {}".format(self.queue))
        self.channel.queue_declare(
            queue=self.queue,
            callback=self.on_queue_declared,
            durable=True,
            exclusive=False,
            auto_delete=False
        )

    def set_prefetch_count(self):
        """Only accepting one message at a time ..."""
        prefetch_count = 1
        logging.debug('Setting prefetch_count = {}'.format(prefetch_count))
        self.channel.basic_qos(prefetch_count=prefetch_count)

    def on_queue_declared(self, frame):
        """Queue has been declared. Now start to consume messages from the queue ..."""
        logging.debug("Consuming message from queue=\'{}\'".format(self.queue))
        logging.debug('Frame: {}'.format(frame))

        if self.activate_prefetch:
            self.set_prefetch_count()

        logging.debug('Now consuming from broker.')
        self.channel.basic_consume(consumer_callback=self.handle_delivery, queue=self.queue)

    def handle_delivery(self, channel, method_frame, header_frame, body):
        """Handle an incoming message."""
        logging.info(
            "Received new task: content-type=\"%s\", delivery-tag=\"%i\", body=%s" %
            (header_frame.content_type, method_frame.delivery_tag, body)
        )

        status = self.callback(body)
        if status == RETURNCODE.OS_SUCCESS:
            logging.debug('Acknowledging received message.')
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            logging.error('Error running task!')

    def connect_to_broker(self):
        """Connect to RabbitMQ broker"""
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(host=self.broker_host, port=self.broker_port, credentials=credentials)
        self.connection = pika.SelectConnection(parameters, self.on_connected)
        logging.info('Connected to broker: {}:{}'.format(self.broker_host, self.broker_port))

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def run(self):
        """Start the consumer IOLoop"""
        try:
            self.connect_to_broker()
            self.connection.ioloop.start()
        except socket.gaierror, e:
            logging.error("Socket.gaierror! Error: {}".format(e))
            self.disconnect()
        except socket.error, e:
            logging.error("Socket.error! Error: {}".format(e))
            self.disconnect()
        except KeyboardInterrupt:
            logging.info('Orderly shutting down ...')
            self.disconnect()
        except Exception, e:
            logging.error('Unknown error! Better run away, now! Error: {}'.format(e))
        finally:
            logging.info('Connection closed.')
