import unittest
from unittest import mock
from requests.exceptions import RequestException
from gitssue.request.requests import Requests
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class RequestsTest(unittest.TestCase):

    def setUp(self):
        self.requests = Requests()

    @mock.patch('requests.request')
    def test_request(self, requests_get_mock):
        response_mock = mock.Mock()
        mocked_return = """
            {
                "field_1": "value_1",
                "field_2": "value_2"
            }
        """
        expected = {
            'field_1': 'value_1',
            'field_2': 'value_2',
        }

        attributes = {
            'status_code': 200,
            'text': mocked_return,
            'close.return_value': None,
        }
        response_mock.configure_mock(**attributes)
        requests_get_mock.return_value = response_mock

        actual = self.requests.request('GET', 'some request')

        self.assertEqual(expected, actual)

    @mock.patch('requests.request')
    def test_request_status_not_200(self, requests_get_mock):
        response_mock = mock.Mock()

        attributes = {
            'status_code': 404,
            'headers': {'header_key': 'header_value'}
        }
        response_mock.configure_mock(**attributes)
        requests_get_mock.return_value = response_mock

        with self.assertRaises(UnsuccessfulHttpRequestException):
            self.requests.request('GET', 'some request')

    @mock.patch('requests.request')
    def test_request_request_exception(self, requests_get_mock):
        requests_get_mock.side_effect = RequestException

        with self.assertRaises(RequestException):
            self.requests.request('GET', 'some request')

    @mock.patch('requests.request')
    def test_request_with_authentication(self, requests_get_mock):
        response_mock = mock.Mock()
        mocked_return = """
            {
                "field_1": "value_1",
                "field_2": "value_2"
            }
        """
        expected = {
            'field_1': 'value_1',
            'field_2': 'value_2',
        }

        attributes = {
            'status_code': 200,
            'text': mocked_return,
            'close.return_value': None,
        }
        response_mock.configure_mock(**attributes)
        requests_get_mock.return_value = response_mock

        credentials = {
            'username': 'whatever',
            'password': 'whatever',
        }
        actual = self.requests.request('GET', 'some request', credentials)

        self.assertEqual(expected, actual)
