# Severus CLI

**Local-First Encrypted Vault for Developers**

Severus is a command-line secret manager built specifically for developers and crypto teams. Store API keys, credentials, environment variables, and sensitive notes in an encrypted vault with TOTP authentication—no master passwords required.

📄 [Read the Whitepaper](https://drive.google.com/file/d/1BUPaHn7NnX5LxD0aYrXh3qjDAmFGNkqR/view?usp=sharing)

## Installation

```bash
pip install severus-vault
```

## Quick Start

### 1. Initialize Your Vault

```bash
severus init
```

This will:

- Create an encrypted vault at `~/.severus/vault.db`
- Generate a QR code for your authenticator app
- Set up TOTP authentication

### 2. Add Your First Secret

```bash
severus add secret
```

Follow the interactive prompts to store credentials with optional metadata like URLs, usernames, and project context.

### 3. Save Environment Files

```bash
# Save all .env files in current project
severus env save

# Restore them later
severus env restore
```

### 4. Search and Retrieve

```bash
# List all items
severus list

# Search for specific items
severus search stripe

# Show detailed information
severus show api-key
```

## Core Commands

### Vault Management

- `severus init` - Initialize new vault with TOTP authentication
- `severus help [command]` - Show help for specific commands

### Adding Items

- `severus add secret` - Store password/credential interactively
- `severus add note` - Create encrypted note (opens editor)
- `severus add file <filename>` - Import file as encrypted note

### Retrieving Items

- `severus list` - Show all vault items
- `severus search <term>` - Find items by name
- `severus show <name>` - Display item details

### Environment Management

- `severus env save [filename]` - Save .env files to vault
- `severus env restore [name]` - Restore environment files

### Editing and Cleanup

- `severus edit note <name>` - Edit existing note
- `severus delete <name>` - Delete item (with confirmation)

### Secure Sharing

- `severus share <name>` - Generate temporary share code
- `severus receive <code>` - Receive shared item

## Example Workflows

### Managing Passwords

```bash
# Store Stripe credentials
severus add secret
# Name: stripe-api
# URL: https://dashboard.stripe.com
# Username: admin@company.com
# Password: MikeTell_...
# Project: ecommerce-backend

# Retrieve later
severus show stripe-api
```

### Environment File Workflow

```bash
# In your project directory
cd /projects/myapp

# Save all environment files
severus env save
# Automatically saves as: myapp-env, myapp-env-local, etc.

# On another machine or fresh clone
cd /projects/myapp
severus env restore
# Restores all .env files for the project
```

### Team Collaboration

```bash
# Share a secret temporarily
severus share database-password
# Output: Share code: 7X9K-M4P2-B8Q1 (expires in 10 minutes)

# Teammate receives it
severus receive 7X9K-M4P2-B8Q1
# Secret added to their vault
```

### Note Management

```bash
# Store deployment instructions
severus add note
# Name: production-deploy
# Opens editor for content

# Store API keys and tokens securely
severus add note
# Name: aws-api-keys
# Content: Store API keys, webhook URLs, tokens, etc.

# Import existing documentation
severus add file backup-procedures.txt

# Import configuration files with sensitive data
severus add file config/api-keys.json

# Edit existing notes
severus edit note production-deploy

# View stored API keys
severus show aws-api-keys
```

## Security Model

### Authentication

- **TOTP-based**: Uses your existing authenticator app (Google Authenticator, Authy, etc.)
- **No master passwords**: Eliminates password reuse and memory vulnerabilities

### Encryption

- **Local-first**: All data encrypted locally before storage
- **Individual item encryption**: Each secret encrypted separately
- **PBKDF2 key derivation**: 100,000 iterations with SHA-256
- **Fernet encryption**: Industry-standard symmetric encryption (AES 128)

### Storage

- **SQLite metadata**: Fast searches with minimal data exposure
- **Encrypted blobs**: Sensitive data stored in separate encrypted files
- **No cloud dependencies**: Works entirely offline except for sharing

## File Locations

- **Vault database**: `~/.severus/vault.db`
- **Configuration**: `~/.severus/config.json`
- **Encrypted data**: `~/.severus/blobs/`

## Sharing Server

The sharing functionality requires a relay server. You can:

1. **Use the public server** (when available)
2. **Run your own server** (see relay-server documentation)

Shared data is:

- Encrypted client-side before upload
- Stored temporarily (10 minutes default)
- Accessible only with the share code
- Automatically deleted after expiration

## Development Setup

```bash
# Clone repository
git clone https://github.com/severus-labs/severus.git
cd severus

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and create virtual environment
poetry install

# Activate the virtual environment
poetry shell

# Run severus in development mode
poetry run severus --help

# Run tests (when you add them)
poetry run pytest

# Add new dependencies
poetry add package-name

# Add development dependencies
poetry add --group dev package-name
```

## Troubleshooting

### Vault Not Initialized

```
Error: Vault not initialized. Run 'severus init' first.
```

Run `severus init` to set up your vault and TOTP authentication.

### Invalid TOTP Code

```
Error: Invalid TOTP code.
```

Ensure your device time is synchronized and try a fresh code from your authenticator app.

### Item Not Found

```
Error: 'item-name' not found.
```

Use `severus list` to see all items or `severus search <term>` to find similar names.

### Environment Restore Failed

```
Error: No .env file found for current project
```

Use `severus env save` first, or specify the environment name: `severus env restore myapp-env`

## Security Considerations

### Best Practices

- Keep your authenticator app backed up
- Regularly update Severus to get security fixes
- Use project contexts to organize secrets
- Don't share your `~/.severus/` directory

### Limitations

- TOTP device loss requires vault recreation
- Sharing requires internet connectivity
- No automatic sync between devices (by design)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: [GitHub](https://github.com/severus-labs/severus)
- Issues: [GitHub Issues](https://github.com/severus-labs/severus/issues)
- Security: ekomobongarchibong24@gmail.com

---
