import os
import sys
import unittest
import contextlib
from io import StringIO
from unittest import mock

sys.path.append(os.path.abspath('./gitssue'))

from gitssue.controller import Controller
from gitssue.dependencies import Dependencies


class ControllerTest(unittest.TestCase):

    mocked_remote_return = False

    def setUp(self):
        self.controller = Controller(Dependencies)

    def mock_remote_get_issue_list(self, username, repo, all=False, desc=False):
        return self.mocked_remote_return

    def mock_remote_get_issues_description(self, username, repository, issue_numbers):
        return self.mocked_remote_return

    def mock_remote_get_issue_comments(self, issue_number):
        return self.mocked_remote_return

    def test_thread(self):
        pass

    def test_thread_invalid_issue_number(self):
        input = 'This is not a number, I think.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.thread(input)
            pass

        expected = 'Issue number must be a number.'
        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)
