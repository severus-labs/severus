import click

@click.command()
@click.argument("name")
@click.pass_context

def share(ctx: click.Context, name: str):
    pass