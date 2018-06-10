import unittest
from unittest import mock
from gitssue.dependencies.dependencies import Dependencies
from gitssue.git.git_wrapper import GitWrapper
from gitssue.remote.github import Github
from gitssue.remote.gitlab import Gitlab
from gitssue.remote.bitbucket import Bitbucket
from gitssue.config.config_reader import get_config


class DependenciesTest(unittest.TestCase):

    @mock.patch.object(GitWrapper, 'get_remote_domain')
    def test_inject_dependencies_github(self, get_remote_domain_mock):
        get_remote_domain_mock.return_value = 'github.com'

        dependencies = Dependencies()

        self.assertIsInstance(dependencies.remote, Github)

    @mock.patch.object(GitWrapper, 'get_remote_domain')
    def test_inject_dependencies_gitlab(self, get_remote_domain_mock):
        get_remote_domain_mock.return_value = 'gitlab.com'

        with mock.patch('gitssue.config.config_reader.get_config') as \
                config_mock:
            dependencies = Dependencies()

        self.assertIsInstance(dependencies.remote, Gitlab)

    @mock.patch.object(GitWrapper, 'get_remote_domain')
    def test_inject_dependencies_bitbucket(self, get_remote_domain_mock):
        get_remote_domain_mock.return_value = 'bitbucket.org'

        with mock.patch('gitssue.config.config_reader.get_config') as \
                config_mock:
            dependencies = Dependencies()

        self.assertIsInstance(dependencies.remote, Bitbucket)
