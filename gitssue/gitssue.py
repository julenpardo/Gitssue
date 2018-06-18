""" CLI module (the main module of the app, since it's a CLI app). """


import sys
import os
import click

sys.path.insert(0, os.getcwd())

from gitssue.dependencies.dependencies import Dependencies
from gitssue.controller.controller import Controller

GITSSUE_VERSION = '1.4.0'

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}

controller = Controller(Dependencies())

def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    print('Gitssue {0}'.format(GITSSUE_VERSION))
    context.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version and exit.')
@click.option('--debug', '-d', is_flag=True, help='Show debug messages.')
def cli(debug):
    if debug:
        controller.enable_debug()


@click.command(help='List open issues.')
@click.option('--all', '-a', is_flag=True, help='Show also closed issues.')
@click.option('--desc', '-d', is_flag=True,
              help='Get description of the issues.')
def list(all, desc):
    controller.list(all, desc)


@click.command(help='Get description of specified issue(s).')
@click.argument('issues', nargs=-1, type=click.INT)
@click.pass_context
def desc(context, issues):
    if len(issues) == 0:
        print('Usage: gitssue desc [OPTIONS] [issue [issue ...]]\n')
        print('Error: Missing argument "issue".')
        context.exit(2)
    controller.desc(issues)


@click.command(help='Get the comments of specified issue.')
@click.argument('issue', nargs=1, type=click.INT)
def comments(issue):
    controller.comments(issue)


@click.command(help='Add a comment to the specified issue.')
@click.argument('issue', nargs=1, type=click.INT)
@click.argument('comment', nargs=1, type=click.STRING)
def comment(issue, comment):
    controller.comment(issue, comment)


@click.command(help='Shows the API rate information (remaining requests, reset'
                    ' time, etc.).')
def rate_info():
    controller.rate_information()


@click.command(help='Close specified issue(s).')
@click.argument('issues', nargs=-1, type=click.INT)
@click.pass_context
def close(context, issues):
    if len(issues) == 0:
        print('Usage: gitssue close [OPTIONS] [issue [issue ...]]\n')
        print('Error: Missing argument "issue".')
        context.exit(2)
    controller.close(issues)


cli.add_command(list)
cli.add_command(desc)
cli.add_command(comments)
cli.add_command(comment)
cli.add_command(close)
cli.add_command(rate_info)
