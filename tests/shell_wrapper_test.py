import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.shell_wrapper import *


class ShellWrapperTest(unittest.TestCase):

    def setUp(self):
        self.shell_wrapper = ShellWrapper()

    def test_execute_command(self):
        """
        Test the command execution and return of output.
        """
        command = 'git config --get remote.origin.url'
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = self.shell_wrapper.execute_command(command).replace('\n', '')

        self.assertEqual(expected, actual)

    def test_execute_command_invalid(self):
        """
        Test the command execution for an invalid command.
        """
        command = 'an-invalid-command'

        expected_false = self.shell_wrapper.execute_command(command)

        self.assertFalse(expected_false)


def fake_execute_command_with_error(command):
    """
    Method to overwrite the shell_wrapper.execute_command method, for mocking,
    with errored return.
        """
    return False
