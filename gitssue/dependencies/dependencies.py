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

        self.remote = self.get_remote_instance(remote_domain)

    def get_remote_instance(self, remote_domain):
        config = config_reader.get_config()

        if remote_domain == 'github.com':
            credentials = config.get('github.com', {})
            remote = Github(self.requester, credentials=credentials)

        elif remote_domain == 'bitbucket.org':
            remote = Bitbucket(self.requester, config_reader.get_config())

        else:
            auth_token = config[remote_domain]['token']
            remote = Gitlab(self.requester, auth_token, remote_domain)

        return remote
