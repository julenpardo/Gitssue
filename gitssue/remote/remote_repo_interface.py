"""
The interface the concrete repo modules (Github, Gitlab, etc.) will have
to implement.
"""
from abc import ABCMeta, abstractmethod


class RemoteRepoInterface(metaclass=ABCMeta):
    """
    The interface the concrete repo modules (Github, Gitlab, etc.) will have
    to implement.
    """

    def __init__(self, requester, credentials='', auth_token=''):
        self.requester = requester
        self.credentials = credentials
        self.auth_token = auth_token

    @abstractmethod
    def get_issue_list(self, username, repository, show_all=False,
                       get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        :return: a dictionary id:label format.
        """
        pass

    @abstractmethod
    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        In this case, the UnsuccessfulHttpRequestException is handled here and
        not in the controller, because it expects the not_found_issues as
        return value, since it may happen that we have both found and not found
        issues.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        :return: a dictionary with the title and the body message of each
            issue id.
        """
        pass

    @abstractmethod
    def get_issue_comments(self, username, repository, issue_number):
        """
        Gets the comments made in the issue ticket.
        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_number: the issue number to query the comments to.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        :return: the comments.
        """

    @abstractmethod
    def close_issues(self, username, repository, issue_numbers):
        """
        Closes the specified issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issues to close.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        pass

    @abstractmethod
    def create_comment(self, username, repository, issue, comment):
        """
        Creates a comment in the specified issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue: the issue to add the comment to.
        :param comment: the comment to add.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """

    @abstractmethod
    def get_rate_information(self):
        """
        Gets the API rate information (remaining requests, reset time, etc.).
        :return: The remaining requests.
        """
        pass

    @abstractmethod
    def parse_request_exception(self, exception):
        """
        Handles the error occurred during the request.
        :param exception:
        :return:
        """
        pass
