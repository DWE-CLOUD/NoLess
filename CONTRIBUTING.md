# Contributing to NoLess

Thank you for your interest in contributing to NoLess! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- Example use cases

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/noless.git
cd noless

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing

Before submitting a PR:
- Test your changes manually
- Ensure existing functionality still works
- Add tests for new features if possible

## Areas for Contribution

We welcome contributions in these areas:
- Additional dataset sources
- More model templates
- Framework support (JAX, MXNet, etc.)
- Data preprocessing utilities
- Visualization tools
- Documentation improvements
- Bug fixes

## Questions?

Feel free to open an issue for any questions about contributing!
