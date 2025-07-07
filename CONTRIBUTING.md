# Contributing to Entity Janitor

We welcome contributions to the Entity Janitor integration! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a new branch** for your feature or bugfix
4. **Make your changes**
5. **Test thoroughly**
6. **Submit a pull request**

## 🔧 Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant development environment
- Git

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/entity-janitor.git
   cd entity-janitor
   ```

2. Set up a Home Assistant development environment
3. Copy the `entity_janitor` folder to your `custom_components` directory
4. Restart Home Assistant

## 🧪 Testing

### Before Submitting

- Test with different Home Assistant versions
- Verify all safety features work correctly
- Test with various entity registry sizes
- Ensure proper error handling
- Check logging output

### Test Cases

- **Orphan Detection**: Verify accurate orphan identification
- **Backup System**: Test backup creation and restoration
- **Filtering**: Test domain and entity exclusions
- **Safety**: Verify dry-run mode prevents deletions
- **Age Filtering**: Test minimum age requirements
- **Configuration**: Test all configuration options

## 📝 Code Style

### Python Code

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Include docstrings for all functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
async def async_scan_for_orphans(self) -> List[Dict[str, Any]]:
    """Scan for orphaned entities in the registry.
    
    Returns:
        List of dictionaries containing orphaned entity information.
    """
    pass
```

## 🐛 Bug Reports

When reporting bugs, please include:

- Home Assistant version
- Entity Janitor version
- Detailed steps to reproduce
- Expected vs actual behavior
- Relevant log entries
- System information (OS, Python version)

## ✨ Feature Requests

When requesting features, please include:

- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Backward compatibility considerations

## 📋 Pull Request Process

1. **Create a descriptive branch name**:
   ```bash
   git checkout -b feature/add-entity-filtering
   git checkout -b bugfix/fix-backup-creation
   ```

2. **Make focused commits**:
   - Each commit should have a single purpose
   - Use clear, descriptive commit messages
   - Reference issues when applicable

3. **Update documentation**:
   - Update README if needed
   - Add changelog entry
   - Update service descriptions

4. **Test thoroughly**:
   - Test on multiple Home Assistant versions
   - Verify backward compatibility
   - Test edge cases

5. **Submit pull request**:
   - Use descriptive title and description
   - Reference related issues
   - Include testing details

## 📚 Documentation

### Required Documentation

- Code comments for complex logic
- Docstrings for all public methods
- README updates for new features
- Service documentation updates
- Example configurations

### Documentation Style

- Use clear, concise language
- Include examples where helpful
- Follow existing formatting patterns
- Update changelog for all changes

## 🔒 Security

### Security Considerations

- Entity Janitor has significant permissions
- Always validate user input
- Use safe defaults
- Implement proper error handling
- Protect against accidental mass deletions

### Reporting Security Issues

Please report security vulnerabilities privately through GitHub's security advisory system.

## 🏷️ Release Process

1. **Update version numbers** in manifest.json
2. **Update changelog** with all changes
3. **Create release notes**
4. **Tag the release** following semantic versioning
5. **Publish to GitHub**

## 💬 Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions and reviews

## 🙏 Recognition

All contributors will be recognized in the project documentation and release notes.

## 📄 License

By contributing to Entity Janitor, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

If you have questions about contributing, please:
1. Check existing issues and discussions
2. Create a new discussion on GitHub
3. Tag maintainers if needed

Thank you for contributing to Entity Janitor! 🎉
