"""
The color printer module, implemented with the 'colorconsole' package.
"""
from printer.color_printer_interface import ColorPrinterInterface
from colorconsole import terminal


class ColorConsoleColorPrinter(ColorPrinterInterface):

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
