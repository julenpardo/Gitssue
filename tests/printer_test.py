import unittest
import contextlib
import time
from datetime import datetime
from io import StringIO
from gitssue.printer.printer import Printer
from gitssue.printer.color_printer_interface import ColorPrinterInterface


class DummyColorPrinter(ColorPrinterInterface):
    def print_colored_line(self, line, hex_color='ffffff'):
        print(line)

    def print_labels(self, labels):
        label_string = ''
        for label in labels:
            label_string += '{0} '.format(label['name'])

        label_string = label_string[:-1]
        print(label_string)

class PrinterTest(unittest.TestCase):

    def setUp(self):
        color_printer = DummyColorPrinter()
        self.printer = Printer(color_printer)

    def test_print_issue_list_empty_dict(self):
        expected = 'No issue could be found.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list({})

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_no_description(self):
        issues_input = [
            {
                'number': '1',
                'title': 'First issue title',
            },
            {
                'number': '2',
                'title': 'Second issue title',
            }
        ]

        expected = ''
        for issue in issues_input:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['title'])
            expected += '\n\n'

        expected = expected[:-3]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list(issues_input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_passing_description(self):
        issues_input = [
            {
                'number': '1',
                'title': 'First issue title',
                'description': 'Description of first issue',
            },
            {
                'number': '2',
                'title': 'Second issue title',
                'description': 'Description of second issue',
            }
        ]

        expected = ''
        for issue in issues_input:
            expected += '#{0}: {1}\n\n'.format(issue['number'], issue['title'])
            expected += '{0}\n'.format(issue['description'])
            expected += '\n'

        expected = expected[:-2]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list(issues_input, True)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_with_desc_empty_dict(self):
        expected = 'No issue could be found.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list_with_desc({})

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_with_desc(self):
        issues_input = [
            {
                'number': '1',
                'description': {
                    'title': 'first issue',
                    'body': 'body of first issue',
                },
                'labels': [
                    {
                        'name': 'some label',
                    }
                ]
            },
            {
                'number': '2',
                'description': {
                    'title': 'second issue',
                    'body': 'body of second issue',
                }
            }
        ]

        expected = ''
        for issue in issues_input:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['description']['title'])
            if issue.get('labels'):

                for label in issue.get('labels'):
                    expected += '{0} '.format(label['name'])
                expected = expected[:-1]
                expected += '\n'

            expected += '{0}\n'.format(issue['description']['body'])
            expected += '\n\n'

        expected = expected[:-3]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list_with_desc(issues_input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_comment_thread(self):
        comments_input = [
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
        expected = 'Author: Julen Pardo\n'
        expected += 'Date: Right now\n'
        expected += '\nthis is the first comment\n'
        expected += '\n\nAuthor: Pardo, Julen\n'
        expected += 'Date: A bit later\n'
        expected += '\nthis is the second and last comment'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_comment_thread(comments_input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_comment_thread_no_comment(self):
        expected = 'No comment could be found.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_comment_thread(())

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_error(self):
        input = 'this is an error.'
        expected = 'Error\n'
        expected += 'this is an error.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_error(input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_rate_information(self):
        limit = 60
        remaining = 55
        reset = time.time()

        expected = 'Limit: {0}\n'.format(limit)
        expected += 'Remaining: {0}\n'.format(remaining)
        expected += 'Reset datetime: {0}'.format(datetime.fromtimestamp(reset))

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_rate_information(limit, remaining, reset)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_rate_information_unlimited(self):
        limit = 60
        remaining = 55
        reset = time.time()
        unlimited = True

        expected = 'There is no rate limit for this API.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_rate_information(
                limit,
                remaining,
                reset,
                unlimited
            )

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_created_comment(self):
        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_created_comment(27)

        expected = 'The comment has been created for the issue #27.'
        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_created_issue(self):
        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_created_issue(41)

        expected = 'The issue has been created as #41.'
        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)
