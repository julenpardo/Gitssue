""" Dependency injection. """
from remote.dummy import Dummy
from shell_wrapper import ShellWrapper
from printer.printer import Printer
from printer.colorconsole_color_printer import ColorConsoleColorPrinter


class Dependencies:
    """
    Dependency injection.
    """

    remote = Dummy()

    shell = ShellWrapper()

    color_printer = ColorConsoleColorPrinter()

    printer = Printer(color_printer)
