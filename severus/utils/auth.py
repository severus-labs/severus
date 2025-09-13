import click
from severus.utils.config import load_config
from severus.utils.totp import verify_totp

def authenticate(config_path):
    """Prompt for TOTP and verify against stored secret"""
    config = load_config(config_path)
    if not config:
        click.echo("Vault not initialized. Run 'severus init' first.")
        return False
    
    user_token = click.prompt(
        "Enter TOTP code", 
        type=str, 
        hide_input=True
    )
    
    if verify_totp(config["secret"], user_token):
        return True
    else:
        click.echo("Invalid TOTP code.")
        return False