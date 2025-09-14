import click
from pathlib import Path
from severus.commands import init, add, edit, env, list, search, show

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """Severus: A tool for managing secrets."""
    root_directory = Path.home() / ".severus"
    root_directory.mkdir(exist_ok=True)

    blobs_directory = root_directory / "blobs"
    blobs_directory.mkdir(exist_ok=True)
    
    vault_path = root_directory / "vault.db"
    config_path = root_directory / "config.json"

    ctx.obj = { 
        "root_directory": root_directory, 
        "vault_path": vault_path, 
        "config_path": config_path,
        "blobs_directory": blobs_directory
    }

cli.add_command(init.init)
cli.add_command(add.add)
cli.add_command(edit.edit)
cli.add_command(env.env)
cli.add_command(list.list)
cli.add_command(search.search)
cli.add_command(show.show)