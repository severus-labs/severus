import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import helpers

@click.command()
@click.argument('name')
@click.pass_context
def delete(ctx: click.Context, name: str):
    """Delete an item from the vault"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    name_slug = helpers.slugify(name)
    
    # Check if item exists
    if not vault.item_exists(vault_path, name_slug):
        click.echo(f"Error: Item '{name}' not found.")
        return
    
    # Get item type for display message
    item_type = vault.get_vault_item_by_name(vault_path, name_slug)
    if not item_type:
        click.echo(f"Error: Item '{name}' not found in vault.")
        return
    
    # Confirm deletion
    if not click.confirm(f"Warning: This will permanently delete '{name}'. Continue?"):
        click.echo("Delete cancelled.")
        return
    
    # Delete encrypted file
    file_path = blobs_directory / f"{name_slug}.enc"
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        click.echo(f"Error: Could not delete encrypted file: {e}")
        return
    
    # Delete from database
    vault.delete_vault_item(vault_path, name_slug)
    
    # Display success message with proper capitalization
    item_type_display = item_type.capitalize()
    click.echo(f"{item_type_display} '{name}' deleted.")