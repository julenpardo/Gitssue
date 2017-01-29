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
