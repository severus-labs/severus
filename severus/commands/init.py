import click
from severus.utils import config, totp, vault

@click.command()
@click.option(
    "--email",
    prompt="Enter your email",
    confirmation_prompt=True,
    help="The email associated with your account",
)
@click.pass_context
def init(ctx: click.Context, email: str) -> None:
    """Initialize Severus"""
    vault_path = ctx.obj["vault_path"]
    config_path = ctx.obj["config_path"]
    blobs_directory = ctx.obj["blobs_directory"]

    # Check if already initialized
    if config_path.exists():
        click.echo("Severus is already initialized.")
        if not click.confirm("This will delete your existing vault and configuration. Continue?"):
            click.echo("Initialization cancelled.")
            return
        
        # Remove existing files
        config_path.unlink()
        if vault_path.exists():
            vault_path.unlink()

         # Remove blobs directory and all contents
        if blobs_directory.exists():
            import shutil
            shutil.rmtree(blobs_directory)

    banner = """\
┌──────────────────────────────────────────────────────┐
│                    Welcome to Severus                │
│           Your Local-First Encrypted Vault           │
└──────────────────────────────────────────────────────┘"""
    click.echo(banner)
    click.echo("Setting up your vault...\n")

    totp_secret = totp.generate_totp_secret()

    click.echo("Scan this QR code with your authenticator app:")
    totp.generate_qr_code(totp_secret, email, "Severus")

    # Prompt the user for the 6-digit TOTP code
    user_token = click.prompt(
        "Enter the 6-digit code from your authenticator", 
        type=str, 
        hide_input=True
    )

   # Verify the TOTP
    if totp.verify_totp(totp_secret, user_token):
        click.echo("\nAuthentication verified!")

        # Create vault file
        vault.create_vault_db(vault_path)

        # Create secret file
        config.save_config(config_path, email, totp_secret)

        click.echo(f"\n✓ Vault ready at {vault_path}")
        # click.echo(f"✓ Secret key stored at {secret_path} (keep secure)\n")
        click.echo(f"✓ Configuration saved to {config_path} (keep secure)\n")
    else:
        click.echo("\nInvalid code! Please try again.")
        return  # optionally exit or loop until valid

    click.echo("Run 'severus help' to get started.")