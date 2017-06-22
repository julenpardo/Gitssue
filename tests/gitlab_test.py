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

    mocked_request_response = None

    def mock_get_request(self, request, credentials={}, extra_headers={}):
        return self.mocked_request_response

    def mock_get_request_with_error(self, request, credentials={}):
        return False

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
        pass

    def test_get_labels_auth_token_error(self):
        pass

    def test_get_labels_no_label_found(self):
        pass
