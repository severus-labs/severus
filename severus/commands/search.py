import click
from severus.utils import auth
from severus.utils import vault

@click.command()
@click.argument('query')
@click.pass_context
def search(ctx: click.Context, query: str):
    """Search items in vault by name"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    
    if not auth.authenticate(config_path):
        return
    
    # Search for items
    results = vault.search_vault_items(vault_path, query)
    
    if not results:
        click.echo(f"No items found matching '{query}'.")
        return
    
    click.echo(f"Found {len(results)} item{'s' if len(results) != 1 else ''}:")
    
    for item in results:
        item_type = item['type']
        name = item['name']
        
        # Add extra context for secrets
        if item_type == 'secret':
            # You could load and decrypt to get URL, but keeping it simple
            click.echo(f"[{item_type}] {name}")
        else:
            click.echo(f"[{item_type}] {name}")