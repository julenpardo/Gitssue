"""
The interface the request handler will have to implement.
"""
from abc import ABCMeta, abstractmethod


class RequestInterface(metaclass=ABCMeta):
    """
    The interface the request handler will have to implement.
    """

    @abstractmethod
    def request(self, method, request, credentials=None, extra_headers=None,
                json_payload=None):
        """
        Executes a request.

        :param request: the GET request to execute.
        :return: response response.
        """
        pass
