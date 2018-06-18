""" Application controller; the one that executes the actions from the CLI. """
import logging
import sys

from requests.exceptions import RequestException
from gitssue.request.unsuccessful_http_request_exception \
    import UnsuccessfulHttpRequestException


class Controller:
    """
    The class that gets the data from the CLI module, uses it for making the
    request in question, and call the printer to show it.
    """

    _MANY_ORIGINS_ERROR = 'More than one remote was detected. Gitssue does ' \
        'not offer support for this yet.'

    def __init__(self, dependencies):
        self.deps = dependencies
        dependencies.instantiate_remote_instance()

    def enable_debug(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger_stream_handler = logging.StreamHandler(sys.stdout)
        logger_stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        logger_stream_handler.setFormatter(formatter)
        logger.addHandler(logger_stream_handler)

    def list(self, show_all=False, description=False):
        """
        Lists the issues, with the labels (if any).
        :param show_all: If show all issues (that is, also closed ones), or
            not.
        :param description: If show description of the issue or not.
        """
        usernames_and_repo = self.deps.git_wrapper.get_username_and_repo()
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
            except UnsuccessfulHttpRequestException as \
                    unsuccessful_http_request:
                error = self.deps.remote.parse_request_exception(
                    unsuccessful_http_request)
            except RequestException as request_exception:
                error = 'A connection error occurred:\n'
                error += str(request_exception)

            if not error:
                self.deps.printer.print_issue_list(issue_list, description)
            else:
                self.deps.printer.print_error(error)
        else:
            self.deps.printer.print_error(self._MANY_ORIGINS_ERROR)

    def desc(self, issue_numbers):
        """
        Prints the description of the given issue numbers.
        :param issue_numbers: the issue number to retrieve the description of.
        """
        usernames_and_repo = self.deps.git_wrapper.get_username_and_repo()
        error = ''
        show_help = False
        issues = False

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            try:
                issues, not_found_issues = self.deps.remote\
                    .get_issues_description(
                        username,
                        repo,
                        issue_numbers,
                    )

                if not_found_issues:
                    error = "The following issues couldn't be found: {0}".\
                        format(', '.join(
                            str(i) for i in not_found_issues
                        ))
            except UnsuccessfulHttpRequestException as \
                    unsuccessful_http_request:
                error = self.deps.remote.parse_request_exception(
                    unsuccessful_http_request)
            except RequestException as request_exception:
                error = 'A connection error occurred:\n'
                error += str(request_exception)

            if issues:
                self.deps.printer.print_issue_list_with_desc(issues)
            if error:
                self.deps.printer.print_error(error)
        else:
            self.deps.printer.print_error(self._MANY_ORIGINS_ERROR)

        return show_help

    def comments(self, issue_number):
        """
        Prints the comment thread of the given issue.
        It's not necessary to check if the "issue_number" is given because in
        this case will be done by Cement, because when the exact number of
        arguments is specified, it does the check itself.
        :param issue_number: the issue to print the comment thread of.
        """
        usernames_and_repo = self.deps.git_wrapper.get_username_and_repo()
        error = ''

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            try:
                comment_thread = self.deps.remote.get_issue_comments(
                    username,
                    repo,
                    issue_number,
                )
            except UnsuccessfulHttpRequestException as \
                    unsuccessful_http_request:
                error = self.deps.remote.parse_request_exception(
                    unsuccessful_http_request,
                    [issue_number],
                )
            except RequestException as request_exception:
                error = 'A connection error occurred:\n'
                error += str(request_exception)

            if not error:
                self.deps.printer.print_issue_comment_thread(
                    comment_thread)
            else:
                self.deps.printer.print_error(error)

        else:
            self.deps.printer.print_error(self._MANY_ORIGINS_ERROR)

    def close(self, issue_numbers):
        """
        Closes the specified issues.

        :param issue_numbers: the issues to close.
        """
        usernames_and_repo = self.deps.git_wrapper.get_username_and_repo()
        error = ''
        closed_issues = []
        not_found_issues = []

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]

            try:
                closed_issues, not_found_issues = self.deps.remote.close_issues(
                    username, repo, issue_numbers
                )
            except UnsuccessfulHttpRequestException as \
                    unsuccessful_http_request:
                error = self.deps.remote.parse_request_exception(
                    unsuccessful_http_request,
                )
            except RequestException as request_exception:
                error = 'A connection error occurred:\n'
                error += str(request_exception)

            if not_found_issues:
                error = "The following issues couldn't be found: {0}".\
                    format(', '.join(
                        str(i) for i in not_found_issues
                    ))

            self.deps.printer.print_closed_issues(closed_issues)

            if error:
                self.deps.printer.print_error(error)
        else:
            self.deps.printer.print_error(self._MANY_ORIGINS_ERROR)

    def rate_information(self):
        """
        Prints the API rate information (remaining requests, reset time, etc.).
        """
        try:
            limit, remaining, reset = self.deps.remote.get_rate_information()

            unlimited = True if limit == -1 and remaining == -1 \
                and reset == -1 else False

            self.deps.printer.print_rate_information(
                limit,
                remaining,
                reset,
                unlimited
            )
        except RequestException as request_exception:
            error = 'A connection error occurred:\n'
            error += str(request_exception)
            self.deps.printer.print_error(error)
