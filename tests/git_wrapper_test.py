import unittest
from unittest import mock

from gitssue.git.git_wrapper import GitWrapper
from gitssue.git.repo_not_found_exception import RepoNotFoundException


class GitWrapperTest(unittest.TestCase):

    mock_response = None

    def mock_execute_command(self, command):
        return self.mock_response

    def fake_execute_command(self, command):
        return 'https://github.com/julenpardo/Gitssue'

    def fake_execute_command_ssh(self, command):
        return 'git@github.com:julenpardo/Gitssue.git'

    def mock_execute_command_with_error(self, command):
        """
        Method to overwrite the shell_wrapper.execute_command method, for mocking,
        with errored return.
            """
        return False

    def test_get_remote_domain(self):
        """
        Test getting the remote URL for the current repository.
        """
        expected = 'github.com'
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command

        git_wrapper = GitWrapper(shell_wrapper_mock)

        actual = git_wrapper.get_remote_domain().replace('\n', '')

        self.assertEqual(expected, actual)

    def test_get_remote_domain_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

        git_wrapper = GitWrapper(shell_wrapper_mock)

        with self.assertRaises(RepoNotFoundException):
            git_wrapper.get_remote_domain()

    def test_get_username_and_repo(self):
        """
        Test getting the username and repository name for the current repository.
        """
        mocked_return = "origin git@github.com:julenpardo/Gitssue.git (fetch)"
        shell_wrapper_mock = mock.Mock()
        self.mock_response = mocked_return
        shell_wrapper_mock.execute_command = self.mock_execute_command
        expected = [['julenpardo', 'Gitssue']]

        git_wrapper = GitWrapper(shell_wrapper_mock)

        actual = git_wrapper.get_username_and_repo()

        self.assertEqual(expected, actual)

    def test_get_username_and_repo_https(self):
        """
        Test getting the username and repository name for the current repository.
        """
        mocked_return = "origin https://github.com/julenpardo/Gitssue.git (fetch)"
        shell_wrapper_mock = mock.Mock()
        self.mock_response = mocked_return
        shell_wrapper_mock.execute_command = self.mock_execute_command
        expected = [['julenpardo', 'Gitssue']]

        git_wrapper = GitWrapper(shell_wrapper_mock)

        actual = git_wrapper.get_username_and_repo()

        self.assertEqual(expected, actual)

    def test_get_username_and_repo_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

        git_wrapper = GitWrapper(shell_wrapper_mock)

        with self.assertRaises(RepoNotFoundException):
            git_wrapper.get_username_and_repo()

    def test_get_remotes_urls(self):
        mocked_return = "origin git@github.com:julenpardo/Gitssue.git (fetch)"\
                        + "\norigin git@github.com:julenpardo/Gitssue.git (push)"\
                        + "\nother_origin github.com/whatever"\
                        + "\nanother_origin github.com/whatever2 (fetch)"\
                        + "\nanother_origin github.com/whatever2 (push)"
        shell_wrapper_mock = mock.Mock()
        self.mock_response = mocked_return
        shell_wrapper_mock.execute_command = self.mock_execute_command

        git_wrapper = GitWrapper(shell_wrapper_mock)

        expected = [
            ['origin', 'git@github.com:julenpardo/Gitssue.git'],
            ['other_origin', 'github.com/whatever'],
            ['another_origin', 'github.com/whatever2'],
        ]
        actual = git_wrapper.get_remotes_urls()

        self.assertEqual(expected, actual)

    def test_get_remotes_urls_invalid_repo(self):
        """
        Simulate an unexpected return value by the shell wrapper, which would be
        caused by a non existing repository, e.g.
        """
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.mock_execute_command_with_error

        git_wrapper = GitWrapper(shell_wrapper_mock)

        with self.assertRaises(RepoNotFoundException):
            git_wrapper.get_remotes_urls()
