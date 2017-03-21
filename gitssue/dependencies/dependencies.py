""" Dependency injection. """
from request.requests import Requests

from git.shell_wrapper import ShellWrapper
from printer.colorconsole_color_printer import ColorConsoleColorPrinter
from printer.printer import Printer
from remote.github import Github


class Dependencies:
    """
    Dependency injection.
    """

    requester = Requests()

    remote = Github(requester)

    shell = ShellWrapper()

    color_printer = ColorConsoleColorPrinter()

    printer = Printer(color_printer)
