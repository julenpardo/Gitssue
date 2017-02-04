""" Github module. """
from gitssue.remote.remote_repo_interface import RemoteRepoInterface


class Github(RemoteRepoInterface):
    """
    Github specific module.
    """

    API_URL = 'https://api.github.com'

    def __init__(self, requester):
        super(Github, self).__init__(requester)

    def get_issue_list(self, username, repository, show_all=False, get_description=False):
        """
        Gets the open issue list of the given repository of the given user.

        :param username: the user owning the repository.
        :param repository: the repository to look the issues at.
        :param show_all: show also closed issues.
        :return: a dictionary id:label format.
        """
        request = '{0}/repos/{1}/{2}/issues'.format(self.API_URL, username, repository)

        if show_all:
            request += '?state=all'

        response_issues = self.requester.get_request(request)
        issue_list = []
        description = ''

        if response_issues:
            for issue in response_issues:
                if get_description:
                    description = self.get_issues_description(
                        username,
                        repository,
                        [issue['number']]
                    )[0]['description']['body']

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
        :return: a dictionary with the title and the body message of each issue id.
        """
        issues_descriptions = []

        if issue_numbers:
            for issue_number in issue_numbers:
                request = '{0}/repos/{1}/{2}/issues/{3}'.format(
                    self.API_URL,
                    username,
                    repository,
                    issue_number
                )

                full_issue = self.requester.get_request(request)
                print(request)

                issue_description = {
                    'number': issue_number,
                    'labels': full_issue['labels'],
                    'description': {
                        'title': full_issue['title'],
                        'body': full_issue['body'],
                    }
                }

                issues_descriptions.append(issue_description)

        return issues_descriptions

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
