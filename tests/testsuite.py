import unittest

from controller_test import ControllerTest
from git_wrapper_test import GitWrapperTest
from github_test import GithubTest
from gitlab_test import GitlabTest
from printer_test import PrinterTest
from shell_wrapper_test import ShellWrapperTest
from requests_test import RequestsTest
from colorconsole_color_printer_test import ColorConsoleColorPrinterTest
from config_reader_test import ConfigReaderTest
from dependencies_test import DependenciesTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(ControllerTest)
    suite.addTest(GitWrapperTest)
    suite.addTest(GithubTest)
    suite.addTest(GitlabTest)
    suite.addTest(PrinterTest)
    suite.addTest(ShellWrapperTest)
    suite.addTest(RequestsTest)
    suite.addTest(ColorConsoleColorPrinterTest)
    suite.addTest(ConfigReaderTest)
    suite.addTest(DependenciesTest)

    return suite


if __name__ == '__main__':
    unittest.main()
