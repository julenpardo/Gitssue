""" Application controller; the one that executes the actions from the CLI. """
from dependencies import Dependencies
from git import git_wrapper
from gitssue.request.unsuccessful_request_exception import UnsuccessfulRequestException


class Controller:
    def __init__(self, dependencies):
        self.deps = dependencies

    def list(self, all=False, description=False):
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            try:
                username, repo = usernames_and_repo[0]
                issue_list = self.deps.remote.get_issue_list(
                    username,
                    repo,
                    all,
                    description,
                )
            except TypeError:
                error = 'No issue could be found.'
            except UnsuccessfulRequestException as unsuccessful_request:
                error = self.deps.remote.parse_request_exception(unsuccessful_request)

            if not error:
                self.deps.printer.print_issue_list(issue_list, description)
            else:
                self.deps.printer.print_error(error)
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')

    def desc(self, issue_numbers):
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''
        show_help = False

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            if not all(number.isdigit() for number in issue_numbers):
                print('Issue numbers must be numbers.')
            elif issue_numbers:
                try:
                    issues = self.deps.remote.get_issues_description(
                        username,
                        repo,
                        issue_numbers,
                    )
                except UnsuccessfulRequestException as unsuccessful_request:
                    error = self.deps.remote.parse_request_exception(unsuccessful_request)

                if not error:
                    self.deps.printer.print_issue_list_with_desc(issues)
                else:
                    self.deps.printer.print_error(error)
            else:
                show_help = True
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')

        return show_help

    def thread(self, issue_number):
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''
        show_help = False

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            if not issue_number.isdigit():
                print('Issue number must be a number.')
            elif issue_number:
                try:
                    comment_thread = self.deps.remote.get_issue_comments(
                        username,
                        repo,
                        issue_number,
                    )
                except UnsuccessfulRequestException as unsuccessful_request:
                    error = self.deps.remote.parse_request_exception(unsuccessful_request)

                if not error:
                    self.deps.printer.print_issue_comment_thread(comment_thread)
                else:
                    self.deps.printer.print_error(error)
            else:
                show_help = True
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')

        return show_help
