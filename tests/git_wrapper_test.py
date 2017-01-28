import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.git_wrapper import *


class GitWrapperTest(unittest.TestCase):

    def test_get_remote_url(self):
        """
        Test the command execution of getting the remote URL for the current repository.
        """
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = get_remote_url().replace('\n', '')

        self.assertEqual(expected, actual)

    def test_get_username_and_repo(self):
        """
        Test getting the username and repository name for the current repository.
        """
        expected = ('julenpardo', 'Gitssue')
        actual = get_username_and_repo()

        self.assertEqual(expected, actual)

    def test_execute_command(self):
        """
        Test the command execution and return of output.
        """
        command = 'git config --get remote.origin.url'
        expected = 'https://github.com/julenpardo/Gitssue.git'
        actual = execute_command(command).replace('\n', '')

        self.assertEqual(expected, actual)
