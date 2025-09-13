import click

@click.group()
@click.pass_context
def add(ctx: click.Context,):
    """Add items to vault"""
    pass

@add.command()
@click.pass_context
def secret(ctx: click.Context,):
    """Add a secret"""
    click.echo("Adding secret...")

@add.command() 
@click.pass_context
def note(ctx: click.Context,):
    """Add a note"""
    click.echo("Adding note...")
