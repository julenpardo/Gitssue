"""
The color printer module, implemented with the 'colorconsole' package.
"""
from __future__ import print_function
from printer.color_printer_interface import ColorPrinterInterface
from colorconsole import terminal


class ColorConsoleColorPrinter(ColorPrinterInterface):
    """
    The color printer module, implemented with the 'colorconsole' package.
    """

    def __init__(self):
        """
        Gets the screen from the colorconsole.terminal.
        """
        self.screen = terminal.get_terminal(conEmu=False)

    def print_colored_line(self, line, hex_color='ffffff'):
        """
        Prints the given line with the given color, and, then, resetting the color.
        :param line: The line to print.
        :param hex_color: The color of the line to print.
        """
        red, green, blue = list(bytes.fromhex(hex_color))

        self.screen.xterm24bit_set_fg_color(red, green, blue)
        print(line)
        self.screen.reset_colors()

    def print_labels(self, labels):
        """
        Prints the label list. We need another method because labels can have
        different colors.
        :param labels: The label dictionary, with the name and the color code.
        """
        for label in labels:
            red, green, blue = list(bytes.fromhex(label['color']))
            self.screen.xterm24bit_set_fg_color(red, green, blue)
            print(label['name'] + ' ', end='', flush=True)

        print()

        self.screen.reset_colors()
