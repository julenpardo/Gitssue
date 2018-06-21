"""
The interface the concrete printer will have to implement.
"""
from abc import ABCMeta, abstractmethod


class PrinterInterface(metaclass=ABCMeta):
    """
    The interface the concrete printer will have to implement.
    """

    @abstractmethod
    def print_issue_list(self, issues, show_description=False):
        """
        Prints the issue list, also with labels, if any.

        :param issues: the issue list.
        :param show_description: if show also the descriptions or not.
        """
        pass

    @abstractmethod
    def print_issue_list_with_desc(self, issues):
        """
        Prints the issue list with descriptions

        :param issues: the issue list.
        """
        pass

    @abstractmethod
    def print_issue_comment_thread(self, comment_thread):
        """
        Prints the given comment thread belonging to the issue.

        :param comment_thread: the thread of comments.
        """
        pass

    @abstractmethod
    def print_closed_issues(self, closed_issues):
        """
        Prints the closed issues.

        :param closed_issues: the closed issues.
        """
        pass

    @abstractmethod
    def print_created_comment(self, issue):
        """
        Prints the created comment of the specified issue.

        :param issue: the issue the comment has been created for.
        :param comment: the comment that has been created.
        """
        pass

    @abstractmethod
    def print_created_issue(self, number):
        """
        Prints the created issue.

        :param number: the issue number.
        """
        pass

    @abstractmethod
    def print_not_found_issues(self, issues):
        """
        Prints the not found issues.

        :param issues: the not found issue numbers.
        """
        pass

    @abstractmethod
    def print_error(self, error):
        """
        Prints an error.

        :param error: The error to print.

        """
        pass

    @abstractmethod
    def print_rate_information(self, limit, remaining, reset):
        """
        Prints the API rate information (remaining requests, reset time, etc.).

        :param limit: rate total limit.
        :param remaining: the remaining requests until the limit.
        :param reset: reset time (Unix timestamp).
        """
        pass
