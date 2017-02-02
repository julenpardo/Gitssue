""" Dummy module to simulate """

from remote.remote_repo_interface import RemoteRepoInterface


class Dummy(RemoteRepoInterface):

    def get_issues_description(self, username, repository, issue_numbers):
        return (
            {
                'number': '1',
                'description': {
                    'title': 'First dummy issue',
                    'body': 'Body of first dummy issue.',
                },
            },
            {
                'number': '2',
                'description': {
                    'title': 'Second dummy issue',
                    'body': 'Body of second dummy issue.',
                },
            },
        )

    def get_issue_list(self, username, repository, show_all=False):
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
