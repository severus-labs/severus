import click
from pathlib import Path
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers

@click.group()
@click.pass_context
def env(ctx: click.Context):
    """Manage environment variables"""
    pass

@env.command()
@click.argument('env_name', required=False)
@click.pass_context
def save(ctx: click.Context, env_name: str):
    """Save .env file(s) to vault"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    current_dir = Path.cwd()
    project_name = helpers.slugify(current_dir.name)
    totp_secret = auth.load_config(config_path)["secret"]
    
    # If specific env_name provided, save only that file
    if env_name:
        env_file = current_dir / env_name
        if not env_file.exists():
            click.echo(f"File '{env_name}' not found in current directory.")
            return
        env_files = [env_file]
    else:
        # Find all .env files in current directory
        env_files = list(current_dir.glob('.env*'))
        if not env_files:
            click.echo("No .env files found in current directory.")
            return
    
    saved_count = 0
    
    # Process each .env file separately
    for env_file in env_files:
        # Generate name: myapp-env, myapp-env-local, myapp-env-development, etc.
        if env_file.name == '.env':
            env_name = f"{project_name}-env"
        else:
            # .env.local -> myapp-env-local, .env.development -> myapp-env-development
            suffix = env_file.name.replace('.env.', '')
            env_name = f"{project_name}-env-{suffix}"
        
        env_slug = helpers.slugify(env_name)
        
        # Check if exists
        if vault.item_exists(vault_path, env_slug):
            if not click.confirm(f"Warning: '{env_slug}' already exists. Overwrite?"):
                click.echo(f"Skipped {env_file.name}")
                continue
        
        # Read file content
        try:
            with open(env_file, 'r') as f:
                content = f.read()
        except Exception as e:
            click.echo(f"Warning: Could not read {env_file.name}: {e}")
            continue
        
        # Prepare data
        data = {
            "project": project_name,
            "directory": str(current_dir),
            "filename": env_file.name,
            "content": content
        }
        
        # Save encrypted file
        file_path = blobs_directory / f"{env_slug}.enc"
        encryption.save_encrypted_file(data, file_path, totp_secret)
        
        # email
        email = auth.load_config(config_path).get("email")
        
        # Insert/update in database
        if vault.item_exists(vault_path, env_slug):
            vault.update_vault_item(vault_path, env_slug, "env", file_path, project_name, email)
        else:
            vault.insert_vault_item(vault_path, env_slug, "env", file_path, project_name, email)
        click.echo(f"✓ Saved {env_file.name} as '{env_slug}'")
        saved_count += 1
    
    if saved_count > 0:
        click.echo(f"✓ Successfully saved {saved_count} environment file(s).")
    else:
        click.echo("No files were saved.")

@env.command()
@click.argument('env_name', required=False)
@click.pass_context
def restore(ctx: click.Context, env_name: str):
    """Restore environment file(s) to current directory"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]
    
    if not auth.authenticate(config_path):
        return
    
    current_dir = Path.cwd()
    project_name = helpers.slugify(current_dir.name)

    
    # If specific env_name provided, restore only that
    if env_name:
        resolved_name = helpers.resolve_env_name(env_name, project_name)
        if not vault.item_exists(vault_path, resolved_name):
            click.echo(f"Environment '{env_name}' not found in vault.")
            return
        env_items = [(resolved_name, str(blobs_directory / f"{resolved_name}.enc"))]
    else:
        # Auto-detect project name and restore all env files for project
        click.echo(f"Current directory: {current_dir}")
        env_items = vault.get_env_items_by_project(vault_path, project_name)
        
        if not env_items:
            click.echo(f"No environment files found for project '{project_name}'")
            return
    
    totp_secret = auth.load_config(config_path)["secret"]
    restored_count = 0
    
    # Restore each environment file
    for name, file_path in env_items:
        try:
            # Load encrypted data
            data = encryption.load_encrypted_file(file_path, totp_secret)
            filename = data.get("filename", ".env")
            content = data.get("content", "")
            
            # Write to current directory
            output_path = current_dir / filename
            
            # Check if file exists
            if output_path.exists():
                if not click.confirm(f"'{filename}' already exists. Overwrite?"):
                    click.echo(f"Skipped {filename}")
                    continue
            
            with open(output_path, 'w') as f:
                f.write(content)
            
            click.echo(f"✓ Restored {filename}")
            restored_count += 1
            
        except Exception as e:
            click.echo(f"Error restoring {name}: {e}")
    
    if restored_count > 0:
        if env_name:
            click.echo(f"✓ Restored {env_name} to {current_dir}")
        else:
            project_name = helpers.slugify(current_dir.name)
            click.echo(f"✓ Restored {project_name} environment ({restored_count} files) to {current_dir}")
    else:
        click.echo("No files were restored.")