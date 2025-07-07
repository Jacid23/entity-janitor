# Contributing to Entity Janitor

Thank you for your interest in contributing to Entity Janitor! This document provides guidelines for contributing to the project.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Create a new branch** for your feature or bug fix
3. **Make your changes** with clear, descriptive commit messages
4. **Test thoroughly** in a development Home Assistant instance
5. **Submit a pull request** with a detailed description

## Development Setup

1. Clone your fork to your Home Assistant `custom_components` directory
2. Create a development environment with Home Assistant
3. Enable debug logging:
   ```yaml
   logger:
     logs:
       custom_components.entity_janitor: debug
   ```

## Code Standards

- Follow Python PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Include comprehensive error handling
- Test all code paths thoroughly

## Testing

- Test with various entity registry states
- Verify backup functionality works correctly
- Test dry-run mode thoroughly
- Ensure configuration UI works properly
- Test with different Home Assistant versions

## Documentation

- Update README.md for new features
- Add changelog entries for all changes
- Include usage examples where appropriate
- Update version numbers consistently

## Pull Request Process

1. Ensure all tests pass
2. Update documentation as needed
3. Add changelog entry
4. Request review from maintainers
5. Address any feedback promptly

## Bug Reports

When reporting bugs, please include:
- Home Assistant version
- Entity Janitor version
- Steps to reproduce
- Expected vs actual behavior
- Relevant log entries
- Configuration details

## Feature Requests

For new features, please:
- Describe the use case clearly
- Explain the expected behavior
- Consider backward compatibility
- Discuss potential implementation approaches

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Maintain a welcoming environment

## Questions?

If you have questions about contributing, please:
- Check existing issues and discussions
- Ask in the Home Assistant community
- Open a GitHub issue for clarification

Thank you for helping make Entity Janitor better!
