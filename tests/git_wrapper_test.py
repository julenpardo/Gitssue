import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.git_wrapper import *
from gitssue.shell_wrapper import *


class GitWrapperTest(unittest.TestCase):

    class ShellWrapperMock():
        def execute_command(self, command):

    def setUp(self):
        """
        Set up the dependency injections.
        :return:
        """
        self.shell_wrapper = ShellWrapper()

    def test_get_remote_url(self):
        """
        Test getting the remote URL for the current repository.
        """
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = get_remote_url(self.shell_wrapper).replace('\n', '')

        self.assertEqual(expected, actual)

    def test_get_username_and_repo(self):
        """
        Test getting the username and repository name for the current repository.
        """
        expected = ('julenpardo', 'Gitssue')
        actual = get_username_and_repo(self.shell_wrapper)

        self.assertEqual(expected, actual)
