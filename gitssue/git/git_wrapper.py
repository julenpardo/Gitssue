""" Wrapper for executing Git commands. """
import re
from gitssue.git.repo_not_found_exception import RepoNotFoundException


class GitWrapper:
    _SUPPORTED_REMOTES = ['github.com', 'gitlab.com', 'bitbucket.org']

    def __init__(self, shell_wrapper):
        self.shell_wrapper = shell_wrapper

    def discard_not_supported_remotes(self, remotes_url):
        """
        Discards the not supported remotes. For the moment, only Github is
        supported.
        :param remotes_url: List of remotes names with its URL, e.g.:
            [['origin', 'git@github.com:julenpardo/Gitssue.git]]
        :return: The list in the same format as received, but discarding the
            not supported origins.
        """
        for remote in remotes_url:
            remote_url = remote[1]
            is_supported = any(supported_remote in remote_url.lower()
                               for supported_remote in self._SUPPORTED_REMOTES)

            if not is_supported:
                remotes_url.remove(remote)

        return remotes_url

    def get_username_and_repo(self):
        """
        Extracts the username and repository from the URL and returns it.
        :return: username and repository name.
        """
        try:
            usernames_and_repos = []

            for remote in self.discard_not_supported_remotes(
                    self.get_remotes_urls()):
                remote_url = remote[1]

                username_and_repo = re.sub(r"https:\/\/.*@", '', remote_url)
                username_and_repo = username_and_repo.replace('.git', '')
                username_and_repo = username_and_repo.replace('https://', '')
                username_and_repo = username_and_repo.replace('\n', '')

                for supported_remote in self._SUPPORTED_REMOTES:
                    username_and_repo = username_and_repo.replace(
                        '{}/'.format(supported_remote),
                        ''
                    )
                    username_and_repo = username_and_repo.replace(
                        'git@{}:'.format(supported_remote),
                        ''
                    )

                username, repo = username_and_repo.split('/')

                usernames_and_repos.append([username, repo])

            return usernames_and_repos
        except RepoNotFoundException:
            raise

    def get_remote_url(self):
        """
        Gets the URL of the remote repository, executing the Git command.
        :return: the URL of the remote.
        """
        command = 'git config --get remote.origin.url'

        url = self.shell_wrapper.execute_command(command)

        if not url:
            raise RepoNotFoundException

        return url

    def get_remotes_urls(self):
        """
        Gets the remotes list with the 'git remote --verbose' command.
        The command returns two URLs for each remote, for fetching and pushing,
        so after creating the list, we have to remove the duplicates.
        :return: list of remote name with its URL.
        """
        command = 'git remote --verbose'

        remotes_info = self.shell_wrapper.execute_command(command)

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
