# Lacus Solutions' Utils

[![PyPI Version](https://img.shields.io/pypi/v/lacus.utils)](https://pypi.org/project/lacus.utils)
[![PyPI Downloads](https://img.shields.io/pypi/dm/lacus.utils)](https://pypi.org/project/lacus.utils)
[![Python Version](https://img.shields.io/pypi/pyversions/lacus.utils)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Reusable utilities library for Lacus Solutions' Python packages.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- **Type description**: Python-native type labels for error messages (`NoneType`, `dict`, `tuple`, built-ins, lists)
- **Random sequences**: Generate numeric, alphabetic, or alphanumeric sequences of any length
- **Zero dependencies**: No external runtime packages required

## Installation

```bash
$ pip install lacus.utils
```

## Import

```python
from lacus.utils import describe_type, generate_random_sequence, SequenceType
```

## Quick Start

```python
describe_type(None)           # 'NoneType'
describe_type("hello")        # 'string'
describe_type(42)             # 'integer number'
describe_type(3.14)           # 'float number'
describe_type(float("nan"))   # 'NaN'
describe_type({})             # 'dict'
describe_type([1, 2, 3])      # 'number[]'
describe_type([1, "a", 2])    # '(number | string)[]'
describe_type((1, 2))         # 'number tuple'

generate_random_sequence(10, "numeric")       # e.g. '9956000611'
generate_random_sequence(6, "alphabetic")   # e.g. 'AXQMZB'
generate_random_sequence(8, "alphanumeric") # e.g. '8ZFB2K09'
```

## API

All functions are implemented in [`src/lacus/utils/`](src/lacus/utils/) and covered by tests in [`tests/`](tests/).

### `describe_type(value) -> str`

Describes the type of a value for error messages.

| Input | Result |
|--------|--------|
| `None` | `'NoneType'` |
| `str` | `'string'` |
| `bool` | `'boolean'` |
| `int` | `'integer number'` |
| `float` (finite) | `'float number'` |
| `float('nan')` | `'NaN'` |
| `float('inf')` / `float('-inf')` | `'Infinity'` |
| `complex` | `'complex number'` |
| `dict` | `'dict'` |
| `set` / `frozenset` | `'set'` / `'frozenset'` |
| `bytes` / `bytearray` | `'bytes'` / `'bytearray'` |
| callable | `'function'` |
| class (`int`, `str`, …) | `'type'` |
| custom class instance | `'object'` |
| `[]` | `'Array (empty)'` |
| `[1, 2, 3]` | `'number[]'` |
| `[1, 'a', 2]` | `'(number | string)[]'` |
| `()` | `'tuple (empty)'` |
| `(1, 2)` | `'number tuple'` |

### `generate_random_sequence(size: int, sequence_type: SequenceType) -> str`

Generates a random character sequence of the given length and type.

- **`size`**: Length of the sequence (e.g. `10`).
- **`sequence_type`**: One of:
  - **`'numeric'`**: digits `0-9`
  - **`'alphabetic'`**: uppercase letters `A-Z`
  - **`'alphanumeric'`**: digits and uppercase letters `0-9A-Z`

### Exports summary

| Export | Description |
|--------|-------------|
| `describe_type` | Type description for error messages |
| `generate_random_sequence` | Random sequence generation |
| `SequenceType` | Literal type: `'alphabetic' \| 'alphanumeric' \| 'numeric'` |

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- Starring the repository
- Contributing to the codebase
- [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](./CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
