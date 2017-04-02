Gitssue [![PyPI version](https://badge.fury.io/py/Gitssue.svg)](https://badge.fury.io/py/Gitssue)
=======

[![Build Status](https://api.travis-ci.org/julenpardo/Gitssue.svg?branch=dev)](https://travis-ci.org/julenpardo/Gitssue)
[![Coverage Status](https://coveralls.io/repos/github/julenpardo/Gitssue/badge.svg?branch=dev)](https://coveralls.io/github/julenpardo/Gitssue?branch=dev)
![Python versions](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

Manage your issues from the command line.

![img/demo.gif](img/demo.gif)

# Features

 - List the issues (also closed ones, if specified).
 - Get issues descriptions.
 - Get comment thread of the issue.
 - Show tags of each issue, with its colors!

# Limitations

 - Just for repositories hosted on GitHub.
 - No support for authentication.
 - Because of the previous one, there's no support for private repositories.
 - GitHub API limitation: also related to the authentication; for non authenticated requests, GitHub has a limit of 60 requests/hour to the API.
 - No "write" operations (i.e. make a comment, open or close issues, etc.).

# Installation

Just with `pip3`:

 ```
 pip3 install gitssue
 ```

 That's it! You can already execute `gitssue` in your shell.

# Upcoming features

 - Look at [limitations](#limitations) :)
