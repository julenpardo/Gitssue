import unittest
from unittest import mock
from gitssue.remote.bitbucket import Bitbucket
from gitssue.request.unsuccessful_http_request_exception \
        import UnsuccessfulHttpRequestException


class BitbucketTest(unittest.TestCase):

    mocked_request_response = None

    def mock_request(self, method, request, credentials={}, extra_headers={}):
        return self.mocked_request_response

    def mock_request_with_error(self, method, request, credentials={}):
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
        requester_mock.request = self.mock_request
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
        requester_mock.request = self.mock_request_with_error

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = []
        actual = bitbucket.get_issue_list('username', 'repo')

        self.assertEqual(expected, actual)

    def test_get_issues_description(self):
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
        requester_mock.request = self.mock_request
        bitbucket = Bitbucket(requester_mock, {})

        expected = [
            {
                'number': 1,
                'description': {
                    'title': 'first issue',
                    'body': 'first issue body',
                },
                'labels': [{
                    'name': 'task',
                    'color': 'ffffff',
                }],
            },
            {
                'number': 3,
                'description': {
                    'title': 'third issue',
                    'body': 'third issue body',
                },
                'labels': [{
                    'name': 'proposal',
                    'color': 'ffffff',
                }],
            },
        ], [4, 15]
        actual = bitbucket.get_issues_description(
            'username', 'repo', [1, 3, 4, 15]
        )

        self.assertEqual(expected, actual)

    def test_get_issues_description_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request_with_error

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = [], []
        actual = bitbucket.get_issues_description('username', 'repo', ['1', '2'])

        self.assertEqual(expected, actual)

    def test_get_issue_comments(self):
        mocked_issue_list = {
            'values': [
                {
                    'user': {
                        'username': 'julenpardo',
                    },
                    'content': {
                        'raw': 'issue first comment',
                    },
                    'created_on': '2018-06-06T13:01:58.224116+00:00',
                    'updated_on': 'null',
                },
                {
                    'user': {
                        'username': 'julenpardo',
                    },
                    'content': {
                        'raw': 'issue second comment',
                    },
                    'created_on': '2018-06-06T14:01:58.224116+00:00',
                    'updated_on': 'null',
                },
            ]
        }
        self.mocked_request_response = mocked_issue_list
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request
        bitbucket = Bitbucket(requester_mock, {})

        expected = [
            {
                'author': 'julenpardo',
                'created_at': '2018-06-06T13:01:58.224116+00:00',
                'updated_at': 'null',
                'body': 'issue first comment',
            },
            {
                'author': 'julenpardo',
                'created_at': '2018-06-06T14:01:58.224116+00:00',
                'updated_at': 'null',
                'body': 'issue second comment',
            },
        ]
        actual = bitbucket.get_issue_comments('username', 'repo', 1)

        self.assertEqual(expected, actual)

    def test_get_issue_comments_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request_with_error

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = []
        actual = bitbucket.get_issue_comments('username', 'repo', '154')

        self.assertEqual(expected, actual)

    def test_get_rate_information(self):
        """
        The Gitlab API doesn't have a rate limit, so everything is set to -1.
        """

        requester_mock = mock.Mock()
        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = -1, -1, -1
        actual = bitbucket.get_rate_information()

        self.assertEqual(expected, actual)

    def test_parse_request_exception_issue_not_found(self):
        exception = UnsuccessfulHttpRequestException(404, {})

        requester_mock = mock.Mock()
        bitbucket = Bitbucket(requester_mock, credentials={})

        input_issues = ['4', '71']

        expected = "The following issue(s) couldn't be found: {0}".\
            format(', '.join(input_issues))
        actual= bitbucket.parse_request_exception(exception, input_issues)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_generic_error(self):
        exception = UnsuccessfulHttpRequestException(404, {})

        requester_mock = mock.Mock()
        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = 'An error occurred in the request.'
        actual= bitbucket.parse_request_exception(exception)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_invalid_credentials(self):
        exception_code = 401
        input_exception = UnsuccessfulHttpRequestException(exception_code, {})

        requester_mock = mock.Mock()
        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = "Invalid credentials. Check your '.gitssuerc' config file."
        actual = bitbucket.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)
