""" CLI printer module. """


def print_issue_list(issues):
    """
    Prints the issue list, in "id: label" format.
    :param issues: The issue dictionary.
    """
    if issues:
        for issue_number, issue_label in sorted(issues.items()):
            print('#{0}: {1}'.format(issue_number, issue_label))
    else:
        print('No issue could be found.')


def print_issue_list_with_desc(issues):
    """
    Prints the issue list like in "print_issue_list", but also with the description.
    :param issues: the issues dictionary.
    :return:
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
