""" The script that makes this directory an executable script. """

import sys
import os

sys.path.insert(0, os.getcwd())

from gitssue import gitssue


if __name__ == '__main__':
    gitssue.cli()
