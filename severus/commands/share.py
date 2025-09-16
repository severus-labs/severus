import click
from severus.utils import auth
from severus.utils import vault
from severus.utils import encryption
from severus.utils import helpers
from severus.utils import sharing
import base64

@click.command()
@click.argument("name")
@click.pass_context
def share(ctx: click.Context, name: str):
    """Share a vault item securely"""
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

    # Get item type and load data
    item_type = vault.get_vault_item_by_name(vault_path, name_slug)
    if not item_type:
        click.echo(f"Error: Item '{name}' not found in vault.")
        return

    # Load encrypted data
    file_path = blobs_directory / f"{name_slug}.enc"
    totp_secret = auth.load_config(config_path)["secret"]

    try:
        data = encryption.load_encrypted_file(file_path, totp_secret)
    except Exception:
        click.echo(f"Error: Could not decrypt '{name}'.")
        return

    # Add metadata for sharing
    share_data = {
        "type": item_type,
        "data": data,
        "shared_by": "severus_user",  # Could use email from config
        "shared_at": helpers.datetime.now().isoformat()
    }

    click.echo("Encrypting and uploading...")

    # Generate unique share ID
    max_attempts = 5
    share_id = None

    for attempt in range(max_attempts):
        candidate_id = sharing.generate_share_id()
        if sharing.check_code_availability(candidate_id):
            share_id = candidate_id
            break
        click.echo(f"ID collision, retrying... ({attempt + 1}/{max_attempts})")

    if not share_id:
        click.echo("Error: Could not generate unique share ID. Please try again.")
        return

    # Generate private key
    private_key = sharing.generate_private_key()

    # Encrypt data with private key
    try:
        encrypted_data = sharing.encrypt_for_sharing(share_data, private_key)
    except Exception as e:
        click.echo(f"Error: Could not encrypt data: {e}")
        return

    # Upload to server (ID + encrypted blob, NO private key)
    if sharing.upload_shared_data(share_id, encrypted_data):
        private_key_str = base64.urlsafe_b64encode(private_key).decode()
        click.echo(f"✓ Share ID: {share_id}")
        click.echo(f"✓ Private Key: {private_key_str}")
        click.echo(f"Tell recipient: {click.style(f'severus receive {share_id}', fg='cyan', bold=True)}")
        click.echo("Share both to recipient. Expires in 10 minutes.")
    else:
        click.echo("Error: Could not upload to server. Please try again.")