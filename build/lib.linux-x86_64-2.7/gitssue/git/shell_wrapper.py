"""
Wrapper for executing shell commands (Git commands, actually).
Actually, the aim of this class is just for later mocking.
"""

import subprocess
import shlex


class ShellWrapper:
    """
    Wrapper for executing shell commands, for Git module.
    """

    def execute_command(self, command):  # pylint: disable=no-self-use
        """
        Executes the given command (a Git command).
        :param command: the Git command to execute.
        :return: the output of the command.
        """
        arguments = shlex.split(command)

        try:
            process = subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            output, error = process.communicate()

            if error or not output:
                return False
            else:
                return output.decode('utf-8')

        except OSError:
            return False
