""" Github module. """

import json
import requests
from remote_repo_interface import RemoteRepoInterface


class Github(RemoteRepoInterface):
    """
    Github specific module.
    """

    API_URL = 'https://api.github.com'

    def get_request(self, request):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response JSON object; False if the HTTP status code distinct to 200.
        """
        response = requests.get(self.API_URL + request)
        response_object = json.loads(response.text)
        response.close()

        return response_object

    def get_issue_list(self, username, repository, show_all=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        request = '/repos/{0}/{1}/issues'.format(username, repository)

        if show_all:
            request += '?state=all'

        issues = self.get_request(request)

        return {
            issue['number']: issue['title'] for issue in issues
        }

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue id.
        """
        issues_descriptions = []

        for issue_number in issue_numbers:
            request = '/repos/{0}/{1}/issues/{2}'.format(
                username,
                repository,
                issue_number
            )

            full_issue = self.get_request(request)

            issue_description = {
                'number': issue_number,
                'description': {
                    'title': full_issue['title'],
                    'body': full_issue['body'],
                }
            }

            issues_descriptions.append(issue_description)

        return issues_descriptions
