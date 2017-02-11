"""
The interface the concrete printer will have to implement.
"""
from abc import ABCMeta, abstractmethod


class PrinterInterface(metaclass=ABCMeta):
    """
    The interface the concrete printer will have to implement.
    """

    @abstractmethod
    def print_issue_list(self, issues):
        """
        Prints the issue list.
        :param issues: The issue list.
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
    def print_issue_list_with_labels(self, issues):
        """
        Prints the issue list with labels.
        :param issues: the issue list.
        """

    @abstractmethod
    def print_issue_comment_thread(self, comment_thread):
        """
        Prints the given comment thread belonging to the issue.
        :param comment_thread: the thread of comments.
        """
        pass
