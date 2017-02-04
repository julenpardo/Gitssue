import unittest
from unittest import mock
import sys, os
sys.path.append(os.path.abspath('..'))
from gitssue.remote.github import Github


class GithubTest(unittest.TestCase):

    mocked_request_response = []

    def mock_get_request(self, request):
        return self.mocked_request_response

    def mock_get_request_with_error(self, request):
        return False

    def test_get_issue_list(self):
        mocked_return = [
            {
                'number': '1',
                'title': 'first fake issue',
                'labels': [{
                    'name': 'fake label 1',
                    'color': 'ffffff'
                }, {
                    'name': 'fake label 2',
                    'color': 'aaaaaa'
                },
                ],
                'body': 'fake body 1',
            },
        ]
        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request
        github = Github(requester_mock)

        expected = self.mocked_request_response
        actual = github.get_issue_list('a', 'b')

        for index, element in enumerate(expected):
            expected_element = expected[index]
            actual_element = actual[index]

            self.assertEqual(expected_element['number'], actual_element['number'])
            self.assertEqual(expected_element['title'], actual_element['title'])
            self.assertEqual(expected_element['labels'], actual_element['labels'])

    def test_get_issue_list_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request_with_error

        github = Github(requester_mock)

        expected_false = github.get_issue_list('a', 'b')

        self.assertFalse(expected_false)

    def test_get_issues_description(self):
        mocked_return = {
            'number': '1',
            'title': 'first fake issue',
            'body': 'fake body 1',
        }
        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request
        github = Github(requester_mock)

        expected = self.mocked_request_response
        actual = github.get_issues_description('a', 'b', ['1'])

        self.assertEqual(
            expected['number'],
            actual[0]['number'],
        )
        self.assertEqual(
            expected['title'],
            actual[0]['description']['title']
        )
        self.assertEqual(
            expected['body'],
            actual[0]['description']['body']
        )

    def test_get_issues_description_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request_with_error

        github = Github(requester_mock)

        expected_false = github.get_issues_description('a', 'b', [])

        self.assertFalse(expected_false)

    def test_get_issue_comments(self):
        mocked_return = [
            {
                'user': {
                    'login': 'julenpardo'
                },
                'created_at': 'now',
                'updated_at': 'now',
                'body': 'this is a comment for some issue.',
            }
        ]
        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        github = Github(requester_mock)

        expected = mocked_return[0]
        actual = github.get_issue_comments('a', 'b', 1)[0]

        self.assertEqual(
            expected['user']['login'],
            actual['author']
        )
        self.assertEqual(
            expected['created_at'],
            actual['created_at']
        )
        self.assertEqual(
            expected['updated_at'],
            actual['updated_at']
        )
        self.assertEqual(
            expected['body'],
            actual['body']
        )

    def test_get_issue_comments_no_comments(self):
        mocked_return = []
        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        github = Github(requester_mock)

        actual_expected_empty_list = github.get_issue_comments('a', 'b', 1)

        self.assertFalse(actual_expected_empty_list)
