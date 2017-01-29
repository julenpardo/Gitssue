""" CLI printer module. """
from printer.printer_interface import PrinterInterface


class Printer(PrinterInterface):
    def print_issue_list(self, issues):
        """
        Prints the issue list, in "id: label" format.
        :param issues: The issue dictionary.
        """
        if issues:
            for issue_number, issue_label in sorted(issues.items()):
                print('#{0}: {1}'.format(issue_number, issue_label))
        else:
            print('No issue could be found.')

    def print_issue_list_with_desc(self, issues):
        """
        Prints the issue list like in "print_issue_list", but also with the description.
        :param issues: the issues dictionary.
        """
        if issues:
            for issue in issues:
                print('#{0}: {1}'.format(
                    issue['number'],
                    issue['description']['title']
                ))
                print(issue['description']['body'])
                print('-----------------------------------\n')
        else:
            print('No issue could be found.')
