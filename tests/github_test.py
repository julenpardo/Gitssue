import unittest
from unittest import mock
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.remote.github import Github


class GithubTest(unittest.TestCase):

    fake_request_response = [
            {
                'number': '1',
                'title': 'first fake issue',
                'labels': [{
                    'name': 'fake label 1',
                    'color': 'ffffff'
                }, {
                    'name': 'fake label 2',
                    'color': 'aaaaaa',
                }],
                'body': 'fake body 1',
            }, {
                'number': '2',
                'title': 'second fake issue',
                'labels': [{
                    'name': 'fake label 2',
                    'color': 'ffffff'
                },],
                'body': 'fake body 2',
            },
        ]

    def fake_get_request(self, request):
        return self.fake_request_response

    def fake_get_request_with_error(self, request):
        return False

    def test_get_issue_list(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.fake_get_request
        github = Github(requester_mock)

        expected = self.fake_request_response
        actual = github.get_issue_list('a', 'b')

        self.assertEqual(expected, actual)

    def test_get_issue_list_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.fake_get_request_with_error

        github = Github(requester_mock)

        expected_false = github.get_issue_list('a', 'b')

        self.assertFalse(expected_false)

    def test_get_issues_description(self):
        self.fail('Not yet implemented')

    def test_get_issues_description_error_request(self):
        self.fail('Not yet implemented')
