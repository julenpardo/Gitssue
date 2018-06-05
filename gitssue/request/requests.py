"""
Concrete implementation requests_interface, using "requests" module.
"""
import json
import requests
from requests.exceptions import RequestException
from gitssue.request.request_interface import RequestInterface
from gitssue.request.unsuccessful_http_request_exception \
    import UnsuccessfulHttpRequestException


class Requests(RequestInterface):
    """
    Concrete implementation requests_interface, using "requests" module.
    """

    _TIMEOUT = 40.0

    def get_request(self, request, credentials=None, extra_headers=None):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response JSON object; False if the HTTP status code distinct
            to 200.
        """
        authentication = ()
        headers = {}

        if extra_headers is not None:
            headers = extra_headers

        if credentials is not None and 'username' in credentials \
           and 'password' in credentials:
            authentication = (credentials['username'], credentials['password'])

        try:
            response = requests.get(
                request,
                auth=authentication,
                headers=headers,
                timeout=self._TIMEOUT
            )
        except RequestException:
            raise

        if response.status_code != 200:
            raise UnsuccessfulHttpRequestException(
                response.status_code, response.headers)

        response_object = json.loads(response.text)
        response.close()

        return response_object
