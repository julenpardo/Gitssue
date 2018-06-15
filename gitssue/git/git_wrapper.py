""" Wrapper for executing Git commands. """
import re
from gitssue.git.repo_not_found_exception import RepoNotFoundException


class GitWrapper:

    def __init__(self, shell_wrapper):
        self.shell_wrapper = shell_wrapper

    def get_username_and_repo(self):
        """
        Extracts the username and repository from the URL and returns it.
        :return: username and repository name.
        """
        try:
            usernames_and_repos = []

            for remote in self.get_remotes_urls():
                remote_url = remote[1]

                if remote_url.startswith('git@'):
                    username_and_repo = remote_url.replace('git@', '')\
                        .split(':')[1]
                else:
                    domain, username, repo = remote_url.replace('https://', '')\
                        .split('/')
                    username_and_repo = username + '/' + repo

                username_and_repo = username_and_repo.replace('.git', '')

                username, repo = username_and_repo.split('/')

                usernames_and_repos.append([username, repo])

            return usernames_and_repos
        except RepoNotFoundException:
            raise

    def get_remote_domain(self):
        """
        Gets the domain of the of the repo hoster.

        :return: the domain of the repo hoster.
        """
        command = 'git config --get remote.origin.url'

        url = self.shell_wrapper.execute_command(command)

        if not url:
            raise RepoNotFoundException

        if url.startswith('git@'):
            domain = url.replace('git@', '').split(':')[0]
        else:
            domain = url.replace('https://', '').split('/')[0]

        return domain

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
