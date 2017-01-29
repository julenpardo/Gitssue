""" Dependency injection. """
from github import Github
from shell_wrapper import ShellWrapper


class Dependencies:

    remote = Github()

    shell = ShellWrapper()
