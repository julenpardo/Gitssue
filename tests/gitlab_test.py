import unittest
from unittest import mock
from gitssue.remote.gitlab import Gitlab
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class GitlabTest(unittest.TestCase):

    SECRET_TOKEN = 'SECRET_TOKEN'
    CREDENTIALS = {
        'gitlab': {
            'token': SECRET_TOKEN
        }
    }
    TOKEN_HEADER = {'PRIVATE-TOKEN': SECRET_TOKEN}

    mocked_request_response = None

    def mock_get_request(self, request, credentials={}, extra_headers={}):
        return self.mocked_request_response

    def mock_get_request_with_error(self, request, credentials={}):
        return False

    def test_get_issue_list(self):
        project_id = {'id': 1}
        mocked_issue_list = [
            {
                'iid': '1',
                'title': 'first issue',
                'labels': [
                    'bug',
                    'feature'
                ],
                'body': 'body 1',
            },
        ]

        def side_effect(*args, **kwargs):
            labels = [
                {
                    'name': 'bug',
                    'color': '#f0f0f0',
                }, {
                    'name': 'feature',
                    'color': '#ffffff'
                }
            ]
            if args[0] == 'https://gitlab.com/api/v4/issues':
                return mocked_issue_list
            elif args[0] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            elif args[0] == 'https://gitlab.com/api/v4/projects/1/labels':
                return labels

        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = side_effect
        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        expected = [{
            'number': '1',
            'title': 'first issue',
            'labels': [{
                'name': 'bug',
                'color': 'f0f0f0',
            }, {
                'name': 'feature',
                'color': 'ffffff'
            }],
            'description': ''
        }]

        actual = gitlab.get_issue_list('username', 'repo')

        self.assertEqual(expected, actual)

    def test_get_project_id(self):
        mocked_return = {
            'id': 12345,
            'description': 'project description',
            'more_info': 'blablabla',
        }

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        expected = mocked_return['id']
        actual = gitlab.get_project_id('julenpardo', 'gitssue')

        self.assertEqual(expected, actual)

    def test_get_project_id_project_not_found(self):
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(404, {})

        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        with self.assertRaises(UnsuccessfulHttpRequestException):
            gitlab.get_project_id('whatever', 'whatever')

    def test_get_labels(self):
        mocked_return = [{
            'id': 1,
            'name': 'first label',
            'color': '#ffffff',
        }, {
            'id': 2,
            'name': 'second label',
            'color': '#000000',
        }]

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        expected = mocked_return
        actual = gitlab.get_labels(
            project_id=1,
            auth_token_header=self.TOKEN_HEADER
        )

        self.assertEqual(expected, actual)

    def test_get_labels_auth_token_error(self):
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(401, {})

        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        with self.assertRaises(UnsuccessfulHttpRequestException):
            gitlab.get_labels(project_id=1, auth_token_header=self.TOKEN_HEADER)

    def test_get_labels_no_label_found(self):
        mocked_return = []

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        gitlab = Gitlab(requester_mock, credentials=self.CREDENTIALS)

        expected = []
        actual = gitlab.get_labels(
            project_id=1,
            auth_token_header=self.TOKEN_HEADER
        )

        self.assertEqual(expected, actual)
