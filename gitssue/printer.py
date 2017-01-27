""" CLI printer module. """


def print_issue_list(issues):
    """
    Prints the issue list, in "id: label" format.
    :param issues: The issue dictionary.
    :return:
    """
    if issues:
        for issue_number, issue_label in sorted(issues.items()):
            print('#{0}: {1}'.format(issue_number, issue_label))
    else:
        print('No issue could be found.')
