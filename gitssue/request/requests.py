"""
Concrete implementation requests_interface, using "requests" module.
"""
from request.request_interface import RequestInterface
import requests
import json
from gitssue.request.unsuccessful_request_exception import UnsuccessfulRequestException


class Requests(RequestInterface):

    TIMEOUT = 2.0

    def get_request(self, request):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response JSON object; False if the HTTP status code distinct to 200.
        """
        response = requests.get(request, timeout=self.TIMEOUT)

        if response.status_code != 200:
            raise UnsuccessfulRequestException(request.status_code, request.headers)

        response_object = json.loads(response.text)
        response.close()

        return response_object
