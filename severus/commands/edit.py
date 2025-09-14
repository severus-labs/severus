import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers
from severus.utils import info

@click.group()
@click.pass_context
def edit(ctx: click.Context):
    """Edit items in the vault"""
    pass

@edit.command()
@click.argument('name')
@click.pass_context
def note(ctx: click.Context, name: str):
    """Edit an existing note"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    name_slug = helpers.slugify(name)
    
    # Check if note exists
    if not vault.item_exists(vault_path, name_slug):
        click.echo(f"Error: Note '{name_slug}' not found.")
        return
    
    # Load existing note
    file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    
    try:
        existing_data = encryption.load_encrypted_file(file_path, totp_secret)
        current_body = existing_data.get("body", "")
    except Exception:
        click.echo(f"Error: Could not decrypt note '{name_slug}'.")
        return

    info.editor(name_slug)

    # Open editor with existing content
    body = click.edit(current_body)
    if body is None:
        click.echo("Edit cancelled.")
        return
    
    # Update the data
    existing_data["body"] = body.strip()
    
    # Save updated file
    encryption.save_encrypted_file(existing_data, file_path, totp_secret)
    
    # Update timestamp in database
    vault.update_vault_item(vault_path, name_slug)
    
    click.echo(f"✓ Note '{name_slug}' updated.")