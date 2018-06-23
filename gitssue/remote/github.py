""" Github module. """
from gitssue.remote.remote_repo_interface import RemoteRepoInterface
from gitssue.request.unsuccessful_http_request_exception \
    import UnsuccessfulHttpRequestException


class Github(RemoteRepoInterface):
    """
    Github specific module.
    """

    API_URL = 'https://api.github.com'

    def __init__(self, requester, credentials):
        super(Github, self).__init__(requester, credentials=credentials)

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
        request = '{0}/repos/{1}/{2}/issues'.format(
            self.API_URL, username, repository)

        if show_all:
            request += '?state=all'

        response_issues = self.requester.request('GET', request,
                                                 self.credentials)

        issue_list = []
        description = ''

        if response_issues:
            for issue in response_issues:
                if get_description:
                    full_description = self.get_issues_description(
                        username,
                        repository,
                        [issue['number']]
                    )

                    description = full_description[0][0]['description']['body']

                issue_list.append({
                    'number': issue['number'],
                    'title': issue['title'],
                    'labels': issue['labels'],
                    'description': description
                })

        return issue_list

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

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
                    full_issue = self.requester.request('GET', request)

                    issue_description = {
                        'number': issue_number,
                        'labels': full_issue.get('labels'),
                        'description': {
                            'title': full_issue['title'],
                            'body': full_issue['body'],
                        }
                    }

                    issues_descriptions.append(issue_description)
                except UnsuccessfulHttpRequestException as \
                        unsuccessful_request:
                    if unsuccessful_request.code == 404:
                        not_found_issues.append(issue_number)

        return issues_descriptions, not_found_issues

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

        request = '{0}/repos/{1}/{2}/issues/{3}/comments'.format(
            self.API_URL, username, repository, issue_number
        )

        issues_comments = []

        response_comments = self.requester.request('GET', request)
        if response_comments:
            for comment in response_comments:
                issues_comments.append({
                    'author': comment['user']['login'],
                    'created_at': comment['created_at'],
                    'updated_at': comment['updated_at'],
                    'body': comment['body'],
                })

        return issues_comments

    def close_issues(self, username, repository, issue_numbers):
        """
        Closes the specified issue.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue: the issue to close.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200 and 404. The 404 are not thrown because there's no way
        to know if the 404 is because what it's not found is the repo or the
        issue. So it may happen that some issues aren't found but others that
        are.
        """
        base_request = '{0}/repos/{1}/{2}/issues/'.format(
            self.API_URL, username, repository
        )
        payload = {'state': 'closed'}
        closed_issues = []
        not_found_issues = []

        for issue in issue_numbers:
            request = base_request + str(issue)

            try:
                response_issue = self.requester.request(
                    'PATCH', request, self.credentials, json_payload=payload
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
        different to 2XX.
        """
        request = '{0}/repos/{1}/{2}/issues/{3}/comments'.format(
            self.API_URL, username, repository, issue
        )
        payload = {'body': comment}

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
        :param labels: list of labels to associate with the issue.
        :param milestone: milestone number to associate the issue with.
        :raises requests.RequestException: if an error occurs during the
        request.
        :raises UnsuccessfulHttpRequestException: if the request code is
        different to 200.
        """
        request = '{0}/repos/{1}/{2}/issues'.format(
            self.API_URL, username, repository
        )

        payload = {
            'title': title,
            'body': body,
            'labels': labels if labels else [],
        }

        if milestone:
            payload['milestone'] = milestone

        response_issue = self.requester.request(
            'POST', request, self.credentials, json_payload=payload
        )

        return response_issue['number']


    def get_rate_information(self):
        """
        Gets the GitHub API rate information (remaining requests, reset time,
        etc.) requests, the limit is 60 requests/hour. For authenticated ones,
        5000/hour.

        :return: remaining request number.
        """
        request = '{0}/rate_limit'.format(self.API_URL)

        rate_information = self.requester.request('GET', request,
                                                  self.credentials)

        return rate_information['rate']['limit'],\
            rate_information['rate']['remaining'],\
            rate_information['rate']['reset']

    def parse_request_exception(self, exception, milestone=0):
        """
        Parses the generated exception during the request, necessary for
        special cases,
        e.g., when the API limit is hit.

        :param exception: (UnsuccessfulRequestException) The exception object
            generated in the request.
        :return: The error message that will be displayed to the user.
        """
        message = 'An error occurred in the request.'

        rate_limit_hit = exception.code == 403\
            and exception.headers['X-RateLimit-Remaining'] == '0'

        if rate_limit_hit:
            message = 'GitHub API limit was reached. Read more about this at '\
                      + 'https://developer.github.com/v3/#rate-limiting'
        elif exception.code == 422 and milestone:
            message = 'The milestone number {0} is invalid.'.format(milestone)
        else:
            message = super().parse_request_exception(exception, milestone)

        return message
