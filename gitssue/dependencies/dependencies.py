""" Dependency injection. """
from gitssue.request.requests import Requests

from gitssue.git.shell_wrapper import ShellWrapper
from gitssue.git.git_wrapper import GitWrapper
from gitssue.printer.colorconsole_color_printer import ColorConsoleColorPrinter
from gitssue.printer.printer import Printer
from gitssue.remote.github import Github
from gitssue.remote.gitlab import Gitlab
from gitssue.remote.bitbucket import Bitbucket
from gitssue.config import config_reader


class Dependencies:
    """
    Dependency injection.
    """

    def __init__(self):
        self.inject_dependencies()

    def inject_dependencies(self):
        self.shell = ShellWrapper()
        self.git_wrapper = GitWrapper(self.shell)
        self.requester = Requests()
        self.color_printer = ColorConsoleColorPrinter()
        self.printer = Printer(self.color_printer)

        remote_domain = self.git_wrapper.get_remote_domain()

        if remote_domain == 'github.com':
            self.remote = Github(self.requester, config_reader.get_config())
        elif remote_domain == 'bitbucket.org':
            self.remote = Bitbucket(self.requester, config_reader.get_config())
        else:
            self.remote = Gitlab(self.requester, config_reader.get_config())
