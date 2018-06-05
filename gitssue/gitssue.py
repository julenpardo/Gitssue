""" CLI module (the main module of the app, since it's a CLI app). """


import sys
import os

sys.path.insert(0, os.getcwd())

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

from gitssue.dependencies.dependencies import Dependencies
from gitssue.controller.controller import Controller

GITSSUE_VERSION = '1.1'


class BaseController(ArgparseController):
    """
    CLI module (the main module of the app, since it's a CLI app).
    """

    controller = Controller(Dependencies())

    """
    Base Cement controller class.
    """
    class Meta:
        """
        Meta class of the base Cement controller.
        """
        label = 'base'
        description = 'Gitssue - Manage your issues from the command line ' \
            + '(version {0})'.format(GITSSUE_VERSION)
        arguments = [
            (
                ['--version', '-v'],
                dict(action='store_true', help='Show version and exit')
            )
        ]

    @expose(hide=True)
    def default(self):
        """
        The default method.
        """
        arguments = self.app.pargs

        if arguments.version:
            print('Gitssue {0}'.format(GITSSUE_VERSION))
        else:
            no_option = arguments.command is None and not arguments.debug \
                and not arguments.suppress_output and not arguments.version

            if no_option:
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
        self.controller.list(self.app.pargs.all, self.app.pargs.desc)

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
        show_help = self.controller.desc(self.app.pargs.issue_numbers)

        if show_help:
            self.app.args.parse_args(['desc', '--help'])

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
        It's not necessary to check if the "issue_number" is given because in
        this case will be done by Cement, because when the exact number of
        arguments is specified, it does the check itself.
        """
        self.controller.thread(self.app.pargs.issue_number[0])

    @expose(
        help='Shows the API rate information (remaining requests, reset '
             'time, etc.).',
        aliases=['ri']
    )
    def rate_info(self):
        """
        Gets the API rate information (remaining requests, reset time, etc.).
        """
        self.controller.rate_information()


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


def main():
    """
    Main method.
    """
    with Gitssue() as app:
        app.run()
