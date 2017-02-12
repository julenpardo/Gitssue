""" CLI module (the main module of the app, since it's a CLI app). """

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

from dependencies import Dependencies
from git import git_wrapper
from gitssue.request.unsuccessful_request_exception import UnsuccessfulRequestException


class BaseController(ArgparseController):
    """
    Base Cement controller class.
    """
    class Meta:
        """
        Meta class of the base Cement controller.
        """
        label = 'base'
        description = 'Gitssue - Manage your issues from the command line'

    deps = Dependencies()

    @expose(hide=True)
    def default(self):
        """
        The accessed method if no command has been specified. Displays the help.
        """
        self.app.render({'foo': 'It works!'}, 'foo.m')
        self.app.args.parse_args(['--help'])


    @expose(
        help='List open issues.',
        aliases=['l'],
        arguments=[(
            ['-a', '--all'],
            dict(
                help='Show all the issues (also closed ones).',
                action='store_true'
            ),
        ), (
            ['-d', '--desc'],
            dict(
                help='Get description of the issue.',
                action='store_true'
            ),
        ),
                  ],
    )
    def list(self):
        """
        The method that lists the issues.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            try:
                username, repo = usernames_and_repo[0]
                issue_list = self.deps.remote.get_issue_list(
                    username,
                    repo,
                    self.app.pargs.all,
                    self.app.pargs.desc,
                )
            except TypeError:
                error = 'No issue could be found.'
            except UnsuccessfulRequestException as unsuccessful_request:
                error = self.deps.remote.parse_request_exception(unsuccessful_request)

            if not error:
                self.deps.printer.print_issue_list_with_labels(issue_list)
            else:
                self.deps.printer.print_error(error)
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')

    @expose(
        help='Get description of the given issue.',
        aliases=['d'],
        arguments=[
            (['issue_numbers'], dict(action='store', nargs='*')),
        ]
    )
    def desc(self):
        """
        Get description of the given issue.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]
            issue_numbers = self.app.pargs.issue_numbers

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
                self.app.args.parse_args(['desc', '--help'])
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')

    @expose(
        help='Get the comment thread of the given issue.',
        aliases=['t'],
        arguments=[
            (['issue_number'], dict(action='store', nargs=1)),
        ]
    )
    def thread(self):
        """
        Get comment thread the given issue.
        """
        usernames_and_repo = git_wrapper.get_username_and_repo(self.deps.shell)
        error = ''

        if len(usernames_and_repo) == 1:
            username, repo = usernames_and_repo[0]
            issue_number = self.app.pargs.issue_number[0]

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
                self.app.args.parse_args(['desc', '--help'])
        else:
            print('More than one remote was detected. Gitssue does not offer support for this yet.')


class Gitssue(CementApp):
    """
    Main class.
    """
    class Meta:
        """
        Meta class for main class.
        """
        label = 'Gitssue'
        base_controller = 'base'
        handlers = [
            BaseController,
        ]

with Gitssue() as app:
    app.run()
