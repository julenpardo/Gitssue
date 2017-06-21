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
            labels_request = '{0}/projects/{1}/labels'.format(
                self.API_URL,
                response_issues[0]['project_id']
            )
            labels_info = self.requester.get_request(
                labels_request,
                extra_headers=auth_token_header
            )

            for issue in response_issues:
                if get_description:
                    description = issue['description']

                issue_labels = []
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

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue id.
        """
        issues_descriptions = []
        not_found_issues = []

        if issue_numbers:
            for issue_number in issue_numbers:
                request = '{0}/repos/{1}/{2}/issues/{3}'.format(
                    self.API_URL,
                    username,
                    repository,
                    issue_number
                )

                try:
                    full_issue = self.requester.get_request(request)

                    issue_description = {
                        'number': issue_number,
                        'labels': full_issue.get('labels'),
                        'description': {
                            'title': full_issue['title'],
                            'body': full_issue['body'],
                        }
                    }

                    issues_descriptions.append(issue_description)
                except UnsuccessfulHttpRequestException as unsuccessful_request:
                    if unsuccessful_request.code == 404:
                        not_found_issues.append(issue_number)

        return issues_descriptions, not_found_issues

    def get_issue_comments(self, username, repository, issue_number):
        """
        Gets the comments made in the issue ticket.
        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_number: the issue number to query the comments to.
        """

        request = '{0}/repos/{1}/{2}/issues/{3}/comments'.format(
            self.API_URL,
            username,
            repository,
            issue_number
        )
        issues_comments = []

        response_comments = self.requester.get_request(request)
        if response_comments:
            for comment in response_comments:
                issues_comments.append({
                    'author': comment['user']['login'],
                    'created_at': comment['created_at'],
                    'updated_at': comment['updated_at'],
                    'body': comment['body'],
                })

        return issues_comments

    def get_rate_information(self):
        """
        Gets the GitHub API rate information (remaining requests, reset time, etc.).
        requests, the limit is 60 requests/hour. For authenticated ones, 5000/hour.
        :return: remaining request number.
        """
        request = '{0}/rate_limit'.format(self.API_URL)

        rate_information = self.requester.get_request(request, self.credentials)

        return rate_information['rate']['limit'],\
            rate_information['rate']['remaining'],\
            rate_information['rate']['reset']

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

        rate_limit_hit = exception.code == 403\
            and exception.headers['X-RateLimit-Remaining'] == '0'

        if rate_limit_hit:
            message = 'GitHub API limit was reached. Read more about this at '\
                      + 'https://developer.github.com/v3/#rate-limiting'
        elif exception.code == 401:
            message = "Invalid credentials. Check your '.gitssuerc' config file."
        elif exception.code == 404 and issue_numbers:
            message = "The following issue(s) couldn't be found: {0}".\
                format(', '.join(issue_numbers))
        elif exception.code == 404:
            message = "The repository doesn't exist; or exists but it's private, and the "\
                      + "credentials haven't been set in the config file. Check the README "\
                      + "for more information."

        return message
