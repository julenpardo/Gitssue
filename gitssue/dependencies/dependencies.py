""" Dependency injection. """
from gitssue.request.requests import Requests

from gitssue.git.shell_wrapper import ShellWrapper
from gitssue.printer.colorconsole_color_printer import ColorConsoleColorPrinter
from gitssue.printer.printer import Printer
from gitssue.remote.github import Github


class Dependencies:
    """
    Dependency injection.
    """

    requester = Requests()

    remote = Github(requester)

    shell = ShellWrapper()

    color_printer = ColorConsoleColorPrinter()

    printer = Printer(color_printer)
