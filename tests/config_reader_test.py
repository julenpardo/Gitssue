import os
import unittest
from gitssue.config import config_reader

TESTING_FILE_PATH = os.path.realpath(__file__)
TESTING_FILE_PATH = TESTING_FILE_PATH.replace('config_reader_test.py', '')


def create_file_overwriting(contents):
    with open(TESTING_FILE_PATH + config_reader.FILENAME, 'w') as file:
        file.write(contents)


def remove_testing_file():
    try:
        os.remove(TESTING_FILE_PATH + config_reader.FILENAME)
    except FileNotFoundError:
        pass


class ConfigReaderTest(unittest.TestCase):

    def setUp(self):
        """
        Replaces the production config files with the testing file path.
        """
        config_reader.FILE_PATHS = (TESTING_FILE_PATH,)

    def tearDown(self):
        remove_testing_file()

    def test_get_config_non_existing_file(self):
        remove_testing_file()

        expected = {}
        actual = config_reader.get_config()

        self.assertEqual(expected, actual)

    def test_get_config_empty_file(self):
        create_file_overwriting('')

        expected = {}
        actual = config_reader.get_config()

        self.assertEqual(expected, actual)

    def test_get_config(self):
        config_file = '[github]\n' \
                      + 'username = whatever\n' \
                      + 'password = whatever'

        create_file_overwriting(config_file)

        expected = {
            'github': {
                'username': 'whatever',
                'password': 'whatever',
                'token': '',
            }
        }
        actual = config_reader.get_config()

        self.assertEqual(expected, actual)
