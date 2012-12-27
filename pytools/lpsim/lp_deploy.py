#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    <application_name>

    created by hgschmidt on 26.12.12, 11:39 CET

    Copyright (c) 2012 apitrary

"""
import json
import sys
from lib.mq.rabbitmq.blocking_rpc_publisher import BlockingRPCPublisher
from lib.mq.rabbitmq.blocking_log_publisher import BlockingLogPublisher
from rabbitmq_config import RPC_QUEUE

# MAIN
#
#
zlog = BlockingLogPublisher(amqp_url='amqp://staging:staging@localhost:5672/%2F', service_name='LP')
rpc_client = BlockingRPCPublisher(amqp_url='amqp://staging:staging@localhost:5672/%2F', rpc_queue=RPC_QUEUE)

m = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
deploy_task = {'task': 'deploy', 'api_id': 'abc123', 'id': m}

while True:
    try:
        zlog.info("calling rpc")
        response = rpc_client.call(json.dumps(deploy_task))
        print ">>>>>>>>>>>>>>>> called"
        zlog.info("response = %s" % response)
    except KeyboardInterrupt:
        rpc_client.close()
        zlog.close()
        sys.exit(0)
