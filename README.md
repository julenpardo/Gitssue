# Gitssue [![PyPI version](https://badge.fury.io/py/Gitssue.svg)](https://badge.fury.io/py/Gitssue)

[![Build Status](https://api.travis-ci.org/julenpardo/Gitssue.svg?branch=dev)](https://travis-ci.org/julenpardo/Gitssue)
[![Coverage Status](https://coveralls.io/repos/github/julenpardo/Gitssue/badge.svg?branch=dev)](https://coveralls.io/github/julenpardo/Gitssue?branch=dev)
![Python versions](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6%2C%203.7--dev-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

Manage your Github, Gitlab or Bitbucket issues from the command line.

Built on [Cement Framework](http://builtoncement.com/).

![img/demo.gif](img/demo.gif)

## Features

* Compatible with Github, Bitbucket and Gitlab (gitlab.com and self hosted
  installations).
* Authentication.
* List the issues.
* Get issues descriptions.
* Get comment thread of the issue.
* Show tags of each issue, with its colors.

## Limitations

* No "write" operations (i.e. make a comment, open or close issues, etc.).

## Installation

Just with `pip3`:

```
pip3 install gitssue
```

That's it! You can already execute `gitssue` in your shell. You don't have to
specify the link to the tracker or the remote type (Github, Gitlab or
Bitbucket); it's already done by Gitssue.

## Configuration

This is optional, just if you want to use authentication (**necessary for Github
and Bitbucket private repositories, and Gitlab repositories**).

Take a look to the [.gitssuerc.example](.gitssuerc.example) file, and follow these
steps:

* Change the values of the example file with the real ones.
* Rename it to `.gitssuerc`.
* Place it in your home directory (`~/.gitssuerc`), or in `/etc/`. **If a config
  file exists in both directories, the one of the home directory will be the one
  used.**
* Check the permissions! The config file stores your credentials, so you will
  probably want to have permissions like `500` (read and write permissions for
  the owner, and no permissions for any other) or similar.

### Gitlab access token

Even if the repository is public, you need an access token. This can be
generated under `Settings/Access Tokens`, with the `api` scope.
