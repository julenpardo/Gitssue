""" Dependency injection. """
from remote.dummy import Dummy
from remote.github import Github
from shell_wrapper import ShellWrapper
from printer.printer import Printer
from printer.colorconsole_color_printer import ColorConsoleColorPrinter
from request.requests import Requests


class Dependencies:
    """
    Dependency injection.
    """

    requester = Requests()

    remote = Dummy(requester)

    shell = ShellWrapper()

    color_printer = ColorConsoleColorPrinter()

    printer = Printer(color_printer)
