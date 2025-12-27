# Contributing to `br-utils`

Thank you for your interest in contributing to this initiative! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contributing Guidelines](#contributing-guidelines)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful, inclusive, and constructive in all interactions.

## Getting Started

Before contributing, please:

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment** (see [Development Setup](#development-setup))
4. **Create a feature branch** for your changes
5. **Make your changes** following our guidelines
6. **Test your changes** thoroughly
7. **Submit a pull request**

## Development Setup

### Prerequisites

- **Python** (v3.10 or higher)
- **pip** (latest version) - for package management
- **Git** - for version control

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/br-utils-py.git
cd br-utils-py/python

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
python run hooks install

# Verify setup
python run lint
python run test
```

### Available Scripts

```bash
# Development
python run lint              # Run linting and formatting for all packages
python run lint [pkg|path]   # Run linting and formatting for package, path, or file
python run test              # Run tests for all packages
python run test [pkg]        # Run tests for specified package
python run test -w [pkg]     # Run tests in watch mode
python run build             # Build all packages
python run build [pkg]       # Build specified package
python run build -i [pkg]    # Build and install specified package locally
python run clean             # Remove build files for all packages
python run clean [pkg]       # Remove build files for specified package
python run publish [pkg]     # Publish specified package to PyPI

# Git Hooks
python run hooks install     # Install pre-commit hooks
python run hooks uninstall   # Uninstall pre-commit hooks
python run hooks update      # Update pre-commit hooks
python run hooks run         # Run pre-commit hooks on all files

# Package-specific scripts (from within a package directory)
python run lint              # Run linting for current package
python run test              # Run tests for current package
python run build             # Build current package
python run build -i          # Build and install current package locally
python run clean             # Remove build files for current package
python run publish           # Publish current package to PyPI
```

## Project Structure

```
br-utils-py/python/
├── packages/               # Monorepo packages
│   ├── br-utilities/       # Core BR utilities (combines CPF and CNPJ)
│   │   ├── src/            # Source code
│   │   ├── tests/          # Test files
│   │   ├── pyproject.toml  # Package configuration
│   │   ├── run             # Package-specific run script
│   │   └── README.md       # Package documentation
│   ├── cnpj-cd/            # CNPJ check digit calculator package
│   │   └── ...
│   ├── cnpj-fmt/           # CNPJ formatter package
│   │   └── ...
│   ├── cnpj-gen/           # CNPJ generator package
│   │   └── ...
│   ├── cnpj-utils/         # CNPJ utilities package
│   │   └── ...
│   ├── cnpj-val/           # CNPJ validator package
│   │   └── ...
│   ├── cpf-cd/             # CPF check digit calculator package
│   │   └── ...
│   ├── cpf-fmt/            # CPF formatter package
│   │   └── ...
│   ├── cpf-gen/            # CPF generator package
│   │   └── ...
│   ├── cpf-utils/          # CPF utilities package
│   │   └── ...
│   └── cpf-val/            # CPF validator package
│       └── ...
├── scripts/                # Monorepo management scripts
│   ├── build.py            # Build script
│   ├── clean.py            # Clean script
│   ├── common.py           # Common utilities
│   ├── hooks.py            # Git hooks management
│   ├── lint.py             # Linting script
│   ├── publish.py          # Publishing script
│   └── test.py             # Testing script
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── requirements-dev.txt    # Development dependencies
├── requirements.txt        # Production dependencies
├── run                     # Main monorepo run script
├── setup.cfg               # Black configuration
└── README.md               # Project documentation
```

## Contributing Guidelines

### What We're Looking For

We welcome contributions in the following areas:

- **🐛 Bug Fixes**: Fix issues and improve stability
- **✨ New Features**: Add new document types, processors, or functionality
- **📚 Documentation**: Improve docs, examples, and guides
- **🧪 Tests**: Add test coverage for new or existing features
- **⚡ Performance**: Optimize validation and formatting performance
- **🔧 Tooling**: Improve testing, linting, or development tools

### What We're NOT Looking For

- Breaking changes to the public API without discussion
- Changes that reduce test coverage
- Code that doesn't follow our style guidelines
- Features that don't align with the project's goals

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow our coding standards
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
python run test

# Run tests for specific package
python run test cpf-fmt

# Run tests in watch mode
python run test -w cpf-gen

# Run linting
python run lint

# Run pre-commit hooks
python run hooks run
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat(cpf-fmt): add string field processor"
git commit -m "fix(cnpj-val): resolve validation error in digit check"
git commit -m "docs: update README with new examples"
git commit -m "test(cpf-gen): add tests for prefix option"
```

Valid scopes: `br-utils`, `cnpj-fmt`, `cnpj-cd`, `cnpj-gen`, `cnpj-val`, `cnpj-utils`, `cpf-fmt`, `cpf-cd`, `cpf-gen`, `cpf-val`, `cpf-utils`, `internal`

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Testing

### Test Structure

- Tests are located in the `tests/` directory within each package
- Test files use the `_test.py` suffix (e.g., `cpf_generator_test.py`)
- Tests mirror the `src/` directory structure
- Use pytest as the test runner

### Writing Tests

```python
"""Unit tests for CPF generator."""

import pytest
from cpf_gen import CpfGenerator, CpfGeneratorOptions


class CpfGeneratorTest:
    def test_should_generate_valid_cpf(self):
        generator = CpfGenerator()
        cpf = generator.generate()

        assert isinstance(cpf, str)
        assert len(cpf) == 11
        assert cpf.isdigit()

    def test_should_generate_formatted_cpf(self):
        options = CpfGeneratorOptions(format=True)
        generator = CpfGenerator(options)
        cpf = generator.generate()

        assert "." in cpf
        assert "-" in cpf

    def test_should_raise_error_for_invalid_prefix(self):
        options = CpfGeneratorOptions(prefix="invalid")

        with pytest.raises(CpfGeneratorPrefixNotValidError):
            CpfGenerator(options).generate()
```

### Test Requirements

- **Coverage**: Maintain 100% line coverage
- **Edge Cases**: Test boundary conditions and error cases
- **Performance**: Consider performance implications
- **Documentation**: Tests should be self-documenting

## Code Style

### Python Guidelines

- Follow **PEP 8** coding standards
- Use **type hints** for all function parameters and return types
- Use **dataclasses** for data containers when appropriate
- Use **`__slots__`** for classes with fixed attributes
- Follow **PEP 257** for docstrings
- Use **snake_case** for functions and variables

### Code Formatting

- Use **Black** for code formatting (line length: 100)
- Use **Ruff** for linting
- Use **4 spaces** for indentation (not tabs)
- Use **double quotes** for strings (Black default)
- Use **trailing commas** in multi-line structures

### Naming Conventions

- **Classes**: PascalCase (`CpfGenerator`)
- **Methods**: snake_case (`generate_cpf`)
- **Functions**: snake_case (`cpf_gen`)
- **Variables**: snake_case (`field_name`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Files**: snake_case (`cpf_generator.py`)
- **Test files**: snake_case with `_test` suffix (`cpf_generator_test.py`)

### Module Structure

- Root namespace: Package name (e.g., `cpf_gen`)
- Source code in `src/{package_name}/`
- Tests in `tests/`
- Public API exported in `__init__.py`

### Example Code Style

```python
"""CPF generator module."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CpfGeneratorOptions:
    """Options for CPF generation."""

    format: bool = False
    prefix: str | None = None


class CpfGenerator:
    """Generator for valid CPF numbers."""

    __slots__ = ("_options",)

    def __init__(self, options: CpfGeneratorOptions | None = None) -> None:
        """Initialize the generator with optional configuration.

        Args:
            options: Configuration options for generation.
        """
        self._options = options or CpfGeneratorOptions()

    @property
    def options(self) -> CpfGeneratorOptions:
        """Get the current generator options."""
        return self._options

    def generate(self) -> str:
        """Generate a valid CPF number.

        Returns:
            A valid CPF string, optionally formatted.
        """
        # Implementation
        return self._generate_digits()

    def _generate_digits(self) -> str:
        """Generate the CPF digits.

        Returns:
            The raw CPF digits.
        """
        # Private implementation
        pass
```

## Pull Request Process

### Before Submitting

- [ ] Code follows our style guidelines (PEP 8, Black, Ruff)
- [ ] All tests pass (`python run test`)
- [ ] Linting passes (`python run lint`)
- [ ] Pre-commit hooks pass (`python run hooks run`)
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] New tests added
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI will run tests, linting, and type checking
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Minimal steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, etc.
- **Code Example**: Minimal code that demonstrates the issue

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Import module with...
2. Call function with...
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- Python version: [e.g. 3.12.0]
- OS: [e.g. Ubuntu 22.04]
- Package version: [e.g. 1.1.2]

**Code example**
```python
# Minimal code that reproduces the issue
from cpf_gen import cpf_gen

result = cpf_gen(prefix="invalid")
```

**Additional context**
Any other context about the problem.
```

## Feature Requests

### Suggesting Features

When suggesting features, please include:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other ways to solve the problem
- **Additional Context**: Any other relevant information

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the README and inline code comments

## Recognition

Contributors will be recognized in:
- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor statistics

## License

By contributing to `br-utils`, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to `br-utils`! 🎉
