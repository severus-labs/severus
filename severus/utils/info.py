import click

def editor(name_slug):
    click.echo(f"Opening editor for note '{name_slug}'...")
    click.echo("Save and close the file to continue, or close without saving to cancel.")