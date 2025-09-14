import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers
from severus.utils import info

@click.group()
@click.pass_context
def env(ctx: click.Context):
    """Manage environment variables"""
    pass

@env.command()
@click.pass_context
def save(ctx: click.Context):
    pass

@env.command()
@click.pass_context
def restore(ctx: click.Context):
    pass
