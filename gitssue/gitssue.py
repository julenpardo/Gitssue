""" CLI module (the main module of the app, since it's a CLI app). """


import sys
import os

sys.path.insert(0, os.getcwd())

from gitssue.dependencies.dependencies import Dependencies
from gitssue.controller.controller import Controller

GITSSUE_VERSION = '1.3'



class Gitssue():
    """
    Main class.
    """

    def run(self):
        print('run')
