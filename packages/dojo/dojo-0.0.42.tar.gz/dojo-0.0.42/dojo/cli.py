import click
import logging

from .run import Entrypoint
from .secrets import Secrets


@click.group()
def cli():
    pass


@cli.command(help='Run a dojo job')
@click.argument('name')
@click.option('--runner', default=None, help='specify a runner for the job')
@click.option('--config', default='config', help='path to directory containing configuration files to be merged')
@click.option('--env', default='development', help='environment used to select configuration and secrets')
@click.pass_context
def run(context, name, runner, config, env):
    if context.obj is None:
        context.obj = {}
    logging.getLogger().setLevel(logging.INFO)
    Entrypoint().run(name, runner, config, env)


@cli.command(help='Encrypt secrets')
@click.option('--config', default='config', help='path to directory containing configuration files to be merged')
@click.option('--env', default='development', help='environment used to select configuration and secrets')
@click.pass_context
def encrypt(context, config, env):
    Secrets().encrypt(config, env)
