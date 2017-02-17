import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.abspath('.'))


class ShellWrapperTest(unittest.TestCase):

    def fake_execute_command(self, command):
        return 'https://github.com/julenpardo/Gitssue'

    def fake_execute_command_with_error(self, command):
        """
        Method to overwrite the shell_wrapper.execute_command method, for mocking,
        with errored return.
            """
        return False

    def test_execute_command(self):
        """
        Test the command execution and return of output.
        """
        command = 'git config --get remote.origin.url'
        expected = 'https://github.com/julenpardo/Gitssue'
        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command
        actual = shell_wrapper_mock.execute_command(command).replace('\n', '')

        self.assertEqual(expected, actual)

    def test_execute_command_invalid(self):
        """
        Test the command execution for an invalid command.
        """
        command = 'an-invalid-command'

        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command = self.fake_execute_command_with_error
        expected_false = shell_wrapper_mock.execute_command(command)

        self.assertFalse(expected_false)
