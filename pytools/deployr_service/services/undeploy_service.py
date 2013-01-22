# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 00:40 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr_service.deployr_base import DeployrBase
from deployr_service.lib.returncodes import RETURNCODE
from deployr_service.services.supervisorctl_service import SuperVisorCtlService


class UndeployService(DeployrBase):
    def __init__(self, config):
        super(UndeployService, self).__init__(config)


    def undeploy_api(self, api_id):
        """Undeploy a currently deployed API with given API ID"""
        supervisorctl_service = SuperVisorCtlService(config=self.config)

        supervisorctl_service.supervisorctl_stop(api_id)
        supervisorctl_service.supervisorctl_remove(api_id)
        supervisorctl_service.supervisorctl_reread()

        # TODO: delete configuration file from file system!
        return RETURNCODE.OS_SUCCESS
