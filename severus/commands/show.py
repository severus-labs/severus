import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers

@click.command()
@click.argument('name')
@click.pass_context
def show(ctx: click.Context, name: str):
    """Show details of a vault item"""
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
    
    # Load encrypted data
    file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]
    
    try:
        data = encryption.load_encrypted_file(file_path, totp_secret)
    except Exception:
        click.echo(f"Error: Could not decrypt '{name}'.")
        return
    
    # Get item type from vault database
    conn = vault.sqlite3.connect(vault_path)
    cursor = conn.execute('SELECT type FROM vault WHERE name = ?', (name_slug,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        click.echo(f"Error: Item '{name}' not found in vault.")
        return
    
    item_type = result[0]
    
    # Display based on type
    if item_type == 'secret':
        display_name = data.get('name', name_slug)
        click.echo(display_name)
        
        url = data.get('url', '')
        username = data.get('username', '')
        password = data.get('password', '')
        project = data.get('project', '')
        
        if url:
            click.echo(f"  URL: {url}")
        if username:
            click.echo(f"  Username: {username}")
        if password:
            click.echo(f"  Password: {password}")
        if project:
            click.echo(f"  Project: {project}")
    
    elif item_type == 'note':
        display_name = data.get('name', name_slug)
        body = data.get('body', '')
        
        click.echo(display_name)
        if body:
            click.echo(body)
    
    elif item_type == 'env':
        filename = data.get('filename', '.env')
        content = data.get('content', '')
        project = data.get('project', '')
        directory = data.get('directory', '')
        
        click.echo(f"{filename}")
        if project:
            click.echo(f"  Project: {project}")
        if directory:
            click.echo(f"  Directory: {directory}")
        click.echo("  Content:")
        for line in content.splitlines():
            click.echo(f"    {line}")
    
    else:
        click.echo(f"Unknown item type: {item_type}")