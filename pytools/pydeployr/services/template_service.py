# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 22:43 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import sys
import logging

import os
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from pydeployr.services import filesystem_service


class TemplateService(object):
    """
        Responsible for writing templates to file system.
    """

    BASE_TEMPLATE = 'genapi_base.tpl'
    BACKENDS_TEMPLATE = 'genapi_backends.tpl'
    FRONTENDS_TEMPLATE = 'genapi_frontends.tpl'

    def entity_list_as_csv(self, entity_list):
        """
            Create a comma-separated list of the entity array
        """
        return ','.join([str(i) for i in entity_list])

    def get_template_base_dir(self, ):
        """
            Depending on where deployr is run, we need to find the templates in a defined location.
        """
        if sys.platform == 'darwin':
            template_dir = "{}/.deployr/templates".format(os.getenv("HOME"))
        elif sys.platform == 'linux2':
            template_dir = "/etc/deployr/templates"
        else:
            template_dir = "{}/.deployr/templates".format(os.getenv("HOME"))
        return template_dir

    def load_template(self, template_name):
        """
            Use jinja2 template engine to load the corresponding template file
        """
        env = Environment(loader=FileSystemLoader(self.get_template_base_dir()))
        template = env.get_template(template_name)
        return template

    def write_genapi_base_tpl(self, python_interpreter, genapi_start, logging_level, riak_host, riak_port, app_port,
                              genapi_api_id, genapi_version, genapi_env, genapi_entity_list, genapi_api_key,
                              genapi_home_directory, genapi_user, genapi_log_file, config_file_name):
        """
            Write a configuration file for a given API that will be readable by supervisord.
        """
        template = self.load_template(self.BASE_TEMPLATE)
        tpl = template.render(
            genapi_api_id=genapi_api_id,
            python_interpreter=python_interpreter,
            genapi_start=genapi_start,
            logging_level=logging_level,
            riak_host=riak_host,
            riak_port=riak_port,
            app_port=app_port,
            genapi_version=genapi_version,
            genapi_env=genapi_env,
            genapi_entity_list=self.entity_list_as_csv(genapi_entity_list),
            genapi_api_key=genapi_api_key,
            genapi_home_directory=genapi_home_directory,
            genapi_user=genapi_user,
            genapi_log_file=genapi_log_file
        )

        logging.debug("Writing template: {}".format(tpl))
        filesystem_service.write_file(filename=config_file_name, content=tpl)
        logging.info('Supervisor configuration file written for API with id: {}'.format(genapi_api_id))

    def write_genapi_backends_tpl(self, config_file_name, api_id, api_host, api_port):
        """
            Write the haproxy backends part for an already deployed API in order to
            create the routing (part 1) on the loadbalancer.
        """
        template = self.load_template(self.BACKENDS_TEMPLATE)
        tpl = template.render(api_id=api_id, api_host=api_host, api_port=api_port)

        logging.debug("Writing template: {}".format(tpl))
        filesystem_service.write_file(filename=config_file_name, content=tpl)

        logging.info('Loadbalancer (haproxy) BACKENDS configuration written for API with id: {}'.format(api_id))

    def write_genapi_frontends_tpl(self, config_file_name, api_id):
        """
            Write the haproxy backends part for an already deployed API in order to
            create the routing (part 1) on the loadbalancer.
        """
        template = self.load_template(self.FRONTENDS_TEMPLATE)
        tpl = template.render(api_id=api_id)
        logging.debug("Writing template: {}".format(tpl))
        filesystem_service.write_file(filename=config_file_name, content=tpl)

        logging.info('Loadbalancer (haproxy) FRONTENDS configuration written for API with id: {}'.format(api_id))
