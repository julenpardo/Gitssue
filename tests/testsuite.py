import sys

import unittest
from unittest import makeSuite

from controller_test import ControllerTest
from git_wrapper_test import GitWrapperTest
from github_test import GithubTest
from gitlab_test import GitlabTest
from bitbucket_test import BitbucketTest
from printer_test import PrinterTest
from shell_wrapper_test import ShellWrapperTest
from requests_test import RequestsTest
from colorconsole_color_printer_test import ColorConsoleColorPrinterTest
from config_reader_test import ConfigReaderTest
from dependencies_test import DependenciesTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(makeSuite(ControllerTest))
    suite.addTest(makeSuite(GitWrapperTest))
    suite.addTest(makeSuite(GithubTest))
    suite.addTest(makeSuite(GitlabTest))
    suite.addTest(makeSuite(BitbucketTest))
    suite.addTest(makeSuite(PrinterTest))
    suite.addTest(makeSuite(ShellWrapperTest))
    suite.addTest(makeSuite(RequestsTest))
    suite.addTest(makeSuite(ColorConsoleColorPrinterTest))
    suite.addTest(makeSuite(ConfigReaderTest))
    suite.addTest(makeSuite(DependenciesTest))

    return suite


if __name__ == '__main__':
    suite = suite()
    runner = unittest.TextTestRunner()
    success = not runner.run(suite).wasSuccessful()

    sys.exit(success)
