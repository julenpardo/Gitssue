""" CLI module (the main module of the app, since it's a CLI app). """

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

from dependencies import Dependencies

import git_wrapper


class BaseController(ArgparseController):
    """
    Base Cement controller class.
    """
    class Meta: # pylint: disable=too-few-public-methods
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
        :return:
        """
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
        )],
    )
    def list(self):
        """
        The method that lists the issues.
        """
        username, repo = git_wrapper.get_username_and_repo(self.deps.shell)
        show_all = self.app.pargs.all

        try:
            issue_list = self.deps.remote.get_issue_list(username, repo, show_all)
        except TypeError:
            issue_list = False

        self.deps.printer.print_issue_list(issue_list)

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
        username, repo = git_wrapper.get_username_and_repo(self.deps.shell)
        issue_numbers = self.app.pargs.issue_numbers

        if not all(number.isdigit() for number in issue_numbers):
            print('Issue numbers must be numbers.')
        elif issue_numbers:
            issues = self.deps.remote.get_issues_description(
                'julenpardo',
                'db-connection-watcher',
                issue_numbers,
            )

            self.deps.printer.print_issue_list_with_desc(issues)
        else:
            self.app.args.parse_args(['desc', '--help'])


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
