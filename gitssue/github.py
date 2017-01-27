""" Github module. """

import json
import requests

API_URL = 'https://api.github.com'


def get_request(request):
    """
    Executes a GET request.
    :param request: the GET request to execute.
    :return: response JSON object; False if the HTTP status code distinct to 200.
    """
    response = requests.get(API_URL + request)
    response_object = json.loads(response.text)
    response.close()

    return response_object


def get_issue_list(username, repository):
    """
    Gets the open issue list of the given repository of the
    given user.
    :param username: the user owning the repository.
    :param repository: the repository to look the issues at.
    :return: a dictionary id:label format.
    """
    request = '/repos/{0}/{1}/issues'.format(username, repository)

    issues = get_request(request)

    return {
        issue['number']: issue['title'] for issue in issues
    }
