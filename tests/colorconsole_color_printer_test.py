import unittest
from unittest import mock
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import contextlib
from io import StringIO
from gitssue.printer.colorconsole_color_printer import ColorConsoleColorPrinter


class ColorConsoleColorPrinterTest(unittest.TestCase):

    @mock.patch('colorconsole.terminal.get_terminal')
    def test_print_colored_line(self, get_terminal_mock):
        get_terminal_mock.return_value = mock.Mock()

        input = 'This is a line.'
        hex_color = 'abcdef'

        expected = input

        color_printer = ColorConsoleColorPrinter()

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            color_printer.print_colored_line(input, hex_color)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)

    @mock.patch('colorconsole.terminal.get_terminal')
    def test_print_labels(self, get_terminal_mock):
        get_terminal_mock.return_value = mock.Mock()

        input = [
            {
                'name': 'label_1',
                'color': 'abcdef',
            },
            {
                'name': 'label_2',
                'color': 'f0f0f0',
            }
        ]

        expected = 'label_1 label_2'

        color_printer = ColorConsoleColorPrinter()

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            color_printer.print_labels(input)

        actual = temp_stdout.getvalue().strip()

        self.assertEqual(expected, actual)
