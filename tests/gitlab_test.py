import unittest
from unittest import mock
from gitssue.remote.gitlab import Gitlab
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class GitlabTest(unittest.TestCase):

    SECRET_TOKEN = 'SECRET_TOKEN'
    CREDENTIALS = {
        'gitlab.com': {
            'token': SECRET_TOKEN
        }
    }
    TOKEN_HEADER = {'PRIVATE-TOKEN': SECRET_TOKEN}

    mocked_request_response = None

    def mock_request(self, method, request, credentials={}, extra_headers={}):
        return self.mocked_request_response

    def mock_request_with_error(self, request, credentials={}):
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
                'project_id': 1,
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
            if args[1].startswith('https://gitlab.com/api/v4/projects/1/issues'):
                return mocked_issue_list
            elif args[1] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            elif args[1] == 'https://gitlab.com/api/v4/projects/1/labels':
                return labels

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect
        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

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
        requester_mock.request = self.mock_request

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = mocked_return['id']
        actual = gitlab._get_project_id('julenpardo', 'gitssue')

        self.assertEqual(expected, actual)

    def test_get_project_id_project_not_found(self):
        requester_mock = mock.Mock()
        requester_mock.request.side_effect = UnsuccessfulHttpRequestException(404, {})

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        with self.assertRaises(UnsuccessfulHttpRequestException):
            gitlab._get_project_id('whatever', 'whatever')

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
        requester_mock.request = self.mock_request

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = mocked_return
        actual = gitlab._get_labels(project_id=1)

        self.assertEqual(expected, actual)

    def test_get_labels_auth_token_error(self):
        requester_mock = mock.Mock()
        requester_mock.request.side_effect = UnsuccessfulHttpRequestException(401, {})

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        with self.assertRaises(UnsuccessfulHttpRequestException):
            gitlab._get_labels(project_id=1)

    def test_get_labels_no_label_found(self):
        mocked_return = []

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = []
        actual = gitlab._get_labels(project_id=1)

        self.assertEqual(expected, actual)

    def test_create_label_list(self):
        mocked_return = [
            {
                'id': 1,
                'name': 'first label',
                'color': '#ffffff',
            }, {
                'id': 2,
                'name': 'second label',
                'color': '#f0f0f0',
            }, {
                'id': 3,
                'name': 'third label but unassigned to the issue',
                'color': '#abcdef',
            }
        ]

        input_issues = {
            'name': 'first issue',
            'labels': [
                'first label', 'second label'
            ]
        }

        self.mocked_request_response = mocked_return
        requester_mock = mock.Mock()
        requester_mock.request = self.mock_request

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = [
            {
                'name': 'first label',
                'color': 'ffffff',
            },
            {
                'name': 'second label',
                'color': 'f0f0f0',
            }
        ]
        actual = gitlab._create_label_list(input_issues, mocked_return)

        self.assertEqual(expected, actual)

    def test_get_issues_description(self):
        project_id = {'id': 1}
        mocked_issue_list = [
            {
                'iid': '1',
                'title': 'first issue',
                'labels': [
                    'bug',
                    'feature'
                ],
                'description': 'first issue description',
            },
            {
                'iid': '3',
                'title': 'third issue',
                'labels': [
                    'feature'
                ],
                'description': 'third issue description',
            },
            {
                'iid': '4',
                'title': 'fourth issue',
                'labels': [
                    'feature'
                ],
                'description': 'fourth but not requested issue',
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
            if args[1] == 'https://gitlab.com/api/v4/projects/1/issues':
                return mocked_issue_list
            elif args[1] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            elif args[1] == 'https://gitlab.com/api/v4/projects/1/labels':
                return labels

        username = 'username'
        repo = 'repo'
        issue_numbers = ['1', '2', '3']

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected_found_issues = [
            {
                'number': '1',
                'labels': [{
                    'name': 'bug',
                    'color': 'f0f0f0',
                }, {
                    'name': 'feature',
                    'color': 'ffffff',
                }],
                'description': {
                    'title': 'first issue',
                    'body': 'first issue description',
                }
            }, {
                'number': '3',
                'labels': [{
                    'name': 'feature',
                    'color': 'ffffff'
                }],
                'description': {
                    'title': 'third issue',
                    'body': 'third issue description',
                }
            }
        ]
        expected_not_found_issues = ['2']
        expected = expected_found_issues, expected_not_found_issues
        actual = gitlab.get_issues_description(username, repo, issue_numbers)

        self.assertEqual(expected, actual)

    def test_get_issues_description_not_found_issue(self):
        project_id = {'id': 1}
        mocked_issue_list = []

        def side_effect(*args, **kwargs):
            # Mock for get_project_id
            if args[1] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            else:
                return mocked_issue_list

        username = 'username'
        repo = 'repo'
        issue_numbers = ['1', '2']

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = [], ['1', '2']
        actual = gitlab.get_issues_description(username, repo, issue_numbers)

        self.assertEqual(expected, actual)

    def test_get_issues_description_not_issue_given(self):
        username = 'username'
        repo = 'repo'
        issue_numbers = []

        requester_mock = mock.Mock()

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = [], []
        actual = gitlab.get_issues_description(username, repo, issue_numbers)

        self.assertEqual(expected, actual)

    def test_get_issue_comments(self):
        project_id = {'id': 1}
        mocked_issue_comments = [
            {
                'author': {'username': 'author 1'},
                'created_at': 'now',
                'updated_at': 'later',
                'body': 'first comment'
            },
            {
                'author': {'username': 'author 1'},
                'created_at': 'later',
                'updated_at': 'even later',
                'body': 'second comment'
            },
        ]

        def side_effect(*args, **kwargs):
            if args[1] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            elif args[1] == 'https://gitlab.com/api/v4/projects/1/issues/1/notes':
                return mocked_issue_comments

        username = 'username'
        repo = 'repo'
        issue_number = 1

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = [
            {
                'author': 'author 1',
                'created_at': 'now',
                'updated_at': 'later',
                'body': 'first comment'
            },
            {
                'author': 'author 1',
                'created_at': 'later',
                'updated_at': 'even later',
                'body': 'second comment'
            },
        ]
        actual = gitlab.get_issue_comments(username, repo, issue_number)

        self.assertEqual(expected, actual)

    def test_get_issue_comments_not_found_issue(self):
        project_id = {'id': 1}
        mocked_issue_comments = []

        def side_effect(*args, **kwargs):
            # Mock for get_project_id
            if args[1] == 'https://gitlab.com/api/v4/projects/username%2Frepo':
                return project_id
            else:
                return mocked_issue_comments

        username = 'username'
        repo = 'repo'
        issue_number = 1

        requester_mock = mock.Mock()
        requester_mock.request.side_effect = side_effect

        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = []
        actual = gitlab.get_issue_comments(username, repo, issue_number)

        self.assertEqual(expected, actual)

    def test_get_issue_comments_no_issue_given(self):
        username = 'username'
        repo = 'repo'
        issue_number = None

        requester_mock = mock.Mock()
        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = []
        actual = gitlab.get_issue_comments(username, repo, issue_number)

        self.assertEqual(expected, actual)

    def test_get_rate_information(self):
        """
        The Gitlab API doesn't have a rate limit, so everything is set to -1.
        """

        requester_mock = mock.Mock()
        gitlab = Gitlab(requester_mock, self.CREDENTIALS, 'gitlab.com')

        expected = -1, -1, -1
        actual = gitlab.get_rate_information()

        self.assertEqual(expected, actual)

    def test_parse_request_exception_generic_error(self):
        exception = UnsuccessfulHttpRequestException(404, {})

        requester_mock = mock.Mock()
        gitlab = Gitlab(requester_mock, credentials={}, domain='gitlab.com')

        expected = 'An error occurred in the request.'
        actual= gitlab.parse_request_exception(exception)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_invalid_credentials(self):
        exception_code = 401
        input_exception = UnsuccessfulHttpRequestException(exception_code, {})

        requester_mock = mock.Mock()
        gitlab = Gitlab(requester_mock, credentials={}, domain='gitlab.com')

        expected = "Invalid auth token. Check your '.gitssuerc' config file."
        actual = gitlab.parse_request_exception(input_exception)

        self.assertEqual(expected, actual)

    def test_parse_request_exception_issue_not_found(self):
        exception = UnsuccessfulHttpRequestException(404, {})

        requester_mock = mock.Mock()
        gitlab = Gitlab(requester_mock, credentials={}, domain='gitlab.com')

        input_issues = ['4', '71']

        expected = "The following issue(s) couldn't be found: {0}".\
            format(', '.join(input_issues))
        actual = gitlab.parse_request_exception(exception, input_issues)

        self.assertEqual(expected, actual)

