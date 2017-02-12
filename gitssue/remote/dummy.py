""" Dummy module to simulate """

from gitssue.remote.remote_repo_interface import RemoteRepoInterface


class Dummy(RemoteRepoInterface):

    def __init__(self, requester):
        super(Dummy, self).__init__(requester)

    def get_issues_description(self, username, repository, issue_numbers):
        return (
            {
                'number': '1',
                'description': {
                    'title': 'First dummy issue',
                    'body': 'Body of first dummy issue.',
                },
                'labels': (
                    {
                        'name': 'bug',
                        'color': 'fab444'
                    },
                    {
                        'name': 'dummy',
                        'color': '000000'
                    },
                ),
            },
            {
                'number': '2',
                'description': {
                    'title': 'Second dummy issue',
                    'body': 'Body of second dummy issue.',
                },
                'labels': (
                    {
                        'name': 'dummy',
                        'color': 'ffffff'
                    },
                ),
            },
        )

    def get_issue_list(self, username, repository, show_all=False, get_description=False):
        return (
            {
                'number': '1',
                'title': 'First dummy issue',
                'labels': (
                    {
                        'name': 'bug',
                        'color': 'fab444'
                    },
                    {
                        'name': 'dummy',
                        'color': '000000'
                    },
                ),
                'description': 'Some description',
            },
            {
                'number': '2',
                'title': 'Second dummy issue',
                'labels': (
                    {
                        'name': 'dummy',
                        'color': 'ffffff'
                    },
                ),
            },
        )

    def get_issue_comments(self, username, repository, issue_number):
        return (
            {
                'author': 'julenpardo',
                'created_at': 'now',
                'updated_at': 'now',
                'body': 'a comment',
            }, {
                'author': 'julenpardo',
                'created_at': 'now',
                'updated_at': 'now',
                'body': 'another comment',
            }
        )

    def parse_request_exception(self, exception):
        pass
