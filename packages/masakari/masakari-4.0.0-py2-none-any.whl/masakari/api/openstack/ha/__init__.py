# Copyright (c) 2016 NTT Data
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
WSGI middleware for OpenStack Compute API.
"""

import masakari.api.openstack
from masakari.api.openstack.ha import extension_info
import masakari.conf


CONF = masakari.conf.CONF


class APIRouterV1(masakari.api.openstack.APIRouterV1):
    """Routes requests on the OpenStack API to the appropriate controller
    and method.
    """
    def __init__(self, init_only=None):
        self._loaded_extension_info = extension_info.LoadedExtensionInfo()
        super(APIRouterV1, self).__init__(init_only)

    def _register_extension(self, ext):
        return self.loaded_extension_info.register_extension(ext.obj)

    @property
    def loaded_extension_info(self):
        return self._loaded_extension_info
