import click
from severus.commands import initialize

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """Severus: A tool for managing secrets."""
    ctx.obj = {}

cli.add_command(initialize.init)