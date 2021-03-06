import unittest
from unittest import mock
from gitssue.remote.bitbucket import Bitbucket
from gitssue.request.unsuccessful_http_request_exception \
        import UnsuccessfulHttpRequestException


class BitbucketTest(unittest.TestCase):

    mocked_request_response = None

    def mock_request(self, method, request, credentials={}, extra_headers={},
                     json_payload={}):
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

    def test_close_comments(self):
        def side_effect(*args, **kwargs):
            existing_closed_issues = {
                1: {
                    'number': 1,
                    'title': 'First closed issue',
                },
                2: {
                    'number': 2,
                    'title': 'Second closed issue',
                },
            }
            request_issue_id = int(args[1][-1:])

            if request_issue_id in existing_closed_issues:
                return existing_closed_issues[request_issue_id]
            else:
                raise UnsuccessfulHttpRequestException(404, {})

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect

        input_issues = [1, 2, 3]

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = [
            {
                'number': 1,
                'title': 'First closed issue'
            },
            {
                'number': 2,
                'title': 'Second closed issue'
            },
        ], [
            3
        ]
        actual = bitbucket.close_issues('username', 'repo', input_issues)

        self.assertEqual(expected, actual)

    def test_close_comments_exception_authentication(self):
        """401"""
        requester_mock = mock.Mock()
        requester_mock.request.side_effect = \
            UnsuccessfulHttpRequestException(401, {})

        bitbucket = Bitbucket(requester_mock, credentials={})

        with self.assertRaises(UnsuccessfulHttpRequestException):
            bitbucket.close_issues('username', 'repo', [1, 2, 3])

    def test_create_comment(self):
        """401"""
        requester_mock = mock.Mock()

        bitbucket = Bitbucket(requester_mock, credentials={})

        try:
            bitbucket.create_comment('username', 'repository', 1, 'comment')
        except:
            self.fail('Unexpected exception')

    def test_create_issue(self):
        mocked_return = {
            'id': 73,
        }

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = 73
        actual = bitbucket.create_issue('username', 'repo', 'title', 'body')

        self.assertEqual(expected, actual)

    def test_create_issue_with_label(self):
        mocked_return = {
            'id': 24,
        }

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request

        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = 24
        actual = bitbucket.create_issue('username', 'repo', 'title', 'body',
                                        ['enhancement'])

        self.assertEqual(expected, actual)

    def test_parse_request_super(self):
        exception_code = 403
        input_exception = UnsuccessfulHttpRequestException(exception_code, {})

        requester_mock = mock.Mock()
        bitbucket = Bitbucket(requester_mock, credentials={})

        expected = Bitbucket.HTTP_ERROR_MESSAGES[403]
        actual = bitbucket.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)
