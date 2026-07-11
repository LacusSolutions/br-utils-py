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
- [Changelog](#changelog)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

Please be respectful, inclusive, and constructive in all interactions.

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

- **Python** 3.10 through 3.14 (CI tests all supported versions)
- **pip** (latest version) — for package management
- **Git** — for version control

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/br-utils-py.git
cd br-utils-py/python

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development tools and all monorepo packages (editable, from source)
python require

# Or install only what a single package needs
python require cnpj-gen

# Install pre-commit hooks
python run hooks install

# Verify setup
python run lint
python run test
```

### Available Scripts

```bash
# Development
python require               # Install dev tools and all monorepo packages (editable)
python require [pkg]         # Install dev tools and a package dependency closure
python require --dev-only    # Install development tools only
python run lint              # Run linting and formatting for all packages
python run lint [pkg|path]   # Run linting and formatting for package, path, or file
python run test              # Run tests for all packages
python run test [pkg]        # Run tests for specified package
python run test -q [pkg]     # Run tests quietly
python run test -v [pkg]     # Run tests verbosely
python run test -w [pkg]     # Run tests in watch mode
python run build             # Build all packages
python run build [pkg]       # Build specified package
python run build -i [pkg]    # Build and install specified package locally
python run build -v [pkg]    # Build with an explicit version (e.g. 2.0.1)
python run clean             # Remove build files for all packages
python run clean [pkg]       # Remove build files for specified package

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

### Pre-commit Hooks

Installing hooks with `python run hooks install` enables three hook stages:

| Hook | Stage | What it does |
| --- | --- | --- |
| File checks + `lint` | pre-commit | YAML/TOML/JSON validation, trailing whitespace, and `python run lint` |
| `sync-license` | pre-commit | Propagates root `LICENSE` changes to all packages |
| `conventional-pre-commit` | commit-msg | Validates conventional commit message format and scope |
| `test-all` | pre-push | Runs `python run test` before pushing to remote |

## Project Structure

```
br-utils-py/python/
├── packages/               # Monorepo packages
│   ├── br-utilities/       # Top-level BR utilities (PyPI: br-utilities)
│   │   ├── src/            # Source code (namespace: br_utils)
│   │   ├── tests/          # Behavioral specs (*.spec.py)
│   │   ├── pyproject.toml  # Package configuration
│   │   ├── CHANGELOG.md    # Per-package release notes
│   │   ├── run             # Package-specific run script
│   │   └── README.md       # Package documentation
│   ├── cnpj-dv/            # CNPJ check digit calculator
│   ├── cnpj-fmt/           # CNPJ formatter
│   ├── cnpj-gen/           # CNPJ generator
│   ├── cnpj-utils/         # CNPJ domain aggregator
│   ├── cnpj-val/           # CNPJ validator
│   ├── cpf-dv/             # CPF check digit calculator
│   ├── cpf-fmt/            # CPF formatter
│   ├── cpf-gen/            # CPF generator
│   ├── cpf-utils/          # CPF domain aggregator
│   ├── cpf-val/            # CPF validator
│   └── utils/              # Shared helpers (PyPI: lacus.utils)
├── scripts/                # Monorepo management scripts
│   ├── build.py            # Build script
│   ├── clean.py            # Clean script
│   ├── common.py           # Common utilities
│   ├── discover.py         # Package discovery and dependency sorting
│   ├── hooks.py            # Git hooks management
│   ├── lint.py             # Linting and formatting script
│   ├── publish.py          # Publishing script
│   ├── release.py          # Release notes preparation
│   ├── sync_license.py     # LICENSE propagation
│   ├── version.py          # Version management helpers
│   ├── require/            # Dependency installation (core.py, __init__.py)
│   └── test.py             # Testing script
├── .github/workflows/      # CI/CD (lint + test matrix on Python 3.10–3.14)
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── .ruff.toml              # Ruff lint and format configuration
├── requirements-dev.txt    # Development dependencies (pytest, ruff, etc.)
├── require                 # Install monorepo dependencies (editable)
├── run                     # Main monorepo run script
├── setup.cfg               # Black configuration
├── AGENTS.md               # Agent/contributor baseline rules
├── CLAUDE.md               # Pointer to AGENTS.md
├── context/                # Task-specific contributor/agent harnesses
└── README.md               # Project documentation
```

Two package folders do not match their import name: `utils` → `lacus.utils` and `br-utilities` → `br_utils`. All other folders match their import namespace (e.g. `cnpj-gen` → `cnpj_gen`).

## Contributing Guidelines

### What We're Looking For

We welcome contributions in the following areas:

- **🐛 Bug Fixes**: Fix issues and improve stability
- **✨ New Features**: Add new formatting, validation, or generation options and capabilities
- **📚 Documentation**: Improve docs, examples, and guides
- **🧪 Tests**: Add or extend behavioral specs for new or existing features
- **⚡ Performance**: Optimize validation and formatting performance
- **🔧 Tooling**: Improve testing, linting, or development tools

### What We're NOT Looking For

- Breaking changes to the public API without discussion
- Changes that reduce meaningful test coverage
- Code that doesn't follow our style guidelines
- Features that don't align with the project's goals

### Cross-language parity

The Python packages mirror the JavaScript and PHP implementations in the broader `br-utils` monorepo. When changing public API behavior, check the corresponding suites under `js/packages/` and `php/packages/` and follow the business rules documented in their `AGENTS.md` files.

Python-specific conventions (architecture, options classes, exception hierarchy, docstrings, tests, changelogs, packaging, and CI) are documented in [`AGENTS.md`](AGENTS.md) and the task-specific harnesses under [`context/`](context/). Read the relevant harness before making changes.

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
- Add behavioral specs for new functionality
- Update documentation and changelogs as needed

### 3. Test Your Changes

```bash
# Run all tests
python run test

# Run tests for a specific package
python run test cpf-fmt

# Run tests in watch mode
python run test -w cpf-gen

# Run linting
python run lint

# Run pre-commit hooks
python run hooks run
```

### 4. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/). The commit-msg hook enforces this format.

```bash
git commit -m "feat(cpf-fmt): add string field processor"
git commit -m "fix(cnpj-val): resolve validation error in digit check"
git commit -m "docs: update README with new examples"
git commit -m "test(cpf-gen): add specs for prefix option"
```

Valid scopes: `br-utils`, `cnpj-fmt`, `cnpj-dv`, `cnpj-gen`, `cnpj-val`, `cnpj-utils`, `cpf-fmt`, `cpf-dv`, `cpf-gen`, `cpf-val`, `cpf-utils`, `utils`, `internal`

Use `br-utils` (not `br-utilities`) when committing changes to the `br-utilities` package folder.

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

The pre-push hook runs the full test suite. Then create a pull request on GitHub.

## Testing

### Test Structure

- Tests live in the `tests/` directory within each package
- Test files use the `.spec.py` suffix (e.g., `cpf_generator.spec.py`)
- Specs are organized by behavior, not as a 1:1 mirror of `src/`
- [pytest](https://docs.pytest.org/) is the test runner
- [pytest-describe](https://github.com/pytest-dev/pytest-describe) provides BDD-style `describe_*` / `it_*` functions

Each package configures pytest in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
python_files = [ "*.spec.py" ]
python_functions = [ "describe_*", "it_*", "test_*" ]
```

### Writing Tests

Specs use nested `describe_*` and `it_*` functions. Module docstrings document which reference suites they cover and any dropped cases:

```python
"""Behavioral spec for ``CpfGenerator``."""

import pytest
from cpf_gen import (
    CpfGenerator,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
)


def describe_cpf_generator():
    def describe_generate():
        def it_returns_an_11_digit_string():
            cpf = CpfGenerator().generate()

            assert isinstance(cpf, str)
            assert len(cpf) == 11
            assert cpf.isdigit()

        def it_returns_a_formatted_string_when_format_is_true():
            cpf = CpfGenerator({"format": True}).generate()

            assert "." in cpf
            assert "-" in cpf

        def it_raises_when_prefix_is_invalid():
            with pytest.raises(CpfGeneratorOptionPrefixInvalidException):
                CpfGenerator({"prefix": "000000000"}).generate()
```

Use `test_*` functions only when the describe/it pattern does not fit (e.g., parametrized helpers).

### Test Requirements

- **Behavioral coverage**: Cover happy paths, boundary conditions, and error cases
- **Cross-language alignment**: Prefer extending existing reference-suite cases over inventing new ones
- **Self-documenting specs**: Use descriptive `describe_*` / `it_*` names; document dropped or Python-specific cases in the module docstring
- **Local coverage** (optional): `pytest --cov=src --cov-report=term-missing` from a package directory — coverage tooling is available but not enforced in CI

## Code Style

### Python Guidelines

- Follow **PEP 8** coding standards
- Use **type hints** for all function parameters and return types
- Use **`__slots__`** on service classes with fixed attributes (generators, formatters, domain utils)
- Use regular **classes with property setters** for options objects — not dataclasses
- Follow **PEP 257** for docstrings
- Use **snake_case** for functions and variables
- Use **`from __future__ import annotations`** in modules that benefit from forward references

### Exception hierarchy

Packages distinguish **errors** (wrong type — subclass `TypeError`) from **exceptions** (invalid value — subclass `Exception`):

- `CpfGeneratorOptionsTypeError` — option has the wrong type
- `CpfGeneratorOptionPrefixInvalidException` — prefix value is invalid

Follow this pattern when adding new failure modes.

### Code Formatting

`python run lint` runs, in order, on each file:

1. **Ruff check** (with auto-fix)
2. **Ruff format**
3. **Black** (line length: 100)

Configuration lives in `.ruff.toml` (lint rules and Ruff formatter) and `setup.cfg` (Black). Also:

- **4 spaces** for indentation (not tabs)
- **Double quotes** for strings
- **Trailing commas** in multi-line structures

Run `python run lint` before committing — the pre-commit hook does the same.

### Naming Conventions

- **Classes**: PascalCase (`CpfGenerator`)
- **Methods**: snake_case (`is_valid`)
- **Functions**: snake_case (`cpf_gen`)
- **Variables**: snake_case (`field_name`)
- **Constants**: UPPER_SNAKE_CASE (`CPF_LENGTH`)
- **Source files**: snake_case (`cpf_generator.py`)
- **Spec files**: snake_case with `.spec.py` suffix (`cpf_generator.spec.py`)

### Module Structure

- Import namespace matches the distribution (e.g., `cpf_gen`, `br_utils`)
- Source code in `src/{namespace}/`
- Specs in `tests/`
- Public API exported in `__init__.py`

### Example Code Style

```python
"""CPF generator module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cpf_generator_options import CpfGeneratorOptions

if TYPE_CHECKING:
    from .types import CpfGeneratorOptionsInput


class CpfGenerator:
    """Generator for CPF identifiers."""

    __slots__ = ("_options",)

    def __init__(
        self,
        options: CpfGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> None:
        """Create a generator with optional default options."""
        self._options = CpfGeneratorOptions(options, format=format, prefix=prefix)

    @property
    def options(self) -> CpfGeneratorOptions:
        """Return the current default options."""
        return self._options

    def generate(self, options: CpfGeneratorOptionsInput | None = None) -> str:
        """Generate a valid CPF string."""
        # Implementation
        ...
```

## Changelog

Each package under `packages/<pkg>/` owns a `CHANGELOG.md`. Update it when your change is **user-facing** (anything under `src/`, public `README.md`, or runtime dependencies in `pyproject.toml`).

Do **not** add changelog entries for dev-only changes (tests, CI, lint config, `requirements-dev.txt`, etc.).

Follow [Semantic Versioning](https://semver.org/):

- **major** — breaking API or behavior change
- **minor** — new public API or feature
- **patch** — bug fix or non-breaking improvement

See existing changelogs (e.g., `packages/cpf-gen/CHANGELOG.md`) for format and tone.

## Pull Request Process

### Before Submitting

- [ ] Code follows our style guidelines (Ruff, Black, PEP 8)
- [ ] All tests pass (`python run test`)
- [ ] Linting passes (`python run lint`)
- [ ] Pre-commit hooks pass (`python run hooks run`)
- [ ] Documentation is updated
- [ ] User-facing changes have a `CHANGELOG.md` entry in the affected package(s)
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
- [ ] New specs added
- [ ] Edge cases covered

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated (if user-facing)
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI runs lint and tests across Python 3.10, 3.11, 3.12, 3.13, and 3.14
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
- **Environment**: Python version, OS, package version
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
- Package version: [e.g. 2.0.0]

**Code example**
```python
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
- **Documentation**: Check the README, package READMEs, and inline docstrings
- **Contributor & agent guides**: [`AGENTS.md`](AGENTS.md) for baseline rules and the task-specific harnesses under [`context/`](context/)

## License

By contributing to `br-utils`, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to `br-utils`! 🎉
