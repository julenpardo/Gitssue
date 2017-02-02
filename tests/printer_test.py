import unittest
import sys, os
sys.path.append(os.path.abspath('..'))
import contextlib
from io import StringIO
from gitssue.printer.printer import Printer
from gitssue.printer.color_printer_interface import ColorPrinterInterface


class DummyColorPrinter(ColorPrinterInterface):
    def print_colored_line(self, line, hex_color='ffffff'):
        print(line)

    def print_labels(self, labels):
        print(' '.join(labels))


class PrinterTest(unittest.TestCase):

    def setUp(self):
        color_printer = DummyColorPrinter()
        self.printer = Printer(color_printer)

    def test_print_issue_list(self):
        issues_input = (
            {
                'number': '1',
                'title': 'first issue',
            },
            {
                'number': '2',
                'title': 'second issue',
            },
            {
                'number': '3',
                'title': 'third and last issue',
            },
        )

        expected = ''

        for issue in issues_input:
            expected += '#{0}: {1}\n'.format(issue['number'], issue['title'])

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
            expected += '\n\n'

        expected = expected[:-3]

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
