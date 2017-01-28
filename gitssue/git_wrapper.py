""" Wrapper for executing Git commands. """


def get_username_and_repo(shell_wrapper):
    """
    Extracts the username and repository from the URL and returns it.
    :param shell_wrapper: the wrapper to execute the command with.
    :return: username and repository name.
    """
    remote_url = get_remote_url(shell_wrapper)

    username_and_repo = remote_url.replace('https://github.com/', '')
    username_and_repo = username_and_repo.replace('.git', '')
    username_and_repo = username_and_repo.replace('\n', '')
    username_and_repo = username_and_repo.split('/')

    return username_and_repo[0], username_and_repo[1]


def get_remote_url(shell_wrapper):
    """
    Gets the URL of the remote repository, executing the Git command.
    :param shell_wrapper: the wrapper to execute the command with.
    :return: the URL of the remote.
    """
    command = 'git config --get remote.origin.url'

    url = shell_wrapper.execute_command(command)

    return url
