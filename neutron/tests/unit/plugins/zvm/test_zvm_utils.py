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
from oslo_config import cfg

from neutron.plugins.zvm.common import utils
from neutron.tests import base
from zvmsdk import utils as zvmutils


class TestZVMUtils(base.BaseTestCase):

    _FAKE_VSWITCH_NAME = "fakevsw1"
    _FAKE_PORT_NAME = "fake_port_name"
    _FAKE_RET_VAL = 0
    _FAKE_VM_PATH = "fake_vm_path"
    _FAKE_VSWITCH = "fakevsw1"
    _FAKE_VLAN_ID = "fake_vlan_id"
    _FAKE_ZHCP_NODENAME = "fakezhcp"
    _FAKE_ZHCP_USER = 'zhcp_user'
    _FAKE_VDEV = "1000"
    _FAKE_XCAT_NODENAME = "fakexcat"
    _FAKE_XCAT_USER = "fake_xcat_user"
    _FAKE_XCAT_PW = "fake_xcat_password"

    def setUp(self):
        super(TestZVMUtils, self).setUp()
        self._xcat_url = zvmutils.get_xcat_url()
        self.addCleanup(cfg.CONF.reset)
        cfg.CONF.set_override('zvm_xcat_username', self._FAKE_XCAT_USER,
                              group='AGENT')
        cfg.CONF.set_override('zvm_xcat_password', self._FAKE_XCAT_PW,
                              group='AGENT')
        with mock.patch(
            'neutron.plugins.zvm.common.utils.zvmUtils._get_xcat_node_name',
                mock.Mock(return_value=self._FAKE_XCAT_NODENAME)):
            self._utils = utils.zvmUtils()

    def test_couple_nic_to_vswitch(self):
        pass

    def test_grant_user(self):
        pass

    def test_uncouple_nic_from_vswitch(self):
        pass

    def test_revoke_user(self):
        pass

    def test_check_vswitch_status(self):
        pass

    def test_add_vswitch_exist_not_changed(self):
        pass

    def test_add_vswitch_exist_changed(self):
        pass

    def test_add_vswitch(self):
        pass

    def test_set_vswitch_rdev(self):
        pass

    def test_set_vswitch_port_vlan_id(self):
        pass

    @mock.patch.object(zvmutils, 'xcat_request')
    def test_get_nic_ids(self, xrequest):
        xrequest.return_value = {"data": [["test1", "test2"]]}
        data = 'fnode,fswitch,fport,fvlan,finf,-,false'
        xrequest.return_value = {'data': [[(
            '#node,switch,port,vlan,interface,comments,disable'), data]]}
        addp = ''
        url = self._xcat_url.tabdump("/switch", addp)
        info = self._utils.get_nic_ids()
        xrequest.assert_called_with('GET', url)
        self.assertEqual(info, [data])

    @mock.patch.object(utils.zvmUtils, 'get_nic_settings')
    def test_get_node_from_port(self, get_nic):
        self._utils.get_node_from_port(self._FAKE_PORT_NAME)
        get_nic.assert_called_once_with(self._FAKE_PORT_NAME, get_node=True)

    @mock.patch.object(zvmutils, 'xcat_request')
    def test_get_userid_from_node(self, xrequest):
        xrequest.return_value = {'data': [["fake_user"]]}
        addp = '&col=node&value=%s&attribute=userid' % self._FAKE_ZHCP_NODENAME
        url = self._xcat_url.gettab("/zvm", addp)
        ret = self._utils.get_userid_from_node(self._FAKE_ZHCP_NODENAME)
        xrequest.assert_called_with('GET', url)
        self.assertEqual(ret, "fake_user")

    def test_put_user_direct_online(self):
        pass

    @mock.patch.object(zvmutils, 'xcat_request')
    def test_update_xcat_switch(self, xrequest):
        commands = "port=%s" % self._FAKE_PORT_NAME
        commands += " switch.switch=%s" % self._FAKE_VSWITCH_NAME
        commands += " switch.vlan=%s" % (self._FAKE_VLAN_ID and
                                         self._FAKE_VLAN_ID or -1)
        url = self._xcat_url.tabch("/switch")
        body = [commands]
        self._utils.update_xcat_switch(self._FAKE_PORT_NAME,
                                       self._FAKE_VSWITCH_NAME,
                                       self._FAKE_VLAN_ID)
        xrequest.assert_called_with("PUT", url, body)

    def _verify_query_nic(self, result, xcat_req):
        pass

    def test_create_xcat_mgt_network_exist(self):
        pass

    def test_create_xcat_mgt_network_not_exist(self):
        pass

    def test_re_grant_user(self):
        pass

    @mock.patch.object(zvmutils, 'xcat_request')
    def test_query_xcat_uptime(self, xrequest):
        xrequest.return_value = {'data': [['2014-06-11 02:41:15']]}
        url = self._xcat_url.xdsh("/%s" % self._FAKE_XCAT_NODENAME)
        cmd = 'date -d "$(awk -F. \'{print $1}\' /proc/uptime) second ago"'
        cmd += ' +"%Y-%m-%d %H:%M:%S"'
        xdsh_commands = 'command=%s' % cmd
        body = [xdsh_commands]
        ret = self._utils.query_xcat_uptime()
        xrequest.assert_called_with('PUT', url, body)
        self.assertEqual(ret, '2014-06-11 02:41:15')

    def test_query_zvm_uptime(self):
        pass

    def test_add_nic_to_user_direct(self):
        pass
