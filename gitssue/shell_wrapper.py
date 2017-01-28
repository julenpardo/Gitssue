"""
Wrapper for executing shell commands (Git commands, actually).
Actually, the aim of this class is just for later mocking.
"""

import subprocess
import shlex


class ShellWrapper():

    def execute_command(self, command):
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
