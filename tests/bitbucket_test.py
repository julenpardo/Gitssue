import unittest
from unittest import mock
from gitssue.remote.bitbucket import Bitbucket
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class BitbucketTest(unittest.TestCase):

    mocked_request_response = None

    def mock_get_request(self, request, credentials={}, extra_headers={}):
        return self.mocked_request_response

    def mock_get_request_with_error(self, request, credentials={}):
        return False

    def test_get_issue_list(self):
        mocked_issue_list = {
            'values': [
                {
                    'id': 1,
                    'kind': 'task',
                    'title': 'first issue',
                    'content': {
                        'raw': 'first issue body',
                    },
                    'state': 'new',
                },
                {
                    'id': 2,
                    'kind': 'proposal',
                    'title': 'second issue',
                    'content': {
                        'raw': 'second issue body',
                    },
                    'state': 'new',
                },
                {
                    'id': 3,
                    'kind': 'proposal',
                    'title': 'third issue',
                    'content': {
                        'raw': 'third issue body',
                    },
                    'state': 'resolved',
                },
            ]
        }
        self.mocked_request_response = mocked_issue_list
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request
        bitbucket = Bitbucket(requester_mock, {})

        expected = [
            {
                'number': 1,
                'title': 'first issue',
                'description': 'first issue body',
                'labels': [{
                    'name': 'task',
                    'color': 'ffffff',
                }],
            },
            {
                'number': 2,
                'title': 'second issue',
                'description': 'second issue body',
                'labels': [{
                    'name': 'proposal',
                    'color': 'ffffff',
                }],

            }
        ]
        actual = bitbucket.get_issue_list('username', 'repo')

        self.assertEqual(expected, actual)

    def test_get_issues_list_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request_with_error

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = []
        actual = bitbucket.get_issue_list('username', 'repo')

        self.assertEqual(expected, actual)
