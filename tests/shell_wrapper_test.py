import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.shell_wrapper import *


class ShellWrapperTest(unittest.TestCase):

    def test_execute_command(self):
        """
        Test the command execution and return of output.
        """
        command = 'git config --get remote.origin.url'
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = ShellWrapper().execute_command(command).replace('\n', '')

        self.assertEqual(expected, actual)
