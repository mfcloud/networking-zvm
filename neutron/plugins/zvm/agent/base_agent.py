# Copyright 2014 IBM Corp.
#
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

from keystoneauth1 import loading as ks_loading
from neutronclient.v2_0 import client as clientv20
from oslo_config import cfg
from oslo_log import log as logging

from neutron.plugins.zvm.common import config

LOG = logging.getLogger(__name__)

CONF = cfg.CONF


class NeutronAPIClient(object):

    def __init__(self):
        self._init_client()

    def _init_client(self):
        session = ks_loading.load_session_from_conf_options(
            CONF, config.NEUTRON_GROUP)
        auth_plugin = ks_loading.load_auth_from_conf_options(
            CONF, config.NEUTRON_GROUP)

        self._client = clientv20.Client(
            session=session,
            auth=auth_plugin)

    def get_network_ports(self, **kwargs):
        try:
            return self._client.list_ports(**kwargs)['ports']
        except Exception as ex:
            LOG.error("Exception caught: %s" % ex)
        return []
