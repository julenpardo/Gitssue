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

    @abstractmethod
    def print_labels(self, labels):
        """
        Prints the label list. Even if they are printed in the same line, we need
        another method because labels can have different colors.
        :param labels: The label dictionary, with the name and the color code.
        """
        pass
