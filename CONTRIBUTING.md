# Contributing to Severus

Thanks for your interest in contributing to Severus! This project aims to solve real developer pain points around secret management with a local-first approach.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/severus-labs/severus.git`
3. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
4. Install dependencies: `poetry install`
5. Activate environment: `poetry shell`
6. Test your setup: `poetry run severus --help`

## What We're Looking For

- **Bug fixes**: Especially around TOTP, encryption, or environment file handling
- **Platform support**: Windows compatibility, macOS edge cases, Linux distributions
- **UX improvements**: Better error messages, command shortcuts, workflow optimizations
- **Security enhancements**: Audit encryption implementation, suggest improvements
- **Documentation**: Usage examples, troubleshooting guides, API documentation
- **Performance**: Faster vault operations, search improvements
- **New features**: Import/export, backup strategies, additional file formats

## Development Workflow

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes with clear commit messages
3. Test locally: `poetry run severus [command]`
4. Run any existing tests: `poetry run pytest` (when available)
5. Update documentation if needed
6. Submit a PR with a clear description

## Code Style

- Follow existing patterns in the codebase
- Use descriptive variable names
- Add docstrings for new functions
- Keep security-sensitive code simple and reviewable

## Security Considerations

This is a security tool, so:

- Assume code will be audited
- Prefer simple, well-tested crypto libraries
- Never log sensitive data
- Test edge cases around encryption/decryption

## Questions or Ideas?

Open an issue to discuss before starting work on major features. We'd rather align on approach before you spend time coding.

## Support the Project

- Star the repository
- Report bugs you encounter
- Share with other developers who need better secret management
- Contribute documentation improvements
