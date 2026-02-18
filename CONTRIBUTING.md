# Contributing to Collaboration Area Event Series

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, WordPress version, etc.)

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test with both simple and complex configurations
   - Use dry-run mode to verify behavior
   - Test error handling

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Explain why the change is needed

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings for functions and classes
- Use meaningful variable and function names

### Documentation

- Update README.md if you add new features
- Update QUICKSTART.md for user-facing changes
- Add examples for new configuration options
- Keep documentation clear and beginner-friendly

### Testing

Before submitting a PR, test your changes:

1. **Syntax Check**
   ```bash
   python -m py_compile scripts/create_events.py
   ```

2. **Dry Run Test**
   ```bash
   python scripts/create_events.py --config examples/simple-config.json --dry-run
   ```

3. **Configuration Validation**
   - Test with missing required fields
   - Test with invalid date/time formats
   - Test with both single `event` and multi `events` config formats

## Feature Ideas

Here are some ideas for potential contributions:

### Script Enhancements
- [ ] Batch update existing events
- [ ] Delete events by criteria
- [ ] Export events from WordPress to JSON

### Configuration
- [ ] YAML configuration file support
- [ ] CSV import for bulk event creation
- [ ] Configuration templates for common use cases
- [ ] Environment variable support for credentials

### Error Handling
- [ ] Better error messages with suggestions
- [ ] Retry logic for failed requests
- [ ] Rollback mechanism for failed batch operations
- [ ] Validation warnings before creation

### Documentation
- [ ] Video tutorial
- [ ] WordPress plugin documentation
- [ ] API endpoint reference
- [ ] Troubleshooting flowchart

### Testing
- [ ] Unit tests for utility functions
- [ ] Integration tests with mock WordPress API
- [ ] Test configuration files
- [ ] CI/CD pipeline

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing documentation in the `docs/` directory
- Review closed issues for similar questions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's guidelines

Thank you for contributing!
