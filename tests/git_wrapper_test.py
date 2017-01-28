import unittest
from unittest import mock
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.git_wrapper import *
from gitssue.shell_wrapper import *
import shell_wrapper_test


class GitWrapperTest(unittest.TestCase):

    def setUp(self):
        """
        Set up the dependencies.
        """
        self.shell_wrapper = ShellWrapper()
        self.shell_wrapper_mock = mock.Mock()
        self.shell_wrapper_mock.execute_command = shell_wrapper_test\
            .fake_execute_command_with_error('git config --get remote.origin.url')

    def test_get_remote_url(self):
        """
        Test getting the remote URL for the current repository.
        """
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = get_remote_url(self.shell_wrapper).replace('\n', '')

        self.assertEqual(expected, actual)

    def test_get_remote_url_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """

        actual = get_remote_url(self.shell_wrapper_mock)

    def test_get_username_and_repo(self):
        """
        Test getting the username and repository name for the current repository.
        """
        expected = ('julenpardo', 'Gitssue')
        actual = get_username_and_repo(self.shell_wrapper)

        self.assertEqual(expected, actual)

    def test_get_username_and_repo_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """

        actual = get_username_and_repo(self.shell_wrapper_mock)

