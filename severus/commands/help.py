import click

@click.command()
@click.argument('command', required=False)
@click.pass_context
def help(ctx: click.Context, command: str):
    """Show help information about Severus commands"""
    
    if not command:
        # Show main help
        click.echo("Severus - Your Local-First Secret Vault\n")
        click.echo("Commands:")
        click.echo("  init                 Initialize new vault")
        click.echo("")
        click.echo("  add secret           Save password/credential")
        click.echo("  add note             Save secure note")
        click.echo("  add file <file>      Import file as note")
        click.echo("  show <name>          Display item details")
        click.echo("  delete <name>        Delete item permanently")
        click.echo("  list                 Show all items")
        click.echo("  search <term>        Find items by name")
        click.echo("  edit note <name>     Edit existing note")
        click.echo("")
        click.echo("  env save [file]      Save .env file(s)")
        click.echo("  env restore [name]   Restore .env file(s)")
        click.echo("")
        click.echo("Use 'severus help <command>' for detailed help on a specific command.")
        return
    
    # Show specific command help
    if command == "init":
        click.echo("Initialize new vault\n")
        click.echo("Usage:")
        click.echo("  severus init\n")
        click.echo("Sets up a new encrypted vault with TOTP authentication.")
        click.echo("You'll need an authenticator app to scan the QR code.")
    
    elif command == "add":
        click.echo("Add items to vault\n")
        click.echo("Commands:")
        click.echo("  severus add secret     Add a password/credential")
        click.echo("  severus add note       Add a secure note")
        click.echo("  severus add file <file> Import file as note")
    
    elif command in ["add secret", "secret"]:
        click.echo("Add a new secret to your vault\n")
        click.echo("Usage:")
        click.echo("  severus add secret\n")
        click.echo("Interactive mode - you'll be prompted for:")
        click.echo("  • Name (e.g. 'stripe-account')")
        click.echo("  • URL (optional)")
        click.echo("  • Username (optional)")
        click.echo("  • Password (required)")
        click.echo("  • Project (optional)")
    
    elif command in ["add note", "note"]:
        click.echo("Add a new note to your vault\n")
        click.echo("Usage:")
        click.echo("  severus add note\n")
        click.echo("Interactive mode - opens your default editor for note content.")
    
    elif command in ["add file", "file"]:
        click.echo("Import file as note\n")
        click.echo("Usage:")
        click.echo("  severus add file <filename>\n")
        click.echo("Examples:")
        click.echo("  severus add file passwords.txt")
        click.echo("  severus add file config/config.json")
    
    elif command == "show":
        click.echo("Display item details\n")
        click.echo("Usage:")
        click.echo("  severus show <name>\n")
        click.echo("Examples:")
        click.echo("  severus show stripe-api-key")
        click.echo("  severus show server-notes")
    
    elif command == "delete":
        click.echo("Delete item permanently\n")
        click.echo("Usage:")
        click.echo("  severus delete <name>\n")
        click.echo("Examples:")
        click.echo("  severus delete stripe-api-key")
        click.echo("  severus delete old-notes")
    
    elif command == "list":
        click.echo("Show all items in vault\n")
        click.echo("Usage:")
        click.echo("  severus list\n")
        click.echo("Displays all secrets, notes, and environment files.")
    
    elif command == "search":
        click.echo("Find items by name\n")
        click.echo("Usage:")
        click.echo("  severus search <term>\n")
        click.echo("Examples:")
        click.echo("  severus search stripe")
        click.echo("  severus search api")
    
    elif command == "edit":
        click.echo("Edit existing note\n")
        click.echo("Usage:")
        click.echo("  severus edit note <name>\n")
        click.echo("Examples:")
        click.echo("  severus edit note server-instructions")
    
    elif command == "env":
        click.echo("Manage environment variables\n")
        click.echo("Commands:")
        click.echo("  severus env save [file]    Save .env file(s) to vault")
        click.echo("  severus env restore [name] Restore .env file(s)")
        click.echo("")
        click.echo("Examples:")
        click.echo("  severus env save           # Save all .env* files")
        click.echo("  severus env save .env.local # Save specific file")
        click.echo("  severus env restore        # Restore all for current project")
        click.echo("  severus env restore env-local # Restore specific env")
    
    else:
        click.echo(f"Unknown command: {command}")
        click.echo("Run 'severus help' to see all available commands.")