#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 11:43 CET
    
    Copyright (c) 2012 apitrary

"""
import pika
import json
from time import sleep
import sys
from rabbitmq_config import RPC_QUEUE
from lib.mq.rabbitmq.blocking_log_publisher import BlockingLogPublisher

zlog = BlockingLogPublisher(amqp_url='amqp://staging:staging@localhost:5672/%2F', service_name='BUILDR')
connection = pika.BlockingConnection(pika.URLParameters('amqp://staging:staging@localhost:5672/%2F'))
channel = connection.channel()
channel.queue_declare(queue=RPC_QUEUE)

def deploy_task(msg):
    print(">>> Simulating heavy work: {}".format(msg))
    zlog.info("Deploying ...")
    sleep(5.0)
    return json.dumps({'task': 'deploy', 'status': 'OK'})


def on_request(ch, method, props, body):
    zlog.info("Received client request: %s -- correlation id: %s" % (body, props.correlation_id))
    response = deploy_task(body)

    zlog.info("Sending confirmation -- correlation id: %s" % props.correlation_id)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response)
    )
    zlog.info("Acknowledging task with correlation id: %s" % props.correlation_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# MAIN
#
#
try:
    zlog.info("Started buildr ...")
    #channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=RPC_QUEUE)
    zlog.info("Awaiting tasks ...")
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
    zlog.close()
    sys.exit(0)
