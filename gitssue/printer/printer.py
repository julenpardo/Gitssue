""" CLI printer module. """
from printer.printer_interface import PrinterInterface


class Printer(PrinterInterface):

    ISSUE_TITLE_COLOR = 'c3a000'

    def __init__(self, color_printer):
        """
        Gets the specific implementation of ColorPrinterInterface.
        :param color_printer: implementation of ColorPrinterInterface.
        """
        self.color_printer = color_printer

    def print_issue_list(self, issues):
        """
        Prints the issue list, in "id: label" format.
        :param issues: The issue dictionary.
        """
        if issues:
            for issue in issues:
                print('#{0}: {1}'.format(issue['number'], issue['title']))
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
                print(issue['description']['body'])
                print('\n')
        else:
            print('No issue could be found.')

    def print_issue_list_with_labels(self, issues):
        """
        Prints the issue list with labels.
        :param issues: the issue list.
        """
        if issues:
            for issue in issues:
                issue_title = '#{0}: {1}'.format(issue['number'], issue['title'])
                self.color_printer.print_colored_line(issue_title, self.ISSUE_TITLE_COLOR)

                if issue['labels']:
                    self.color_printer.print_labels(issue['labels'])

                print()
        else:
            print('No issue could be found.')
