""" Bitbucket module. """
from gitssue.remote.remote_repo_interface import RemoteRepoInterface
from gitssue.request.unsuccessful_http_request_exception \
    import UnsuccessfulHttpRequestException


class Bitbucket(RemoteRepoInterface):
    """
    Github specific module.
    """

    API_VERSION = '2.0'
    API_URL = 'https://api.bitbucket.org/{0}'.format(API_VERSION)
    ALLOWED_ISSUE_KINDS = ('bug', 'enhancement', 'proposal', 'task')

    def __init__(self, requester, credentials):
        super(Bitbucket, self).__init__(requester, credentials=credentials)

    def get_issue_list(self, username, repository, show_all=False,
                       get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        :return: a dictionary id:label format.
        """
        request = '{0}/repositories/{1}/{2}/issues'.format(
            self.API_URL, username, repository
        )

        issue_list = []
        response_issues = self.requester.request('GET', request, self.credentials)

        if response_issues:
            for issue in response_issues['values']:
                is_closed = issue['state'] == 'resolved'

                if not is_closed or (is_closed and show_all):
                    issue_list.append({
                        'number': issue['id'],
                        'title': issue['title'],
                        'description': issue['content']['raw'],
                        'labels': [{
                            'name': issue['kind'],
                            'color': 'ffffff'
                        }]
                    })

        return issue_list

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        In this case, the UnsuccessfulHttpRequestException is handled here and
        not in the controller, because it expects the not_found_issues as
        return value, since it may happen that we have both found and not found
        issues.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        :return: a dictionary with the title and the body message of each issue
            id.
        """
        request = '{0}/repositories/{1}/{2}/issues'.format(
            self.API_URL, username, repository
        )

        issue_list = []
        not_found_issues = []

        response_issues = self.requester.request(
            'GET', request, self.credentials
        )

        if response_issues:
            filtered_issues = list(filter(
                lambda issue: issue['id'] in issue_numbers,
                response_issues['values']
            ))

            for issue in filtered_issues:
                issue_list.append({
                    'number': issue['id'],
                    'description': {
                        'title': issue['title'],
                        'body': issue['content']['raw'],
                    },
                    'labels': [{
                        'name': issue['kind'],
                        'color': 'ffffff'
                    }]
                })

            not_found_issues = [iid for iid in issue_numbers if int(iid) not in
                                [issue['id'] for issue in response_issues['values']]
                               ]

        return issue_list, not_found_issues

    def get_issue_comments(self, username, repository, issue_number):
        """
        Gets the comments made in the issue ticket.
        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_number: the issue number to query the comments to.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        request = '{0}/repositories/{1}/{2}/issues/{3}/comments'.format(
            self.API_URL, username, repository, issue_number
        )

        issue_comments = []
        response_comments = self.requester.request(
            'GET', request, self.credentials
        )

        if response_comments:
            for comment in response_comments['values']:
                issue_comments.append({
                    'author': comment['user']['username'],
                    'created_at': comment['created_on'],
                    'updated_at': comment['updated_on'],
                    'body': comment['content']['raw'],
                })

        return issue_comments

    def close_issues(self, username, repository, issue_numbers):
        """
        Closes the specified issues.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issues: the issue numbers to close.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        base_request = '{0}/repositories/{1}/{2}/issues/'.format(
            self.API_URL, username, repository
        )
        payload = {'state': 'closed'}
        closed_issues = []
        not_found_issues = []

        for issue in issue_numbers:
            request = base_request + str(issue)

            try:
                response_issue = self.requester.request(
                    'PUT', request, self.credentials, json_payload=payload
                )
                closed_issues.append({
                    'number': issue,
                    'title': response_issue['title'],
                })
            except UnsuccessfulHttpRequestException as http_exception:
                if http_exception.code == 404:
                    not_found_issues.append(issue)
                else:
                    raise

        return closed_issues, not_found_issues

    def create_comment(self, username, repository, issue, comment):
        """
        Creates a comment in the specified issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue: the issue to add the comment to.
        :param comment: the comment to add.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        request = '{0}/repositories/{1}/{2}/issues/{3}/comments'.format( self.API_URL, username, repository, issue
        )
        payload = {
            'content': {
                'raw': comment
            }
        }

        self.requester.request(
            'POST', request, self.credentials, json_payload=payload
        )

    def create_issue(self, username, repository, title, body='', labels=None,
                     milestone=0):
        """
        Creates an issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param title: the issue title.
        :param body: the issue body.
        :param labels: the label (a value defined in self.ALLOWED_ISSUE_KINDS).
        :param milestone: milestone number to associate the issue with.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        request = '{0}/repositories/{1}/{2}/issues'.format(
            self.API_URL, username, repository
        )
        payload = {
            'title': title,
            'content': {
                'raw': body,
            },
        }

        if labels:
            payload['kind'] = labels[0]

        response_issue = self.requester.request(
            'POST', request, self.credentials, json_payload=payload
        )

        return response_issue['id']

    def get_rate_information(self):
        """
        The Bitbucket API doesn't have a rate limit for repository queries, so
        we return everything as -1 (the total limit, the remaining requests,
        and the reset time), to let the controller know that it's unlimited.
        :return: everything to -1 to indicate that is unlimited.
        """
        return -1, -1, -1

    def parse_request_exception(self, exception, milestone=0):
        """
        Parses the error occurred during the request.
        :param exception:
        """
        return super().parse_request_exception(exception, milestone)
