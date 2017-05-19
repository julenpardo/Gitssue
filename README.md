Gitssue [![PyPI version](https://badge.fury.io/py/Gitssue.svg)](https://badge.fury.io/py/Gitssue)
=======

[![Build Status](https://api.travis-ci.org/julenpardo/Gitssue.svg?branch=dev)](https://travis-ci.org/julenpardo/Gitssue)
[![Coverage Status](https://coveralls.io/repos/github/julenpardo/Gitssue/badge.svg?branch=dev)](https://coveralls.io/github/julenpardo/Gitssue?branch=dev)
![Python versions](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

Manage your issues from the command line.

Built on [Cement Framework](http://builtoncement.com/).

![img/demo.gif](img/demo.gif)

# Features

 - Authentication.
 - List the issues (also closed ones, if specified).
 - Get issues descriptions.
 - Get comment thread of the issue.
 - Show tags of each issue, with its colors!

# Limitations

 - Just for repositories hosted on GitHub.
 - No "write" operations (i.e. make a comment, open or close issues, etc.).

# Installation

Just with `pip3`:

 ```
 pip3 install gitssue
 ```

 That's it! You can already execute `gitssue` in your shell.

# Configuration

This is optional, just if you want to use authentication (necessary for private repositories).

Take a look to the [.gitssuerc.example](.gitssuerc.example) file, and follow these steps:

 - Change the values of the example file with the real ones.
 - Rename it to `.gitssuerc`.
 - Place it in your home directory (`~/.gitssuerc`), or in `/etc/`. **If a config file exists in both directories, the one of the home directory will be the one used.**
 - Check the permissions! The config file stores your credentials, so you will probably want to have permissions like `500` (read and write permissions for the owner, and no permissions for any  other) or similar.

# Upcoming features

 - Look at [limitations](#limitations) :)
