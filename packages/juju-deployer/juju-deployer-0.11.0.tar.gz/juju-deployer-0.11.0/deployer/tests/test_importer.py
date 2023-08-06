from __future__ import absolute_import
import os

import mock

from deployer.config import ConfigStack
from deployer.action.importer import Importer

from .base import (
    Base,
    skip_if_offline,
)


class Options(dict):

    def __getattr__(self, key):
        return self[key]


class ImporterTest(Base):

    def setUp(self):
        self.juju_home = self.mkdir()
        self.change_environment(JUJU_HOME=self.juju_home)
        self.options = Options({
            'bootstrap': False,
            'branch_only': False,
            'configs': [os.path.join(self.test_data_dir, 'wiki.yaml')],
            'debug': True,
            'deploy_delay': 0,
            'destroy_services': None,
            'diff': False,
            'find_service': None,
            'ignore_errors': False,
            'list_deploys': False,
            'no_local_mods': True,
            'no_relations': False,
            'overrides': None,
            'rel_wait': 60,
            'retry_count': 0,
            'series': None,
            'skip_unit_wait': False,
            'terminate_machines': False,
            'timeout': 2700,
            'update_charms': False,
            'verbose': True,
            'watch': False})

    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer(self, mock_time):
        mock_time.time.return_value = 0
        # Trying to track down where this comes from http://pad.lv/1243827
        stack = ConfigStack(self.options.configs)
        deploy = stack.get('wiki')
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()

        config = {'name': '$hi_world _are_you_there? {guess_who}'}
        self.assertEqual(
            env.method_calls[3], mock.call.deploy(
                'wiki', 'cs:precise/mediawiki',
                os.environ.get("JUJU_REPOSITORY", ""),
                config, None, None, None, 1, None, 'precise', None))
        env.add_relation.assert_called_once_with('wiki', 'db')

    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_with_resources(self, mock_time):
        mock_time.time.return_value = 0
        stack = ConfigStack([
            os.path.join(self.test_data_dir, 'wiki-resources.yaml')])
        deploy = stack.get('wiki')
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()

        config = {'name': '$hi_world _are_you_there? {guess_who}'}
        self.assertEqual(
            env.method_calls[3], mock.call.deploy(
                'wiki', 'cs:precise/mediawiki',
                os.environ.get("JUJU_REPOSITORY", ""),
                config, None,
                {"config": "./docs/cfg.xml", "tarball": "/some/file.tgz"},
                None, 1, None, 'precise', None))
        env.add_relation.assert_called_once_with('wiki', 'db')

    @skip_if_offline
    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_with_storage(self, mock_time):
        mock_time.time.return_value = 0
        stack = ConfigStack([
            os.path.join(self.test_data_dir, 'wiki-storage.yaml')])
        deploy = stack.get('wiki')
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()

        config = {'name': '$hi_world _are_you_there? {guess_who}'}
        self.assertEqual(
            env.method_calls[3], mock.call.deploy(
                'wiki', 'cs:precise/mediawiki',
                os.environ.get("JUJU_REPOSITORY", ""),
                config, None, None, {"web-data": "cinder,10G,1"},
                1, None, 'precise', None))
        env.add_relation.assert_called_once_with('wiki', 'db')

    @skip_if_offline
    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_with_bindings(self, mock_time):
        mock_time.time.return_value = 0
        stack = ConfigStack([
            os.path.join(self.test_data_dir, 'wiki-bindings.yaml')])
        deploy = stack.get('wiki')
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()

        config = {'name': '$hi_world _are_you_there? {guess_who}'}
        self.assertEqual(
            env.method_calls[3], mock.call.deploy(
                'wiki', 'cs:precise/mediawiki',
                os.environ.get("JUJU_REPOSITORY", ""),
                config, None, None, None,
                1, None, 'precise', {"": "default"}))
        env.add_relation.assert_called_once_with('wiki', 'db')

    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_no_relations(self, mock_time):
        mock_time.time.return_value = 0
        self.options.no_relations = True
        stack = ConfigStack(self.options.configs)
        deploy = stack.get('wiki')
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()
        self.assertFalse(env.add_relation.called)

    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_add_machine_series(self, mock_time):
        mock_time.time.return_value = 0
        self.options.configs = [
            os.path.join(self.test_data_dir, 'v4', 'series.yaml')]
        stack = ConfigStack(self.options.configs)
        deploy = stack.get(self.options.configs[0])
        env = mock.MagicMock()
        importer = Importer(env, deploy, self.options)
        importer.run()

        self.assertEqual(env.add_machine.call_count, 2)
        env.add_machine.assert_has_calls([
            mock.call(series='precise', constraints='mem=512M'),
            mock.call(series='trusty', constraints='mem=512M'),
        ], any_order=True)

    @skip_if_offline
    @mock.patch('deployer.action.importer.time')
    def test_importer_existing_machine(self, mock_time):
        mock_time.time.return_value = 0
        self.options.configs = [
            os.path.join(self.test_data_dir, 'v4',
                         'container-existing-machine.yaml')]
        stack = ConfigStack(self.options.configs)
        deploy = stack.get(self.options.configs[0])
        env = mock.MagicMock()

        config = {'status.return_value.get.return_value': {
            1: {}
        }}

        env.configure_mock(**config)

        importer = Importer(env, deploy, self.options)
        importer.run()
        self.assertFalse(env.add_machine.called)
