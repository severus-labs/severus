import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers

@click.group()
@click.pass_context
def add(ctx: click.Context):
    """Add items to vault"""
    pass

@add.command()
@click.pass_context
def secret(ctx: click.Context):
    """Add a secret"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return

    name = click.prompt("Name (e.g. 'stripe-account')")
    name = helpers.slugify(name)
    
    # Check if exists and get confirmation early
    is_update = False
    if vault.item_exists(vault_path, name):
        if not click.confirm(f"Warning: '{name}' already exists. Overwrite?"):
            click.echo("Operation cancelled.")
            return
        is_update = True

    # Collect all the data
    url = click.prompt("URL (optional, e.g. 'https://dashboard.stripe.com')", default="", show_default=False)
    username = click.prompt("Username (optional, e.g. 'admin@company.com')", default="", show_default=False) 
    password = click.prompt("Password", hide_input=True)
    project = click.prompt("Project (optional, e.g. 'myapp-backend')", default="", show_default=False)

    # Prepare data
    data = {
        "name": name,
        "url": url,
        "username": username,
        "password": password,
        "project": project or None
    }

    # Save encrypted file
    file_path = blobs_directory / f"{name}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    encryption.save_encrypted_file(data, file_path, totp_secret)
    
    # Update or insert in database
    if is_update:
        vault.update_vault_item(vault_path, name, "secret", file_path, project or None)
        click.echo(f"✓ Secret '{name}' updated.")
    else:
        vault.insert_vault_item(vault_path, name, "secret", file_path, project or None)
        click.echo(f"✓ Secret '{name}' added to vault.")

@add.command() 
@click.pass_context
def note(ctx: click.Context):
    """Add a note"""
    click.echo("Adding note...")
