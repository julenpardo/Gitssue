"""
The interface the concrete repo modules (Github, Gitlab, etc.) will have to implement.
"""
from abc import ABCMeta, abstractmethod


class RemoteRepoInterface(metaclass=ABCMeta):
    """
    The interface the concrete repo modules (Github, Gitlab, etc.) will have to implement.
    """

    def __init__(self, requester):
        self.requester = requester

    @abstractmethod
    def get_issue_list(self, username, repository, show_all=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        pass

    @abstractmethod
    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue id.
        """
        pass
