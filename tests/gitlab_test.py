import unittest
import time
from unittest import mock
from gitssue.remote.github import Github
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class GithubTest(unittest.TestCase):

    mocked_request_response = None

    def mock_get_request(self, request, credentials={}):
        return self.mocked_request_response

    def mock_get_request_with_error(self, request, credentials={}):
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
        github = Github(requester_mock, credentials={})

        expected = self.mocked_request_response
        actual = github.get_issue_list('a', 'b', True)

        for index, element in enumerate(expected):
            expected_element = expected[index]
            actual_element = actual[index]

            self.assertEqual(expected_element['number'], actual_element['number'])
            self.assertEqual(expected_element['title'], actual_element['title'])
            self.assertEqual(expected_element['labels'], actual_element['labels'])

    def test_get_issue_list_error_request(self):
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request_with_error

        github = Github(requester_mock, credentials={})

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
        github = Github(requester_mock, credentials={})

        expected = self.mocked_request_response
        actual, errors_empty = github.get_issues_description('a', 'b', ['1'])

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

        github = Github(requester_mock, credentials={})

        expected = [], []
        actual = github.get_issues_description('a', 'b', [])

        self.assertEqual(expected, actual)

    def test_get_issues_description_not_found_issue(self):
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(404, {})

        github = Github(requester_mock, credentials={})

        issues = ['1', '2', '3']
        expected = [], issues
        actual = github.get_issues_description('username', 'repo', issues)

        self.assertEqual(expected, actual)

    def test_get_issues_description_other_error(self):
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(500, {})

        github = Github(requester_mock, credentials={})

        issues = ['1']
        expected = [], []
        actual = github.get_issues_description('username', 'repo', issues)

        self.assertEqual(expected, actual)

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

        github = Github(requester_mock, credentials={})

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

        github = Github(requester_mock, credentials={})

        actual_expected_empty_list = github.get_issue_comments('a', 'b', 1)

        self.assertFalse(actual_expected_empty_list)

    def test_parse_request_exception_api_limit(self):
        exception_code = 403
        exception_headers = {
            'X-RateLimit-Remaining': '0'
        }
        input_exception = UnsuccessfulHttpRequestException(exception_code, exception_headers)

        requester_mock = mock.Mock()
        github = Github(requester_mock, credentials={})

        expected = 'GitHub API limit was reached. Read more about this at '\
                    + 'https://developer.github.com/v3/#rate-limiting'
        actual = github.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_404(self):
        exception_code = 404
        exception_headers = {
            'X-RateLimit-Remaining': 100
        }
        input_exception = UnsuccessfulHttpRequestException(exception_code, exception_headers)
        not_found_issues = ['1', '2', '3']

        requester_mock = mock.Mock()
        github = Github(requester_mock, credentials={})

        expected = "The following issue(s) couldn't be found: {0}".\
            format(', '.join(not_found_issues))

        actual = github.parse_request_exception(input_exception, not_found_issues)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_other_exception(self):
        exception_code = 403
        exception_headers = {
            'X-RateLimit-Remaining': 1
        }
        input_exception = UnsuccessfulHttpRequestException(exception_code, exception_headers)

        requester_mock = mock.Mock()
        github = Github(requester_mock, credentials={})

        expected = 'An error occurred in the request.'
        actual = github.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_invalid_credentials(self):
        exception_code = 401
        input_exception = UnsuccessfulHttpRequestException(exception_code, {})

        requester_mock = mock.Mock()
        github = Github(requester_mock, credentials={})

        expected = "Invalid credentials. Check your '.gitssuerc' config file."
        actual = github.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)


    def test_parse_request_repo_not_found(self):
        exception_code = 404
        input_exception = UnsuccessfulHttpRequestException(exception_code, {})

        requester_mock = mock.Mock()
        github = Github(requester_mock, credentials={})

        expected = "The repository doesn't exist; or exists but it's private, and the "\
                      + "credentials haven't been set in the config file. Check the README "\
                      + "for more information."
        actual = github.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)

    def test_get_rate_information(self):
        current_timestamp = time.time()
        mocked_return = {
            'rate': {
                'limit': 60,
                'remaining': 55,
                'reset': current_timestamp
            }
        }

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.get_request = self.mock_get_request

        github = Github(requester_mock, credentials={})

        expected = mocked_return['rate']['limit'],\
            mocked_return['rate']['remaining'],\
            mocked_return['rate']['reset']

        actual = github.get_rate_information()

        self.assertEqual(expected, actual)
