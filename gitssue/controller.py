""" Application controller; the one that executes the actions from the CLI. """
from requests.exceptions import RequestException
from git import git_wrapper
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class Controller:
    """
    The class that gets the data from the CLI module, uses it for making the request in question,
    and call the printer to show it.
    """

    ISSUE_NUMBER_FORMAT_ERROR = 'Issue number(s) must be number(s).'
    MANY_ORIGINS_ERROR = 'More than one remote was detected. Gitssue does not offer ' \
                         'support for this yet.'

    def __init__(self, dependencies):
        self.deps = dependencies

    def list(self, show_all=False, description=False):
        """
        Lists the issues, with the labels (if any).
        :param show_all: If show all issues (that is, also closed ones), or not.
        :param description: If show description of the issue or not.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            try:
                username, repo = usernames_and_repo[0]
                issue_list = self.deps.remote.get_issue_list(
                    username,
                    repo,
                    show_all,
                    description,
                )
            except TypeError:
                error = 'No issue could be found.'
            except UnsuccessfulHttpRequestException as unsuccessful_http_request:
                error = self.deps.remote.parse_request_exception(unsuccessful_http_request)
            except RequestException as request_exception:
                error = 'A connection error occurred:\n'
                error += str(request_exception)

            if not error:
                self.deps.printer.print_issue_list(issue_list, description)
            else:
                self.deps.printer.print_error(error)
        else:
            self.deps.printer.print_error(self.MANY_ORIGINS_ERROR)

    def desc(self, issue_numbers):
        """
        Prints the description of the given issue numbers.
        :param issue_numbers: the issue number to retrieve the description of.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''
        show_help = False

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            if not all(number.isdigit() for number in issue_numbers):
                self.deps.printer.print_error(self.ISSUE_NUMBER_FORMAT_ERROR)
            elif issue_numbers:
                try:
                    issues = self.deps.remote.get_issues_description(
                        username,
                        repo,
                        issue_numbers,
                    )
                except UnsuccessfulHttpRequestException as unsuccessful_http_request:
                    error = self.deps.remote.parse_request_exception(unsuccessful_http_request)
                except RequestException as request_exception:
                    error = 'A connection error occurred:\n'
                    error += str(request_exception)

                if not error:
                    self.deps.printer.print_issue_list_with_desc(issues)
                else:
                    self.deps.printer.print_error(error)
            else:
                show_help = True
        else:
            self.deps.printer.print_error(self.MANY_ORIGINS_ERROR)

        return show_help

    def thread(self, issue_number):
        """
        Prints the comment thread of the given issue.
        It's not necessary to check if the "issue_number" is given because in this case will
        be done by Cement, because when the exact number of arguments is specified, it does the
        check itself.
        :param issue_number: the issue to print the comment thread of.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            if not issue_number.isdigit():
                self.deps.printer.print_error(self.ISSUE_NUMBER_FORMAT_ERROR)
            else:
                try:
                    comment_thread = self.deps.remote.get_issue_comments(
                        username,
                        repo,
                        issue_number,
                    )
                except UnsuccessfulHttpRequestException as unsuccessful_http_request:
                    error = self.deps.remote.parse_request_exception(unsuccessful_http_request)
                except RequestException as request_exception:
                    error = 'A connection error occurred:\n'
                    error += str(request_exception)

                if not error:
                    self.deps.printer.print_issue_comment_thread(comment_thread)
                else:
                    self.deps.printer.print_error(error)

        else:
            self.deps.printer.print_error(self.MANY_ORIGINS_ERROR)
