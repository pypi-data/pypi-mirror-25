""" Unittest for juju-deployer diff action (--diff) """
# pylint: disable=C0103
from __future__ import absolute_import
import os
import shutil
import tempfile
import unittest
import yaml

from mock import patch, mock_open
from six import StringIO

from deployer.config import ConfigStack
from deployer.env.mem import MemoryEnvironment
from deployer.utils import setup_logging

from .base import Base, skip_if_offline, TEST_OFFLINE, TEST_OFFLINE_REASON
from ..action.diff import Diff


@skip_if_offline
class DiffTest(Base):

    def setUp(self):
        self.output = setup_logging(
            debug=True, verbose=True, stream=StringIO())

    # Because fetch_charms is expensive, do it once for all tests
    @classmethod
    def setUpClass(cls):
        super(DiffTest, cls).setUpClass()
        # setUpClass not being skipped, here, could have to do with
        # decorator on derived class.  So skip explicitly.
        if TEST_OFFLINE:
            raise unittest.SkipTest(TEST_OFFLINE_REASON)
        deployment = ConfigStack(
            [os.path.join(
                cls.test_data_dir,
                "openstack",
                "openstack-1501.yaml")]).get('openstack')
        cls._dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(cls._dir, "trusty"))
        deployment.repo_path = cls._dir
        deployment.fetch_charms()
        deployment.resolve()
        cls._deployment = deployment

    @classmethod
    def tearDownClass(cls):
        super(DiffTest, cls).tearDownClass()
        # TearDownClass not being skipped, here, could have to do with
        # decorator on derived class.  So skip explicitly.
        if TEST_OFFLINE:
            raise unittest.SkipTest(TEST_OFFLINE_REASON)
        shutil.rmtree(cls._dir)

    @classmethod
    def get_dir(cls):
        """ Return temp working dir
        """
        return cls._dir

    @classmethod
    def get_deployment(cls):
        """ Return saved deployment at class initialization
        """
        return cls._deployment

    def test_diff_nil(self):
        dpl = self.get_deployment()
        # No changes, assert nil diff
        env = MemoryEnvironment(dpl.name, dpl)
        diff = Diff(env, dpl, {}).do_diff()
        self.assertEqual(diff, {})

    def test_diff_num_units(self):
        # Removing 1 unit must show -1 'num_units'
        dpl = self.get_deployment()
        env = MemoryEnvironment(dpl.name, dpl)
        env.remove_unit(env.status()['services']['nova-compute']['units'][0])
        diff = Diff(env, dpl, {}).do_diff()
        self.assertEqual(
            diff['services']['modified']['nova-compute']['num_units'], -1)
        # re-adding a unit -> nil diff
        env.add_units('nova-compute', 1)
        diff = Diff(env, dpl, {}).do_diff()
        self.assertEqual(diff, {})

    def test_diff_config(self):
        dpl = self.get_deployment()
        env = MemoryEnvironment(dpl.name, dpl)
        # Reconfigure the environment to have an explicit change
        # (admin-password), one that differs from the charm
        # default (admin-token), and an option that no longer exists in the
        # charm (obsolete).
        env.set_config(
            'keystone',
            {'admin-password': 'password', 'admin-user': 'root',
             'obsolete': 'for ages'})
        diff = Diff(env, dpl, {}).do_diff()
        mod_keystone = diff['services']['modified']['keystone']
        self.assertEqual(
            mod_keystone['env-config'],
            {'admin-password': 'password', 'admin-user': 'root',
             'obsolete': 'for ages'})
        self.assertEqual(
            mod_keystone['cfg-config'],
            {'admin-password': 'openstack', 'admin-user': 'admin',
             'obsolete': None})

    def test_diff_constraints(self):
        dpl = self.get_deployment()
        env = MemoryEnvironment(dpl.name, dpl)
        env.set_constraints('nova-compute', 'foo=bar')
        diff = Diff(env, dpl, {}).do_diff()
        mod_svc = diff['services']['modified']['nova-compute']
        self.assertTrue(
            mod_svc['env-constraints'] != mod_svc['cfg-constraints'])
        self.assertEqual(mod_svc['env-constraints'], {'foo': 'bar'})

    def test_diff_env_remove_relation(self):
        dpl = self.get_deployment()
        env = MemoryEnvironment(dpl.name, dpl)
        env.remove_relation('cinder:amqp', 'rabbitmq-server:amqp')
        diff = Diff(env, dpl, {}).do_diff()
        self.assertEqual(str(diff['relations']['missing']),
                         '[cinder:amqp <-> rabbitmq-server:amqp]')

    def test_diff_env_service_destroy(self):
        dpl = self.get_deployment()
        env = MemoryEnvironment(dpl.name, dpl)
        env.destroy_service('nova-compute')
        diff = Diff(env, dpl, {}).do_diff()
        self.assertTrue(
            str(diff['relations']['missing'][0]).find('nova-compute') != -1)
        self.assertEqual(
            list(diff['services']['missing'].keys()),
            ['nova-compute'])

    def test_diff_cfg_remove_relation(self):
        dpl = self.get_deployment()
        # need a tmp file to sneak and save deployment YAML
        edited_config_file = os.path.join(self.get_dir(), 'saved.yaml')
        dpl.save(edited_config_file)
        # in memory edit yaml content
        edited_config = yaml.load(open(edited_config_file))
        edited_config["relations"].remove(
            ['nova-compute:amqp', 'rabbitmq-server:amqp'])
        edited_config = yaml.dump({'openstack': edited_config})

        # mock open to inyect edited_config YAML to ConfigStack
        with patch('deployer.config.open', mock_open(read_data=edited_config),
                   create=True):
            edited_dpl = ConfigStack("mocked").get('openstack')

        edited_dpl.repo_path = self.get_dir()
        edited_dpl.fetch_charms()
        edited_dpl.resolve()
        env = MemoryEnvironment(dpl.name, dpl)
        diff = Diff(env, edited_dpl, {}).do_diff()
        self.assertTrue(
            diff['relations']['unknown'],
            '[nova-compute:amqp <-> rabbitmq-server:amqp]')

    def test_diff_cfg_remove_ambiguous_relation(self):
        dpl = self.get_deployment()
        # need a tmp file to sneak and save deployment YAML
        edited_config_file = os.path.join(self.get_dir(), 'saved.yaml')
        dpl.save(edited_config_file)
        # in memory edit yaml content
        edited_config = yaml.load(open(edited_config_file))
        edited_config["relations"].remove(
            ['ceilometer:identity-service', 'keystone:identity-service'])
        edited_config = yaml.dump({'openstack': edited_config})

        # mock open to inyect edited_config YAML to ConfigStack
        with patch('deployer.config.open', mock_open(read_data=edited_config),
                   create=True):
            edited_dpl = ConfigStack("mocked").get('openstack')

        edited_dpl.repo_path = self.get_dir()
        edited_dpl.fetch_charms()
        edited_dpl.resolve()
        env = MemoryEnvironment(dpl.name, dpl)
        diff = Diff(env, edited_dpl, {}).do_diff()
        # verify ceilometer<->keystone present in unknown relations
        self.assertTrue('ceilometer' in str(diff['relations']['unknown']) and
                        'keystone' in str(diff['relations']['unknown']))

    def test_diff_cfg_replace_with_unnamed_relations(self):
        dpl = self.get_deployment()
        # need a tmp file to sneak and save deployment YAML
        edited_config_file = os.path.join(self.get_dir(), 'saved.yaml')
        dpl.save(edited_config_file)
        # in memory edit yaml content
        edited_config = yaml.load(open(edited_config_file))
        # remove ':name' from service endpoint specification
        for relation in edited_config["relations"]:
            relation = [(relation[0] + ":").split(":")[0],
                        (relation[1] + ":").split(":")[0]]
        edited_config = yaml.dump({'openstack': edited_config})

        # mock open to inyect edited_config YAML to ConfigStack
        with patch('deployer.config.open', mock_open(read_data=edited_config),
                   create=True):
            edited_dpl = ConfigStack("mocked").get('openstack')

        edited_dpl.repo_path = self.get_dir()
        edited_dpl.fetch_charms()
        edited_dpl.resolve()
        env = MemoryEnvironment(dpl.name, dpl)
        diff = Diff(env, edited_dpl, {}).do_diff()
        self.assertEqual(diff, {})
