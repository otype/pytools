# -*- coding: utf-8 -*-
"""

    balancr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import os
import sys
import logging
import subprocess
from pytools.pydeployr.returncodes import RETURNCODE
from pytools.pydeployr.services.template_service import TemplateService


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
        logging.debug('Creating backends directory: {}'.format(backends_path))
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

def reload_haproxy():
    """
        Reload HAPROXY
    """
    logging.info('Trying to reload loadbalancer (haproxy), now ...')
    status_code = subprocess.call(['/etc/init.d/haproxy', 'reload'])
    logging.info('Reload of haproxy status: {}'.format(status_code))
    if status_code != RETURNCODE.OS_SUCCESS:
        logging.error("Error on reloading haproxy.")
    return status_code


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

    # Reload HAPROXY and return
    return reload_haproxy()


def loadbalance_remove_api(api_id):
    """
        Delete the corresponding configuration files for a given API when undeploying.
    """
    backends_config = get_backends_config_file(api_id=api_id)
    frontends_config = get_frontends_config_file(api_id=api_id)

    try:
        logging.info('Deleting BACKEND configuration file:{} for API:{}'.format(backends_config, api_id))
        os.remove(backends_config)
        logging.info('Deleting FRONTEND configuration file:{} for API:{}'.format(frontends_config, api_id))
        os.remove(frontends_config)
    except OSError, e:
        logging.error('Error when trying to delete haproxy configuration files for API:{}! '
                      'Error: {}'.format(api_id, e))
        return RETURNCODE.OS_ERROR

    return reload_haproxy()
