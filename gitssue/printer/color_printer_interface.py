"""
The interface the concrete color printer will have to implement.
"""
from abc import ABCMeta, abstractmethod


class ColorPrinterInterface(metaclass=ABCMeta):
    """
    The interface the concrete color printer will have to implement.
    """

    @abstractmethod
    def print_colored_line(self, line, hex_color='ffffff'):
        """
        Prints the given line with the given color. After printing it, it must
        reset the color.
        :param line: The line to print.
        :param hex_color: The color of the line to print.
        """
        pass
