""" The script that makes this directory an executable script. """

import sys
import os
import click

sys.path.insert(0, os.getcwd())

from gitssue.gitssue import Gitssue

# gitssue = Gitssue()
# gitssue.run()


@click.group()
def cli():
    pass


@click.command(help='List open issues.')
@click.option('--all', '-a', is_flag=True, help='Show also closed issues.')
def list(all):
    print(all)


@click.command(help='Get description of specified issue(s).')
@click.argument('issues', nargs=-1)
def desc(issues):
    print(issues)


@click.command(help='Get the comments of specified issue.')
@click.argument('issue', nargs=1, type=click.INT)
def thread(issue):
    print(issue)


@click.command(help='Shows the API rate information (remaining requests, reset'
                    ' time, etc.).')
def rate_info():
    print('rate info')


cli.add_command(list)
cli.add_command(desc)
cli.add_command(thread)
cli.add_command(rate_info)

if __name__ == '__main__':
    cli()
