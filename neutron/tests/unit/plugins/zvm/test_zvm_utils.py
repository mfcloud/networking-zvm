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

"""
Unit tests for the z/VM utils.
"""
import mock

from neutron.plugins.zvm.common import exception
from neutron.plugins.zvm.common import utils
from neutron.tests import base
from sdkclient import client


class TestZVMUtils(base.BaseTestCase):
    def setUp(self):
        super(TestZVMUtils, self).setUp()
        self._utils = utils.zVMSDKRequestHandler()

    @mock.patch.object(client.SDKClient, 'send_request')
    def test_call(self, request):
        request.return_value = {"overallRC": 0, 'output': "OK"}
        info = self._utils.call('API', "parm1", "parm2")
        request.assert_called_with('API', "parm1", "parm2")
        self.assertEqual("OK", info)

    @mock.patch.object(client.SDKClient, 'send_request')
    def test_call_exception(self, request):
        request.return_value = {"overallRC": 1, 'output': ""}
        self.assertRaises(exception.ZVMSDKRequestFailed,
                          self._utils.call,
                          "API")
