# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 00:40 CET
    
    Copyright (c) 2012 apitrary

"""
from archive.deployr_service.deployr_base import DeployrBase
from archive.deployr_service.lib.returncodes import RETURNCODE
from archive.deployr_service.services.supervisor_xml_rpc_service import SupervisorXmlRpcService


class UndeployService(DeployrBase):
    def __init__(self, config):
        super(UndeployService, self).__init__(config)
        self.supervisor_xml_rpc_service = SupervisorXmlRpcService(config=self.config)


    def undeploy_api(self, api_id):
        """
            Undeploy a currently deployed API with given API ID
        """
        status = 0
        status += self.supervisor_xml_rpc_service.stop(app_name=api_id)
        status += self.supervisor_xml_rpc_service.remove_group(group_name=api_id)
        status += self.supervisor_xml_rpc_service.reload_config()

        # TODO: delete configuration file from file system!

        if status > 0:
            status_code = RETURNCODE.OS_ERROR
        else:
            status_code = RETURNCODE.OS_SUCCESS

        return status_code