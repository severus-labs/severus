import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers
from severus.utils import sharing

@click.command()
@click.argument("code")
@click.pass_context
def receive(ctx: click.Context, code: str):
    """Receive a shared vault item"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    # Clean up the code (remove extra spaces, normalize case)
    share_code = code.upper().strip()
    
    click.echo("Retrieving shared secret...")
    
    # Download encrypted data
    try:
        encrypted_data = sharing.download_shared_data(share_code)
    except Exception as e:
        click.echo(f"Error: {e}")
        return
    
    # Decrypt the data
    try:
        share_data = sharing.decrypt_from_sharing(encrypted_data, share_code)
    except Exception:
        click.echo("Error: Could not decrypt shared data. Invalid code?")
        return
    
    # Extract the actual item data
    item_type = share_data.get("type")
    item_data = share_data.get("data", {})
    item_name = item_data.get("name", "shared-item")
    
    if not item_type or not item_data:
        click.echo("Error: Invalid shared data format.")
        return
    
    # Generate name for local vault
    name_slug = helpers.slugify(item_name)
    
    # Check if item already exists
    if vault.item_exists(vault_path, name_slug):
        if not click.confirm(f"Warning: '{item_name}' already exists in your vault. Overwrite?"):
            click.echo("Operation cancelled.")
            return
    
    # Save to local vault
    file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    encryption.save_encrypted_file(item_data, file_path, totp_secret)
    
    # Get email and project info
    email = auth.load_config(config_path).get("email")
    project = item_data.get("project")
    
    # Save to database
    if vault.item_exists(vault_path, name_slug):
        vault.update_vault_item(vault_path, name_slug, item_type, file_path, project, email)
    else:
        vault.insert_vault_item(vault_path, name_slug, item_type, file_path, project, email)
    
    # Show success message
    item_type_display = item_type.capitalize()
    click.echo(f"✓ {item_type_display} '{item_name}' added to your vault.")