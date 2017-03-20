""" CLI printer module. """
from gitssue.printer.printer_interface import PrinterInterface


class Printer(PrinterInterface):
    """
    CLI printer module for printing the output.
    """

    ISSUE_TITLE_COLOR = 'c3a000'
    COMMENT_AUTHOR_COLOR = 'c3a000'
    COMMENT_DATE_COLOR = 'c3a000'
    ERROR_COLOR = 'ff0000'

    def __init__(self, color_printer):
        """
        Gets the specific implementation of ColorPrinterInterface.
        :param color_printer: implementation of ColorPrinterInterface.
        """
        self.color_printer = color_printer

    def print_issue_list(self, issues, show_description=False):
        """
        Prints the issue list with labels, if any, these ones with colors.
        The issue title is printed with colors only if the descriptions for these are going
        to be displayed.
        :param issues: the issue list.
        :param show_description: if show also the descriptions or not.
        """
        if issues:
            for issue in issues:
                issue_title = '#{0}: {1}'.format(issue['number'], issue['title'])

                if show_description:
                    self.color_printer.print_colored_line(issue_title, self.ISSUE_TITLE_COLOR)
                else:
                    print(issue_title)

                self.color_printer.print_labels(issue.get('labels', list()))

                if show_description and issue.get('description'):
                    print(issue['description'])

                print()
        else:
            print('No issue could be found.')

    def print_issue_list_with_desc(self, issues):
        """
        Prints the issue list like in "print_issue_list", but also with the description.
        :param issues: the issues dictionary.
        """
        if issues:
            for issue in issues:
                issue_title = '#{0}: {1}'.format(
                    issue['number'],
                    issue['description']['title']
                )
                self.color_printer.print_colored_line(issue_title, self.ISSUE_TITLE_COLOR)

                if issue.get('labels'):
                    self.color_printer.print_labels(issue['labels'])

                print(issue['description']['body'])
                print('\n')
        else:
            print('No issue could be found.')

    def print_issue_comment_thread(self, comment_thread):
        """
        Prints the given comment thread belonging to the issue.
        :param comment_thread: the thread of comments.
        """
        if comment_thread:
            for comment in comment_thread:
                author = 'Author: {0}'.format(comment['author'])
                self.color_printer.print_colored_line(author, self.COMMENT_AUTHOR_COLOR)

                date = 'Date: {0}'.format(comment['created_at'])
                self.color_printer.print_colored_line(date, self.COMMENT_DATE_COLOR)

                print('\n{0}\n\n'.format(comment['body']))

        else:
            print('No comment could be found.')

    def print_error(self, error):
        """
        Prints an error.
        :param error: The error to print.
        """
        self.color_printer.print_colored_line('Error', self.ERROR_COLOR)
        print(error + '\n')
