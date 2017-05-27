""" The script that makes this directory an executable script. """

import sys
import os

sys.path.insert(0, os.getcwd())

from gitssue.gitssue import Gitssue

with Gitssue() as app:
    app.run()
