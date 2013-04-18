# -*- coding: utf-8 -*-
"""

    balancr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import os
import sys
import logging
from pybalancr.repositories import haproxy_repository
from pydeployr.conf.returncodes import RETURNCODE
from pydeployr.services.template_service import TemplateService


def define_haproxy_config_path():
    """
        Construct the base path depending on the running platform we are on.
    """
    if sys.platform == 'darwin':
        return '.'
    elif sys.platform == 'linux2':
        return '/etc/haproxy'
    else:
        return '.'


def create_and_fetch_backends_directory(api_id):
    """
        Creates the necessary /etc/haproxy/backends/<api_id>-cluster directory
        for the backends config file.
    """
    backends_path = '{}/backends/{}_cluster'.format(define_haproxy_config_path(), api_id)
    if not os.path.exists(backends_path):
        os.mkdir(backends_path, 0755)
    return backends_path


def get_backends_config_file(api_id):
    """
        Define the backends config file.
    """
    return '{}/100-{}'.format(create_and_fetch_backends_directory(api_id), api_id)


def get_frontends_config_file(api_id):
    """
        Define the frontends config file.
    """
    return '{}/frontends/http_proxy/100-{}'.format(define_haproxy_config_path(), api_id)


def loadbalance_update_api(api_id, api_host, api_port):
    """
        Write the backends and frontends configuration file for haproxy
        for a given deployed API.
    """
    # get the config file names
    backends_config = get_backends_config_file(api_id=api_id)
    frontends_config = get_frontends_config_file(api_id=api_id)

    # Get the template service
    template_service = TemplateService()

    # Write the backends config
    logging.info('Writing configuration {} for API: {}'.format(backends_config, api_id))
    template_service.write_genapi_backends_tpl(
        config_file_name=backends_config,
        api_id=api_id,
        api_host=api_host,
        api_port=api_port
    )

    # write the frontends config
    logging.info('Writing configuration {} for API: {}'.format(frontends_config, api_id))
    template_service.write_genapi_frontends_tpl(config_file_name=frontends_config, api_id=api_id)

    # add the config (implicitly starts the genapi)
    logging.info('Trying to reload loadbalancer (haproxy), now ...')

    status_code = RETURNCODE.OS_SUCCESS
    if not haproxy_repository.reload_haproxy():
        logging.error("Error on reloading haproxy.")
        status_code = RETURNCODE.OS_ERROR

    return status_code
