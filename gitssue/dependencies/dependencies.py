""" Dependency injection. """
from gitssue.request.requests import Requests

from gitssue.git.shell_wrapper import ShellWrapper
from gitssue.git.git_wrapper import GitWrapper
from gitssue.printer.colorconsole_color_printer import ColorConsoleColorPrinter
from gitssue.printer.printer import Printer
from gitssue.remote.github import Github
from gitssue.remote.gitlab import Gitlab
from gitssue.config import config_reader


class Dependencies:
    """
    Dependency injection.
    """

    requester = Requests()

    remote = Gitlab(requester, config_reader.get_config())

    shell = ShellWrapper()

    git_wrapper = GitWrapper(shell)

    color_printer = ColorConsoleColorPrinter()

    printer = Printer(color_printer)
