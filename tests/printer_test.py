import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
import contextlib
from io import StringIO
from printer.printer import Printer


class PrinterTest(unittest.TestCase):

    def setUp(self):
        self.printer = Printer()

    def test_print_issue_list(self):
        issues_input = {
            '1': 'first issue',
            '2': 'second issue',
            '3': 'third and last issue'
        }

        expected = ''

        for number, label in sorted(issues_input.items()):
            expected += '#{0}: {1}\n'.format(number, label)

        expected = expected[:-1]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list(issues_input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_empty_dict(self):
        expected = 'No issue could be found.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list({})

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_with_desc(self):
        issues_input = [{
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

        expected = ''
        for issue in issues_input:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['description']['title'])
            expected += '{0}\n'.format(issue['description']['body'])
            expected += '-----------------------------------\n\n'
        expected = expected[:-2]

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list_with_desc(issues_input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    def test_print_issue_list_empty_dict(self):
        expected = 'No issue could be found.'

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.printer.print_issue_list_with_desc({})

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)
