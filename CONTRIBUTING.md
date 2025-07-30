# Contributing to Avatar Realms Collide Bot

Thank you for your interest in contributing to the Avatar Realms Collide Discord Bot! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following the guidelines below
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Setup

1. Install Python 3.9+ and pip
2. Clone the repository: `git clone https://github.com/yourusername/ArcPythonBot.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with your Discord bot token
5. Run the bot: `python main.py`

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

## Adding New Features

### Adding New Commands

1. Create or modify a cog in the `cogs/` directory
2. Add the command with proper error handling
3. Update the help system in `cogs/utility.py`
4. Add tests if applicable

### Adding New Data

1. Update JSON files in the `data/` directory
2. Follow the existing data structure
3. Update the data parser if needed
4. Test with existing commands

### Adding New Images

1. Place images in the appropriate `images/` subdirectory
2. Use WebP format for optimal size and quality
3. Update any references to the images in the code

## Testing

- Test all new commands thoroughly
- Test error cases and edge cases
- Ensure the bot handles invalid input gracefully
- Test with different Discord permissions

## Pull Request Guidelines

1. **Clear description** of what the PR does
2. **Screenshots** if UI changes are involved
3. **Test coverage** for new functionality
4. **Documentation updates** if needed
5. **Follow the existing code style**

## Reporting Issues

When reporting issues, please include:

1. **Clear description** of the problem
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable

## Discord Community

Join our Discord server for support and discussions:
[Discord Server](https://discord.gg/a3tGyAwVRc)

## Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow Discord's Terms of Service

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to the Avatar Realms Collide Bot community! 