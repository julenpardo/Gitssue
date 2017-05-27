""" Configuration reader. """

import configparser
import os

FILENAME = '.gitssuerc'
FILE_PATHS = (
    os.path.expanduser('~') + '/',
    '/etc/gitssue/',
)
PARSER_DEFAULTS = ({
    'password': ''
})


def get_config():
    """
    Reads the config file defined in the FILE_PATHS tuple, keeping the priority. That is,
    the config will be set for the first file found, exiting the loop in that moment and
    returning the value.
    If no file was found, an empty dictionary will be returned.
    :return: A dictionary with the config, in "{'remote':{'username':'...'}..." format.
    """
    config = {}
    parser = configparser.ConfigParser(PARSER_DEFAULTS)

    for file_path in FILE_PATHS:
        file = file_path + FILENAME
        exists_and_not_empty = os.path.isfile(file) \
            and os.path.getsize(file) > 0

        if not exists_and_not_empty:
            continue

        parser.read(file)
        for remote in parser.sections():
            config[remote] = {
                'username': parser.get(remote, 'username'),
                'password': parser.get(remote, 'password'),
            }

        break

    return config
