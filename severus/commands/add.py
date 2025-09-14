import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers
from severus.utils import info

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
    
    # email
    email = auth.load_config(config_path).get("email")
    
    # Update or insert in database
    if is_update:
        vault.update_vault_item(vault_path, name, "secret", file_path, project or None, email)
        click.echo(f"✓ Secret '{name}' updated.")
    else:
        vault.insert_vault_item(vault_path, name, "secret", file_path, project or None, email)
        click.echo(f"✓ Secret '{name}' added to vault.")

@add.command() 
@click.pass_context
def note(ctx: click.Context):
    """Add a note"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return

    name = click.prompt("Name (e.g. 'Server Restart Instructions')")
    name_slug = helpers.slugify(name)
    
    # Check if exists and get confirmation early
    is_update = False
    if vault.item_exists(vault_path, name_slug):
        if not click.confirm(f"Warning: '{name_slug}' already exists. Overwrite?"):
            click.echo("Operation cancelled.")
            return
        is_update = True

    info.editor(name_slug)

    # Use click's editor for multiline input
    body = click.edit("# Enter your note content here")
    if body is None:
        click.echo("Note cancelled.")
        return
    
    # Remove comment lines
    # body = '\n'.join(line for line in body.split('\n') if not line.strip().startswith('#'))
    
    project = click.prompt("Project (optional, e.g. 'myapp-backend')", default="", show_default=False)

    # Prepare data
    data = {
        "name": name,
        "body": body.strip(),
        "project": project or None
    }

    # Save encrypted file
    file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    encryption.save_encrypted_file(data, file_path, totp_secret)

    # email
    email = auth.load_config(config_path).get("email")
    
    # Update or insert in database
    if is_update:
        vault.update_vault_item(vault_path, name_slug, "note", file_path, project or None, email)
        click.echo(f"✓ Note '{name}' updated.")
    else:
        vault.insert_vault_item(vault_path, name_slug, "note", file_path, project or None, email)
        click.echo(f"✓ Note '{name}' added to vault.")

@add.command()
@click.argument('filename')
@click.pass_context
def file(ctx: click.Context, filename: str):
    """Import a file as a note"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    # Check if file exists
    from pathlib import Path
    file_path = Path(filename)
    if not file_path.exists():
        click.echo(f"Error: File '{filename}' not found.")
        return
    
    # Use filename as note name
    name = file_path.name
    name_slug = helpers.slugify(name)
    
    # Check if exists and get confirmation
    is_update = False
    if vault.item_exists(vault_path, name_slug):
        if not click.confirm(f"Warning: '{name_slug}' already exists. Overwrite?"):
            click.echo("Operation cancelled.")
            return
        is_update = True
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            # Try with different encoding for binary-ish files
            with open(file_path, 'r', encoding='latin1') as f:
                content = f.read()
        except Exception as e:
            click.echo(f"Error: Could not read file '{filename}': {e}")
            return
    except Exception as e:
        click.echo(f"Error: Could not read file '{filename}': {e}")
        return
    
    click.echo(f"Importing {filename} as note...")
    
    # Get current directory for project context
    current_dir = Path.cwd()
    project = helpers.slugify(current_dir.name)
    
    # Prepare data
    data = {
        "name": name,
        "body": content,
        "project": project,
        "original_filename": filename,
        "imported_from": str(file_path.absolute())
    }
    
    # Save encrypted file
    encrypted_file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    encryption.save_encrypted_file(data, encrypted_file_path, totp_secret)
    
    # Get email
    email = auth.load_config(config_path).get("email")
    
    # Update or insert in database
    if is_update:
        vault.update_vault_item(vault_path, name_slug, "note", encrypted_file_path, project, email)
    else:
        vault.insert_vault_item(vault_path, name_slug, "note", encrypted_file_path, project, email)
    
    click.echo(f"✓ Note '{name}' saved to vault.")