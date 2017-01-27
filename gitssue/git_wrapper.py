""" Wrapper for executing Git commands. """

import subprocess
import shlex


def get_username_and_repo():
    """
    Extracts the username and repository from the URL and returns it.
    :return: username and repository name.
    """
    remote_url = get_remote_url()

    username_and_repo = remote_url.replace('https://github.com/', '')
    username_and_repo = username_and_repo.replace('.git', '')
    username_and_repo = username_and_repo.replace('\n', '')
    username_and_repo = username_and_repo.split('/')

    return username_and_repo[0], username_and_repo[1]


def get_remote_url():
    """
    Gets the URL of the remote repository, executing the Git command.
    :return: the URL of the remote.
    """
    command = 'git config --get remote.origin.url'

    url = execute_command(command)

    return url


def execute_command(command):
    """
    Executes the given command (a Git command).
    :param command: the Git command to execute.
    :return: the output of the command.
    """
    arguments = shlex.split(command)

    process = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output, error = process.communicate()

    return output.decode('utf-8')
