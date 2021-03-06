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

    HTTP_ERROR_MESSAGES = {
        401: 'Authentication error: no credentials/auth token were provided, '
             'or they are invalid. Check your .gitssuerc file and the '
             'documentation.',
        403: 'Permission error: you are not authorized to do that. Check your '
             'credentials/auth token in your .gitssuerc, and your permissions '
             'in the remote repository.',
        404: 'The issue(s) do(es)n\'t exist; or the repository doesn\'t '
             'exist; or it exists but it\'s private, and the credentials '
             'haven\'t been set in the config file. Check your .gitssuerc and '
             'the documentation.',
    }

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
        pass

    @abstractmethod
    def create_issue(self, username, repository, title, body='', labels=None,
                     milestone=False):
        """
        Creates an issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param title: the issue title.
        :param body: the issue body.
        :param labels: list of labels to associate with the issue.
        :param milestone: milestone number to associate the issue with.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        pass

    @abstractmethod
    def get_rate_information(self):
        """
        Gets the API rate information (remaining requests, reset time, etc.).
        :return: The remaining requests.
        """
        pass

    def parse_request_exception(self, exception, milestone=0):
        """
        Parses the error occurred during the request.
        :param exception:
        """
        return self.HTTP_ERROR_MESSAGES[exception.code]
