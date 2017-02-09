import os
import sys
import unittest
from unittest import mock

sys.path.append(os.path.abspath('..'))
from gitssue.git.git_wrapper import *
from gitssue.git.repo_not_found_exception import RepoNotFoundException


class GitWrapperTest(unittest.TestCase):

    mock_response = None

    def mock_execute_command(self, command):
        return self.mock_response

    def fake_execute_command(self, command):
        return 'https://github.com/julenpardo/Gitssue'

    def mock_execute_command_with_error(self, command):
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
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

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
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

        with self.assertRaises(RepoNotFoundException):
            get_username_and_repo(shell_wrapper_mock)

    def test_get_remotes_urls(self):
        mocked_return = "origin git@github.com:julenpardo/Gitssue.git (fetch)"\
                        + "\norigin git@github.com:julenpardo/Gitssue.git (push)"\
                        + "\nother_origin github.com/whatever"\
                        + "\nanother_origin github.com/whatever2 (fetch)"\
                        + "\nanother_origin github.com/whatever2 (push)"
        shell_wrapper_mock = mock.Mock()
        self.mock_response = mocked_return
        shell_wrapper_mock.execute_command = self.mock_execute_command

        expected = [
            ['origin', 'git@github.com:julenpardo/Gitssue.git'],
            ['other_origin', 'github.com/whatever'],
            ['another_origin', 'github.com/whatever2'],
        ]
        actual = get_remotes_urls(shell_wrapper_mock)

        self.assertEqual(expected, actual)

    def test_get_remotes_urls_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

        with self.assertRaises(RepoNotFoundException):
            get_remotes_urls(shell_wrapper_mock)

    def test_discard_not_supported_remotes(self):
        """
        In the current version, only "Github" is supported.
        :return:
        """
        input = [
            ['origin1', 'foo@GiThUb.foo'],
            ['origin2', 'foo@gitlab.foo'],
            ['origin3', 'github.com/foo/bar'],
            ['origin4', 'foo@bitbucket.foo'],
        ]
        expected = [
            ['origin1', 'foo@GiThUb.foo'],
            ['origin3', 'github.com/foo/bar'],
        ]
        actual = discard_not_supported_remotes(input)

        self.assertEqual(expected, actual)

    def test_discard_not_supported_remotes_empty_list(self):
        """
        In the current version, only "Github" is supported.
        :return:
        """
        input = []
        expected = []
        actual = discard_not_supported_remotes(input)

        self.assertEqual(expected, actual)
