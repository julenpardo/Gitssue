"""
Wrapper for executing shell commands (Git commands, actually).
Actually, the aim of this class is just for later mocking.
"""

import subprocess
import shlex


class ShellWrapper:

    def execute_command(self, command):
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
                returned_value = False
            else:
                returned_value = output.decode('utf-8')

        except Exception:
            returned_value = False

        return returned_value
