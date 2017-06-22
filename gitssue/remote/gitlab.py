""" Gitlab module. """
from gitssue.remote.remote_repo_interface import RemoteRepoInterface
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class Gitlab(RemoteRepoInterface):
    """
    Github specific module.
    """

    API_VERSION = 'v4'
    API_URL = 'https://gitlab.com/api/{0}'.format(API_VERSION)

    def __init__(self, requester, credentials):
        super(Gitlab, self).__init__(
            requester,
            auth_token=credentials['gitlab']['token']
        )

    def get_issue_list(self, username, repository, show_all=False,
                       get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        request = '{0}/issues'.format(self.API_URL)

        if show_all:
            request += '?state=all'

        auth_token_header = {'PRIVATE-TOKEN': self.auth_token}
        response_issues = self.requester.get_request(
            request,
            extra_headers=auth_token_header
        )

        issue_list = []
        description = ''

        if response_issues:
            project_id = self.get_project_id(username, repository)

            for issue in response_issues:
                if get_description:
                    description = issue['description']

                issue_labels = []
                labels_info = self.get_labels(
                    project_id,
                    auth_token_header
                )

                for label in issue['labels']:
                    color = '#ffffff'

                    for label_info in labels_info:
                        if label_info['name'] == label:
                            color = label_info['color']

                    issue_labels.append({
                        'name': label,
                        'color': color.replace('#', '')
                    })

                issue_list.append({
                    'number': issue['iid'],
                    'title': issue['title'],
                    'labels': issue_labels,
                    'description': description,
                })

        return issue_list

    def get_labels(self, project_id, auth_token_header):
        labels_request = '{0}/projects/{1}/labels'.format(
            self.API_URL,
            project_id
        )

        labels_info = self.requester.get_request(
            labels_request,
            extra_headers=auth_token_header
        )

        return labels_info

    def get_project_id(self, username, password):
        project_request = '{0}/projects/{1}%2F{2}'.format(
            self.API_URL,
            username,
            password
        )

        project = self.requester.get_request(project_request)

        return project['id']

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue id.
        """
        pass

    def get_issue_comments(self, username, repository, issue_number):
        """
        Gets the comments made in the issue ticket.
        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_number: the issue number to query the comments to.
        """
        pass

    def get_rate_information(self):
        """
        Gets the GitHub API rate information (remaining requests, reset time, etc.).
        requests, the limit is 60 requests/hour. For authenticated ones, 5000/hour.
        :return: remaining request number.
        """
        pass

    def parse_request_exception(self, exception, issue_numbers=()):
        """
        Parses the generated exception during the request, necessary for special cases,
        e.g., when the API limit is hit.

        @TODO: make messages more specific.
        :param exception: (UnsuccessfulRequestException) The exception object generated in the
            request.
        :param issue_numbers: the issue number(s) that weren't found in the request.
        :return: The error message that will be displayed to the user.
        """
        message = 'An error occurred in the request.'

        return message

