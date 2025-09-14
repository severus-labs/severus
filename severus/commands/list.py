import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import helpers

@click.command()
@click.pass_context
def list(ctx: click.Context):
    """List items in vault"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    
    if not auth.authenticate(config_path):
        return
    
    # Get all items from vault
    items = vault.get_all_vault_items(vault_path)
    
    if not items:
        click.echo("Your vault is empty.")
        return
    
    # Group items by type
    secrets = [item for item in items if item['type'] == 'secret']
    notes = [item for item in items if item['type'] == 'note']
    envs = [item for item in items if item['type'] == 'env']
    
    total_count = len(items)
    click.echo(f"Your Vault ({total_count} items):")
    
    if secrets:
        click.echo("Secrets:")
        for item in secrets:
            time_ago = helpers.time_ago(item['created_at'])
            click.echo(f"  {item['name']:<25} (saved {time_ago})")
        click.echo()
    
    if notes:
        click.echo("Notes:")
        for item in notes:
            time_ago = helpers.time_ago(item['created_at'])
            click.echo(f"  {item['name']:<25} (saved {time_ago})")
        click.echo()
    
    if envs:
        click.echo("Environments:")
        for item in envs:
            time_ago = helpers.time_ago(item['created_at'])
            click.echo(f"  {item['name']:<25} (saved {time_ago})")