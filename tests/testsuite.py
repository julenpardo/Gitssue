import sys, os
sys.path.append(os.path.abspath('..'))
import unittest

from controller_test import ControllerTest
from git_wrapper_test import GitWrapperTest
from github_test import GithubTest
from printer_test import PrinterTest
from shell_wrapper_test import ShellWrapperTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(GitWrapperTest())
    suite.addTest(GithubTest())
    suite.addTest(PrinterTest())
    suite.addTest(ShellWrapperTest)

    return suite


if __name__ == '__main__':
    unittest.main()
