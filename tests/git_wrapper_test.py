import unittest
from unittest import mock
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.git_wrapper import *
from gitssue.shell_wrapper import *
import tests.shell_wrapper_test
from gitssue.repo_not_found_exception import RepoNotFoundException


class GitWrapperTest(unittest.TestCase):

    def fake_execute_command(self, command):
        return 'https://github.com/julenpardo/Gitssue'

    def fake_execute_command_with_error(self, command):
        """
        Method to overwrite the shell_wrapper.execute_command method, for mocking,
        with errored return.
            """
        return False

    def test_get_remote_url(self):
        """
        Test getting the remote URL for the current repository.
        """
        expected = 'https://github.com/julenpardo/Gitssue'
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command
        actual = get_remote_url(shell_wrapper_mock).replace('\n', '')

        self.assertEqual(expected, actual)

    def test_get_remote_url_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command_with_error

        with self.assertRaises(RepoNotFoundException):
            get_remote_url(shell_wrapper_mock)

    def test_get_username_and_repo(self):
        """
        Test getting the username and repository name for the current repository.
        """
        expected = ('julenpardo', 'Gitssue')

        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command

        actual = get_username_and_repo(shell_wrapper_mock)

        self.assertEqual(expected, actual)

    def test_get_username_and_repo_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command_with_error

        with self.assertRaises(RepoNotFoundException):
            get_username_and_repo(shell_wrapper_mock)
