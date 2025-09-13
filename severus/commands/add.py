import click
from severus.utils import auth

@click.group()
@click.pass_context
def add(ctx: click.Context):
    """Add items to vault"""
    pass

@add.command()
@click.pass_context
def secret(ctx: click.Context):
    """Add a secret"""
    config_path = ctx.obj["config_path"]
    if not auth.authenticate(config_path):
        return

    name = click.prompt("Name (e.g. 'stripe-account')")
    url = click.prompt("URL (optional, e.g. 'https://dashboard.stripe.com')", default="", show_default=False)
    username = click.prompt("Username (optional, e.g. 'admin@company.com')", default="", show_default=False) 
    password = click.prompt("Password", hide_input=True)
    project = click.prompt("Project (optional, e.g. 'myapp-backend')", default="", show_default=False)

@add.command() 
@click.pass_context
def note(ctx: click.Context):
    """Add a note"""
    click.echo("Adding note...")
