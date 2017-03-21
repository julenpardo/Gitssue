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
    def print_error(self, error):
        """
        Prints an error.
        :param error: The error to print.
        """
        pass
