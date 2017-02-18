"""
Concrete implementation requests_interface, using "requests" module.
"""
import json
import requests
from requests.exceptions import RequestException
from request.request_interface import RequestInterface
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class Requests(RequestInterface):
    """
    Concrete implementation requests_interface, using "requests" module.
    """

    TIMEOUT = 2.0

    def get_request(self, request):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response JSON object; False if the HTTP status code distinct to 200.
        """
        try:
            response = requests.get(request, timeout=self.TIMEOUT)
        except RequestException:
            raise

        if response.status_code != 200:
            raise UnsuccessfulHttpRequestException(response.status_code, response.headers)

        response_object = json.loads(response.text)
        response.close()

        return response_object
