""" Wrapper for executing Git commands. """
from gitssue.repo_not_found_exception import RepoNotFoundException

SUPPORTED_REMOTES = ['github']


def discard_not_supported_remotes(remotes_url):
    """
    Discards the not supported remotes. For the moment, only Github is supported.
    :param remotes_url: List of remotes names with its URL, e.g.:
    [['origin', 'git@github.com:julenpardo/Gitssue.git]]
    :return: The list in the same format as received, but discarding the not supported
    origins.
    """
    for remote in remotes_url:
        remote_url = remote[1]
        is_supported = any(supported_remote in remote_url.lower() for supported_remote in SUPPORTED_REMOTES)

        if not is_supported:
            remotes_url.remove(remote)

    return remotes_url


def get_username_and_repo(shell_wrapper):
    """
    Extracts the username and repository from the URL and returns it.
    :param shell_wrapper: the wrapper to execute the command with.
    :return: username and repository name.
    """
    try:
        remote_url = get_remote_url(shell_wrapper)

        username_and_repo = remote_url.replace('https://github.com/', '')
        username_and_repo = username_and_repo.replace('.git', '')
        username_and_repo = username_and_repo.replace('\n', '')
        username_and_repo = username_and_repo.split('/')

        return username_and_repo[0], username_and_repo[1]
    except RepoNotFoundException:
        raise


def get_remote_url(shell_wrapper):
    """
    Gets the URL of the remote repository, executing the Git command.
    :param shell_wrapper: the wrapper to execute the command with.
    :return: the URL of the remote.
    """
    command = 'git config --get remote.origin.url'

    url = shell_wrapper.execute_command(command)

    if not url:
        raise RepoNotFoundException

    return url


def get_remotes_urls(shell_wrapper):
    """
    Gets the remotes list with the 'git remote --verbose' command.
    The command returns two URLs for each remote, for fetching and pushing, so
    after creating the list, we have to remove the duplicates.
    :param shell_wrapper: the wrapper to execute the command with.
    :return: list of remote name with its URL.
    """
    command = 'git remote --verbose'

    remotes_info = shell_wrapper.execute_command(command)

    if not remotes_info:
        raise RepoNotFoundException

    duplicated_remotes_list = []

    for remote_info in remotes_info.splitlines():
        remote_name, url = remote_info.split()[:2]
        duplicated_remotes_list.append([remote_name, url])

    remotes_list = []

    for remote in duplicated_remotes_list:
        if remote not in remotes_list:
            remotes_list.append(remote)

    return remotes_list
