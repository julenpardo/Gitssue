import os
import sys
import unittest
import contextlib
from io import StringIO
from unittest import mock
from requests.exceptions import RequestException

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('./gitssue'))

from gitssue.controller.controller import Controller
from gitssue.git.git_wrapper import GitWrapper
from gitssue.dependencies.dependencies import Dependencies
from gitssue.printer.color_printer_interface import ColorPrinterInterface
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException

class DummyColorPrinter(ColorPrinterInterface):
    def print_colored_line(self, line, hex_color='ffffff'):
        print(line)

    def print_labels(self, labels):
        if labels:
            labels_str = ''

            for label in labels:
                labels_str += '{0} '.format(label['name'])

            labels_str = labels_str[:-1]
            print(labels_str)


class ControllerTest(unittest.TestCase):

    mocked_remote_get_issue_list_return = None
    mocked_remote_get_issues_description_return = None
    mocked_remote_get_issue_comments_return = None
    mocked_remote_close_issues_return = None
    mocked_shell_wrapper_execute_command_return = None
    mocked_request_get_request_return = None
    mocked_request_parse_request_exception_return = None
    requester_mock = None

    def dummy(self):
        return None

    def setUp(self):
        self.controller = Controller(Dependencies())
        self.controller.deps.printer.color_printer = DummyColorPrinter()

        shell_wrapper_mock = self._create_shell_wrapper_mock()
        self.controller.deps.shell = shell_wrapper_mock
        self.controller.deps.git_wrapper = GitWrapper(shell_wrapper_mock)
        self.controller.deps.instantiate_remote_instance()


    def _create_shell_wrapper_mock(self):
        def side_effect(*args, **kwargs):
            if args[0] == 'git remote --verbose':
                return  "origin git@github.com:julenpardo/Gitssue.git (fetch)"
            elif args[0] == 'git config --get remote.origin.url':
                return 'git@github.com:julenpardo/gitssue.git'

        shell_wrapper_mock = mock.Mock()
        shell_wrapper_mock.execute_command.side_effect = side_effect

        return shell_wrapper_mock


    def mock_remote_get_issue_list(self, username, repo, all=False, desc=False):
        if self.requester_mock is not None:
            self.requester_mock.get_request(None)

        return self.mocked_remote_get_issue_list_return

    def mock_remote_get_issues_description(self, username, repository, issue_numbers):
        if self.requester_mock is not None:
            self.requester_mock.get_request(None)

        return self.mocked_remote_get_issues_description_return

    def mock_remote_get_issue_comments(self, username, repo, issue_number):
        if self.requester_mock is not None:
            self.requester_mock.get_request(None)

        return self.mocked_remote_get_issue_comments_return

    def mock_remote_close_issues(self, username, repo, issues):
        if self.requester_mock is not None:
            self.requester_mock.get_request(None)

        return self.mocked_remote_close_issues_return

    def mock_shell_wrapper_execute_command(self, command):
        return self.mocked_shell_wrapper_execute_command_return

    def mock_request_get_request(self, request):
        return self.mocked_request_get_request_return

    def mock_remote_parse_request_exception(self, exception, issue_numbers=()):
        return self.mocked_request_parse_request_exception_return

    def mock_remote_get_rate_information(self):
        import time
        return 1, 1, time.time()

    def test_list(self):
        mocked_return = [
            {
                'number': '1',
                'title': 'first issue',
                'labels': [
                    {
                        'name': 'foo',
                        'color': 'ffffff'
                    }
                ]
            },
            {
                'number': '2',
                'title': 'second and last issue',
                'labels': [
                    {
                        'name': 'bar',
                        'color': 'ffffff'
                    },
                    {
                        'name': 'foo',
                        'color': '000000'
                    }
                ]
            },
        ]
        remote_mock = mock.Mock()
        self.mocked_remote_get_issue_list_return = mocked_return
        remote_mock.get_issue_list = self.mock_remote_get_issue_list
        self.controller.deps.remote = remote_mock

        expected = ''

        for issue in mocked_return:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['title'])
            labels = [] if not issue.get('labels') else issue['labels']

            for label in labels:
                expected += '{0} '.format(label['name'])
            expected = expected[:-1]
            expected += '\n\n'

        expected = expected[:-2]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.list()

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_list_request_error(self):
        expected = 'Mocked exception'

        remote_mock = mock.Mock()
        remote_mock.get_issue_list = self.mock_remote_get_issue_list
        self.mocked_request_parse_request_exception_return = expected
        remote_mock.parse_request_exception = self.mock_remote_parse_request_exception
        self.controller.deps.remote = remote_mock
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(400, expected)
        self.requester_mock = requester_mock

        original_requester = self.controller.deps.requester
        self.controller.deps.remote.requester = requester_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.list()
            pass

        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.controller.deps.remote.requester = original_requester

        self.assertEqual(expected, actual)

    def test_list_connection_error(self):
        remote_mock = mock.Mock()
        remote_mock.get_issue_list.side_effect = RequestException
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.list()

        expected = 'A connection error occurred:'
        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.assertEqual(expected, actual)

    def test_list_many_origins(self):
        mocked_shell_wrapper_return = 'origin1 git@github.com:julenpardo/first-remote\n' + \
                                      'origin2 git@github.com:julenpardo/second-remote'
        shell_wrapper_mock = mock.Mock()
        self.mocked_shell_wrapper_execute_command_return = mocked_shell_wrapper_return
        shell_wrapper_mock.execute_command = self.mock_shell_wrapper_execute_command

        original_shell = self.controller.deps.shell
        self.controller.deps.shell = shell_wrapper_mock
        self.controller.deps.git_wrapper = GitWrapper(shell_wrapper_mock)

        expected = 'Error\n'
        expected += 'More than one remote was detected. Gitssue does not offer support for this yet.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.list()

        self.controller.deps.shell = original_shell

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_desc(self):
        mocked_return = [{
            'number': '1',
            'description': {
                'title': 'first issue',
                'body': 'body of first issue',
            }},
            {
            'number': '2',
            'description': {
                'title': 'second issue',
                'body': 'body of second issue',
            }
        }]

        self.mocked_remote_get_issues_description_return = mocked_return, []
        remote_mock = mock.Mock()
        remote_mock.get_issues_description = self.mock_remote_get_issues_description
        self.controller.deps.remote = remote_mock

        expected = ''
        for issue in mocked_return:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['description']['title'])
            expected += '{0}\n'.format(issue['description']['body'])
            expected += '\n\n'

        expected = expected[:-3]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.desc('1')  # We need a number to pass the condition.

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_desc_request_error(self):
        expected = 'Mocked exception'

        remote_mock = mock.Mock()
        remote_mock.get_issues_description = self.mock_remote_get_issues_description
        self.mocked_request_parse_request_exception_return = expected
        remote_mock.parse_request_exception = self.mock_remote_parse_request_exception
        self.controller.deps.remote = remote_mock
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(400, expected)
        self.requester_mock = requester_mock

        original_requester = self.controller.deps.requester
        self.controller.deps.remote.requester = requester_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.desc('1')  # We need a number to pass the first condition.

        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.controller.deps.remote.requester = original_requester

        self.assertEqual(expected, actual)

    def test_desc_connection_error(self):
        remote_mock = mock.Mock()
        remote_mock.get_issues_description.side_effect = RequestException
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.desc('1')

        expected = 'A connection error occurred:'
        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.assertEqual(expected, actual)

    def test_desc_issue_not_found(self):
        not_found_issues = ['1', '2', '3']
        mocked_return = [], not_found_issues

        self.mocked_remote_get_issues_description_return = mocked_return
        remote_mock = mock.Mock()
        remote_mock.get_issues_description = self.mock_remote_get_issues_description
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.desc('1')

        expected = "The following issues couldn't be found: {0}".\
            format(', '.join(not_found_issues))
        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.assertEqual(expected, actual)

    def test_desc_many_origins(self):
        mocked_shell_wrapper_return = 'origin1 git@github.com:julenpardo/first-remote\n' + \
                                      'origin2 git@github.com:julenpardo/second-remote'
        shell_wrapper_mock = mock.Mock()
        self.mocked_shell_wrapper_execute_command_return = mocked_shell_wrapper_return
        shell_wrapper_mock.execute_command = self.mock_shell_wrapper_execute_command

        original_shell = self.controller.deps.shell
        self.controller.deps.shell = shell_wrapper_mock
        self.controller.deps.git_wrapper = GitWrapper(shell_wrapper_mock)

        expected = 'Error\n'
        expected += 'More than one remote was detected. Gitssue does not offer support for this yet.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.desc(None)

        self.controller.deps.shell = original_shell

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_thread(self):
        mocked_return = [
            {
                'author': 'Julen Pardo',
                'created_at': 'Right now',
                'updated_at': 'never',
                'body': 'this is the first comment'
            }, {
                'author': 'Pardo, Julen',
                'created_at': 'A bit later',
                'updated_at': 'never',
                'body': 'this is the second and last comment'
            },
        ]

        self.mocked_remote_get_issue_comments_return = mocked_return
        remote_mock = mock.Mock()
        remote_mock.get_issue_comments = self.mock_remote_get_issue_comments
        self.controller.deps.remote = remote_mock

        expected = 'Author: Julen Pardo\n'
        expected += 'Date: Right now\n'
        expected += '\nthis is the first comment\n'
        expected += '\n\nAuthor: Pardo, Julen\n'
        expected += 'Date: A bit later\n'
        expected += '\nthis is the second and last comment'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.comments('1')  # We need a number to pass the condition.

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_thread_many_origins(self):
        mocked_shell_wrapper_return = 'origin1 git@github.com:julenpardo/first-remote\n' + \
                                      'origin2 git@github.com:julenpardo/second-remote'
        shell_wrapper_mock = mock.Mock()
        self.mocked_shell_wrapper_execute_command_return = mocked_shell_wrapper_return
        shell_wrapper_mock.execute_command = self.mock_shell_wrapper_execute_command

        original_shell = self.controller.deps.shell
        self.controller.deps.shell = shell_wrapper_mock
        self.controller.deps.git_wrapper = GitWrapper(shell_wrapper_mock)

        expected = 'Error\n'
        expected += 'More than one remote was detected. Gitssue does not offer support for this yet.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.comments(None)
            pass

        self.controller.deps.shell = original_shell

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_thread_request_error(self):
        expected = 'Mocked exception'

        remote_mock = mock.Mock()
        remote_mock.get_issue_comments = self.mock_remote_get_issue_comments
        self.mocked_request_parse_request_exception_return = expected
        remote_mock.parse_request_exception = self.mock_remote_parse_request_exception
        self.controller.deps.remote = remote_mock
        requester_mock = mock.Mock()
        requester_mock.get_request.side_effect = UnsuccessfulHttpRequestException(400, expected)
        self.requester_mock = requester_mock

        original_requester = self.controller.deps.requester
        self.controller.deps.remote.requester = requester_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.comments('1')  # We need a number to pass the first condition.
            pass

        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.controller.deps.remote.requester = original_requester

        self.assertEqual(expected, actual)

    def test_thread_connection_error(self):
        remote_mock = mock.Mock()
        remote_mock.get_issue_comments.side_effect = RequestException
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.comments('1')

        expected = 'A connection error occurred:'
        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.assertEqual(expected, actual)

    def test_close(self):
        remote_mocked_return = [
            {
                'number': 1,
                'title': 'First clossed issue',
            },
            {
                'number': 2,
                'title': 'Second closed issue',
            }
        ], []

        self.mocked_remote_close_issues_return = remote_mocked_return
        remote_mock = mock.Mock()
        remote_mock.close_issues = self.mock_remote_close_issues

        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.close([1, 2])

        expected = 'The following issues have been closed:\n\n' \
            + '#1: First clossed issue\n\n' \
            + '#2: Second closed issue'

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_close_with_not_found_issues(self):
        remote_mocked_return = [
            {
                'number': 1,
                'title': 'First clossed issue',
            },
            {
                'number': 2,
                'title': 'Second closed issue',
            }
        ], [
            3
        ]

        self.mocked_remote_close_issues_return = remote_mocked_return
        remote_mock = mock.Mock()
        remote_mock.close_issues = self.mock_remote_close_issues

        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.close([1, 2, 3])

        expected = 'The following issues have been closed:\n\n' \
            + '#1: First clossed issue\n\n' \
            + '#2: Second closed issue\n\n' \
            + 'Error\n' \
            + 'The following issues couldn\'t be found: 3'

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_close_connection_error(self):
        remote_mock = mock.Mock()
        remote_mock.close_issues.side_effect = RequestException
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.close([])

        expected = 'A connection error occurred:'
        actual = temp_stdout.getvalue().strip().splitlines()[2]

        self.assertEqual(expected, actual)

    def test_close_request_error(self):
        expected = 'Mocked exception'

        remote_mock = mock.Mock()

        self.mocked_request_parse_request_exception_return = expected
        remote_mock.parse_request_exception = self.mock_remote_parse_request_exception
        remote_mock.close_issues.side_effect = \
                UnsuccessfulHttpRequestException(401, {})

        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.close([1])

        actual = temp_stdout.getvalue().strip().splitlines()[2]

        self.assertEqual(expected, actual)


    def test_close_many_origins(self):
        mocked_shell_wrapper_return = 'origin1 git@github.com:julenpardo/first-remote\n' + \
                                      'origin2 git@github.com:julenpardo/second-remote'
        shell_wrapper_mock = mock.Mock()
        self.mocked_shell_wrapper_execute_command_return = mocked_shell_wrapper_return
        shell_wrapper_mock.execute_command = self.mock_shell_wrapper_execute_command

        original_shell = self.controller.deps.shell
        self.controller.deps.shell = shell_wrapper_mock
        self.controller.deps.git_wrapper = GitWrapper(shell_wrapper_mock)

        expected = 'Error\n'
        expected += 'More than one remote was detected. Gitssue does not offer support for this yet.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.controller.close([])

        self.controller.deps.shell = original_shell

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_rate_information(self):
        remote_mock = mock.Mock()
        remote_mock.get_rate_information = self.mock_remote_get_rate_information
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        try:
            with contextlib.redirect_stdout(temp_stdout):
                self.controller.rate_information()
        except:
            self.fail('No exception should be thrown.')

    def test_rate_information_request_exception(self):
        remote_mock = mock.Mock()
        remote_mock.get_rate_information.side_effect = RequestException
        self.controller.deps.remote = remote_mock

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.controller.rate_information()

        expected = 'A connection error occurred:'
        actual = temp_stdout.getvalue().strip().splitlines()[1]

        self.assertEqual(expected, actual)
