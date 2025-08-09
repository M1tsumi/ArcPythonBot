# Contributing to Avatar Realms Collide Discord Bot

Thank you for your interest in contributing to the Avatar Realms Collide Discord Bot! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome contributions in the following areas:

- **Bug Reports**: Report bugs or issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with code changes
- **Documentation**: Improve or add documentation
- **Character Data**: Add or update character information
- **UI/UX Improvements**: Enhance the user interface and experience

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Mitsum1/ArcPythonBot.git
   cd ArcPythonBot
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Test your changes thoroughly
   - Update documentation if needed

4. **Commit Your Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Coding Standards

### Python Code Style

- **PEP 8**: Follow Python PEP 8 style guidelines
- **Black**: Use Black for code formatting
- **Type Hints**: Include type hints for function parameters and return values
- **Docstrings**: Add docstrings to all functions and classes

### Example Code Style

```python
from typing import Optional, Dict, List
import discord
from discord.ext import commands


class ExampleCog(commands.Cog):
    """Example cog demonstrating coding standards."""
    
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
    
    @commands.command(name="example")
    async def example_command(self, ctx: commands.Context) -> None:
        """Example command demonstrating proper structure.
        
        Args:
            ctx: The command context
        """
        await ctx.send("This is an example command!")
```

### File Organization

- **Cogs**: Place in `cogs/` directory
- **Utilities**: Place in `utils/` directory
- **Configuration**: Place in `config/` directory
- **Data**: Place in `data/` directory

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=./ --cov-report=html
```

### Writing Tests

- Create test files in `tests/` directory
- Name test files as `test_*.py`
- Test both success and error cases
- Mock external dependencies when possible

## 📝 Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include parameter types and descriptions
- Document return values and exceptions
- Add examples for complex functions

### User Documentation

- Update README.md for new features
- Add command examples
- Include screenshots for UI changes
- Update CHANGELOG.md for releases

## 🎯 Character Data Contributions

### Adding New Characters

1. **Update Character List**: Add to `utils/data_parser.py`
2. **Add Images**: Place talent tree images in `HeroTalentImages/`
3. **Update Documentation**: Add character to README.md

### Character Data Format

```python
{
    "name": "Character Name",
    "element": "Fire|Water|Earth|Air",
    "category": "Character Type",
    "rarity": "Common|Rare|Epic|Legendary|Mythic",
    "description": "Character description"
}
```

## 🚀 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass successfully
- [ ] Documentation is updated
- [ ] No sensitive data is included
- [ ] Changes are focused and atomic

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated
```

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Python version:
- Discord.py version:
- Operating system:

**Additional Information**
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Additional Information**
Any relevant context or examples
```

## 📞 Getting Help

- **GitHub Issues**: Create an issue for questions
- **Discord Server**: Join our community for real-time help
- **Documentation**: Check the README and code comments

## 🏆 Recognition

Contributors will be recognized in:
- **README.md**: List of contributors
- **CHANGELOG.md**: Credit for significant contributions
- **Release Notes**: Acknowledgment in releases

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Avatar Realms Collide Discord Bot! 🎮 