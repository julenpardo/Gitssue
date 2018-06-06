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

    def __init__(self, requester, credentials):
        super(Bitbucket, self).__init__(requester, credentials.get('github', {}))

    def get_issue_list(self, username, repository, show_all=False,
                       get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        request = '{0}/repositories/{1}/{2}/issues'.format(
            self.API_URL, username, repository)

        issue_list = []
        response_issues = self.requester.get_request(request)

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

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue
            id.
        """
        request = '{0}/repositories/{1}/{2}/issues'.format(
            self.API_URL, username, repository)

        issue_list = []
        not_found_issues = []

        response_issues = self.requester.get_request(request)

        if response_issues:
            filtered_issues = list(filter(
                lambda issue: str(issue['id']) in issue_numbers,
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
        """
        pass

    def get_rate_information(self):
        """
        Gets the GitHub API rate information (remaining requests, reset time,
        etc.) requests, the limit is 60 requests/hour. For authenticated ones,
        5000/hour.
        :return: remaining request number.
        """
        pass

    def parse_request_exception(self, exception, issue_numbers=()):
        """
        Parses the generated exception during the request, necessary for
        special cases,
        e.g., when the API limit is hit.

        @TODO: make messages more specific.
        :param exception: (UnsuccessfulRequestException) The exception object
            generated in the request.
        :param issue_numbers: the issue number(s) that weren't found in the
            request.
        :return: The error message that will be displayed to the user.
        """
        pass
