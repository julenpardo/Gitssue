""" Gitlab module. """
from gitssue.remote.remote_repo_interface import RemoteRepoInterface
from gitssue.request.unsuccessful_http_request_exception \
    import UnsuccessfulHttpRequestException


class Gitlab(RemoteRepoInterface):
    """
    Github specific module.
    """

    _API_VERSION = 'v4'

    def __init__(self, requester, credentials, domain):
        super(Gitlab, self).__init__(requester, auth_token=credentials)
        self.api_url = 'https://{0}/api/{1}'.format(domain, self._API_VERSION)

    def get_issue_list(self, username, repository, show_all=False,
                       get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        request = '{0}/issues'.format(self.api_url)

        state = '?state=all' if show_all else '?state=opened'
        request += state

        auth_token_header = {'PRIVATE-TOKEN': self.auth_token}

        issue_list = []
        description = ''
        project_id = self._get_project_id(username, repository)

        if project_id:
            response_issues = self.requester.get_request(
                request,
                extra_headers=auth_token_header
            )

            project_issues = list(filter(
                lambda i: i['project_id'] == project_id, response_issues
            ))

            for issue in project_issues:
                if get_description:
                    description = issue['description']

                issue_labels = self._create_label_list(
                    project_id,
                    auth_token_header,
                    issue
                )

                issue_list.append({
                    'number': issue['iid'],
                    'title': issue['title'],
                    'labels': issue_labels,
                    'description': description,
                })

        return issue_list

    def _get_labels(self, project_id, auth_token_header):
        labels_request = '{0}/projects/{1}/labels'.format(
            self.api_url,
            project_id
        )

        labels_info = self.requester.get_request(
            labels_request,
            extra_headers=auth_token_header
        )

        return labels_info

    def _create_label_list(self, project_id, auth_token_header, issue):
        issue_labels = []
        labels_info = self._get_labels(
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

        return issue_labels

    def _get_project_id(self, username, repository):
        auth_token_header = {'PRIVATE-TOKEN': self.auth_token}
        project_request = '{0}/projects/{1}%2F{2}'.format(
            self.api_url,
            username,
            repository
        )

        project = self.requester.get_request(project_request,
                                             extra_headers=auth_token_header)

        return project.get('id')

    def get_issues_description(self, username, repository, issue_numbers):
        """
        Gets the specified issues, with the descriptions.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_numbers: the issue identifier(s).
        :return: a dictionary with the title and the body message of each issue
            id.
        """
        request = '{0}/issues'.format(self.api_url)
        issues_descriptions = []
        not_found_issues = []

        if issue_numbers:
            project_id = self._get_project_id(username, repository)
            auth_token_header = {'PRIVATE-TOKEN': self.auth_token}
            response_issues = self.requester.get_request(
                request,
                extra_headers=auth_token_header
            )

            for issue in response_issues:
                issue_id = str(issue['iid'])

                if issue_id in issue_numbers:
                    issue_labels = self._create_label_list(
                        project_id,
                        auth_token_header,
                        issue
                    )

                    issue_description = {
                        'number': issue_id,
                        'labels': issue_labels,
                        'description': {
                            'title': issue['title'],
                            'body': issue['description']
                        }
                    }

                    issues_descriptions.append(issue_description)

            not_found_issues = [issue_number for issue_number in issue_numbers if issue_number not in [
                str(issue['iid']) for issue in response_issues]]

        return issues_descriptions, not_found_issues

    def get_issue_comments(self, username, repository, issue_number):
        """
        Gets the comments made in the issue ticket.
        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param issue_number: the issue number to query the comments to.
        """
        request = '{0}/projects/{1}/issues/{2}/notes'
        issue_comments = []

        if issue_number:
            project_id = self._get_project_id(username, repository)
            request = request.format(self.api_url, project_id, issue_number)

            auth_token_header = {'PRIVATE-TOKEN': self.auth_token}
            response_comments = self.requester.get_request(
                request,
                extra_headers=auth_token_header
            )

            if response_comments:
                for comment in response_comments:
                    issue_comments.append({
                        'author': comment['author']['username'],
                        'created_at': comment['created_at'],
                        'updated_at': comment['updated_at'],
                        'body': comment['body'],
                    })

        return issue_comments

    def get_rate_information(self):
        """
        The Gitlab API doesn't have a rate limit, so we return everything as
        -1 (the total limit, the remaining requests, and the reset time), to
        let the controller know that it's unlimited.
        :return: everything to -1 to indicate that is unlimited.
        """
        return -1, -1, -1

    def parse_request_exception(self, exception, issue_numbers=()):
        """
        Parses the generated exception during the request, necessary for
        special cases, e.g., when the API limit is hit.

        TODO: make messages more specific.
        :param exception: (UnsuccessfulRequestException) The exception object
            generated in the request.
        :param issue_numbers: the issue number(s) that weren't found in the
            request.
        :return: The error message that will be displayed to the user.
        """
        message = 'An error occurred in the request.'

        return message
