""" CLI module (the main module of the app, since it's a CLI app). """

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

import git_wrapper
import github
import printer


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

    @expose(hide=True)
    def default(self):
        """
        The accessed method if no command has been specified.
        :return:
        """
        self.app.log.info('Inside BaseController.default()')

    @expose(
        help='List opened issues',
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
        self.app.log.info('Inside BaseController.list()')

        username, repo = git_wrapper.get_username_and_repo()

        self.app.log.info('Github username: {0}; repo name: {1}'.format(username, repo))

        show_all = False
        if self.app.pargs.all:
            show_all = True

        try:
            issue_list = github.get_issue_list(username, repo, show_all)
        except TypeError:
            issue_list = False

        printer.print_issue_list(issue_list)


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
