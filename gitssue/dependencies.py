""" Dependency injection. """
from remote.github import Github
from shell_wrapper import ShellWrapper
from printer.printer import Printer


class Dependencies:

    remote = Github()

    shell = ShellWrapper()

    printer = Printer()
