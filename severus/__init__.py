import click
from severus.commands import initialize
from pathlib import Path

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """Severus: A tool for managing secrets."""
    directory = Path.home() / ".severus"
    directory.mkdir(exist_ok=True)
    
    vault_path = directory / "vault.db"
    config_path = directory / "config.json"

    ctx.obj = { 
        "directory": directory, 
        "vault_path": vault_path, 
        "config_path": config_path
    }

cli.add_command(initialize.init)