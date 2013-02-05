# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 22:36 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import socket


def get_host_name():
    """
        Get the hostname
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    return client


def get_open_port():
    """
        Responsible for getting a free port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    logging.debug('Port {} is available.'.format(port))
    return port


def get_local_public_ip_address():
    """
        Get the public IP address for this host
    """
    ipaddr = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except Exception, e:
        logging.error(e)
    return ipaddr
