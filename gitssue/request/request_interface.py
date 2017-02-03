"""
The interface the request handler will have to implement.
"""
from abc import ABCMeta, abstractmethod


class RequestInterface(metaclass=ABCMeta):
    """
    The interface the request handler will have to implement.
    """

    @abstractmethod
    def get_request(self, request):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response response.
        """
        pass
