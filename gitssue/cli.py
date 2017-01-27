""" CLI module (the main module of the app, since it's a CLI app). """

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import git_wrapper
import github
import printer


class BaseController(CementBaseController):
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
        aliases=['l'],
        help='List opened issues'
    )
    def list(self):
        """
        The method that lists the issues.
        :return:
        """
        self.app.log.info('Inside BaseController.list()')

        username, repo = git_wrapper.get_username_and_repo()

        self.app.log.info('Github username: {0}; repo name: {1}'.format(username, repo))

        try:
            issue_list = github.get_issue_list(username, repo)
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
