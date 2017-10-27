# Copyright 2014 IBM Corp.
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


from oslo_log import log as logging

from neutron.plugins.zvm.common import config as cfg
from neutron.plugins.zvm.common import exception
from sdkclient import client

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class zVMSDKRequestHandler(object):

    def __init__(self):
        self._sdkclient = client.SDKClient(CONF.AGENT.zvm_sdkserver_addr)

    def call(self, func_name, *args, **kwargs):
        results = self._sdkclient.send_request(func_name, *args, **kwargs)
        if results['overallRC'] == 0:
            return results['output']
        else:
            msg = ("SDK request %(api)s failed with parameters: %(args)s "
                   "%(kwargs)s . Results: %(results)s" %
                   {'api': func_name, 'args': str(args), 'kwargs': str(kwargs),
                    'results': str(results)})
            LOG.debug(msg)
            raise exception.ZVMSDKRequestFailed(msg=msg, results=results)


class zvmUtils(object):

    def __init__(self):
        self._sdkreq = zVMSDKRequestHandler()

    def get_port_map(self):
        ports_info = self._sdkreq.call('guests_get_nic_info')
        ports = {}
        for p in ports_info:
            if p[3] is not None:
                userid = p[0]
                vswitch = p[2]
                port_id = p[3]
                ports[port_id] = {'userid': userid,
                                  'vswitch': vswitch}
        return ports
