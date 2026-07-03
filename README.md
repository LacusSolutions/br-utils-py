![cpf-gen for Python](https://br-utils.vercel.app/img/cover_cpf-gen.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-gen)](https://pypi.org/project/cpf-gen)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-gen)](https://pypi.org/project/cpf-gen)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-gen)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🌎 [Acessar documentação em português](./README.pt.md)

A Python utility to generate valid CPF (Brazilian Individual's Taxpayer ID) values.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Optional prefix**: Provide 0–9 digits to fix the start of the CPF and generate the rest with valid check digits
- ✅ **Formatting**: Option to return the standard formatted string (`000.000.000-00`)
- ✅ **Reusable generator**: `CpfGenerator` class with default options and per-call overrides
- ✅ **Type hints**: Built for Python 3.10+ with full type annotations
- ✅ **Minimal dependencies**: Only internal packages `lacus.utils` and `cpf-dv` for random sequence generation and check-digit calculation
- ✅ **Error handling**: Specific type errors and exceptions for invalid options

## Installation

```bash
$ pip install cpf-gen
```

## Quick Start

```python
from cpf_gen import cpf_gen
```

Basic usage:

```python
cpf_gen()                    # e.g. '47844241055' (11-digit numeric)

cpf_gen(format=True)         # e.g. '005.265.352-88'

cpf_gen(prefix='528250911')  # e.g. '52825091138'
cpf_gen(                     # e.g. '528.250.911-38'
    prefix='528250911',
    format=True,
)
```

Options can also be passed as a mapping:

```python
cpf_gen({'format': True, 'prefix': '528250911'})
```

## Usage

### Generator options

All options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | When `True`, return the generated CPF in standard format (`000.000.000-00`). Non-boolean values are coerced with `bool()`. |
| `prefix` | `str` | `''` | Partial start string (0–9 digits). Only digits are kept; missing characters are generated randomly and check digits are computed. Prefixes longer than 9 digits are truncated silently. |

Prefix rules: the base (first 9 digits) cannot be all zeros; 9 repeated digits (e.g. `999999999`) are not allowed.

### `cpf_gen` (helper function)

Generates a valid CPF string. With no options, returns an 11-digit numeric CPF. This is a convenience wrapper around `CpfGenerator(options, ...).generate()`.

- **`options`** (optional): `CpfGeneratorOptionsInput` — a `CpfGeneratorOptions` instance, a partial mapping, or `None`. See [Generator options](#generator-options).
- **`format`**, **`prefix`** (keyword-only): Per-option overrides when `options` is omitted or to layer on top of a mapping.

### `CpfGenerator` (class)

For reusable defaults or per-call overrides, use the class:

```python
from cpf_gen import CpfGenerator

generator = CpfGenerator(format=True)

generator.generate()                  # e.g. '005.265.352-88'
generator.generate(prefix='123456')   # override for this call only
generator.options                   # current default options (CpfGeneratorOptions)
```

- **`__init__(options=None, *, format=None, prefix=None)`**: Optional default options (plain mapping, `CpfGeneratorOptions` instance, or keyword arguments).
- **`generate(options=None, *, format=None, prefix=None)`**: Returns a valid CPF; per-call options override instance defaults for that call only.
- **`options`**: Property returning the default options used when per-call options are not provided (same instance as used internally; mutating it affects future `generate` calls).

Default options on the instance; per-call overrides:

```python
generator = CpfGenerator(format=True)

generator.generate()              # formatted CPF
generator.generate(format=False)  # this call only: unformatted
generator.generate()              # formatted again (instance defaults preserved)
```

### `CpfGeneratorOptions` (class)

Holds options (`format`, `prefix`) with validation and merge support:

```python
from cpf_gen import CpfGeneratorOptions

options = CpfGeneratorOptions(
    prefix='123456',
    format=True,
)
options.prefix   # '123456'
options.format   # True
options.set({'format': False})  # merge and return self
options.all      # immutable shallow snapshot of current options
```

- **`__init__(default_options=None, *overrides, format=None, prefix=None)`**: Options merged in order (later overrides win).
- **`format`**, **`prefix`**: Properties with setters; `prefix` is validated (base ID ineligible, repeated digits).
- **`set(options)`**: Update multiple options at once; omitted fields keep their current value; returns `self`.
- **`all`**: Read-only snapshot of current options (`MappingProxyType`).
- **`DEFAULT_FORMAT`**, **`DEFAULT_PREFIX`**: Class-level default constants.

## API

### Exports

- **`cpf_gen`**: `(options=None, *, format=None, prefix=None) -> str`
- **`CpfGenerator`**: Class to generate CPF with optional default options and per-call overrides.
- **`CpfGeneratorOptions`**: Class holding options (`format`, `prefix`) with validation and merge.
- **`CPF_LENGTH`**: `11` (constant).
- **`CPF_PREFIX_MAX_LENGTH`**: `9` (constant).
- **Types**: `CpfGeneratorOptionsInput`, `CpfGeneratorOptionsType`.
- **Exceptions**: `CpfGeneratorTypeError`, `CpfGeneratorOptionsTypeError`, `CpfGeneratorException`, `CpfGeneratorOptionPrefixInvalidException`.

### Errors & Exceptions

This package uses **TypeError** subclasses for invalid option types and **Exception** subclasses for invalid option values (e.g. `prefix`). You can catch specific classes or the base types.

- **CpfGeneratorTypeError** (_abstract_) — base for option type errors
- **CpfGeneratorOptionsTypeError** — an option has the wrong type (e.g. `prefix` not a string)
- **CpfGeneratorException** (_abstract_) — base for option value exceptions
- **CpfGeneratorOptionPrefixInvalidException** — prefix invalid (e.g. zeroed base ID, repeated digits)

```python
from cpf_gen import (
    cpf_gen,
    CpfGeneratorOptionsTypeError,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorException,
)

# Option type (e.g. `prefix` must be string)
try:
    cpf_gen(prefix=123)
except CpfGeneratorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Invalid prefix (e.g. zeroed base ID)
try:
    cpf_gen(prefix='000000000')
except CpfGeneratorOptionPrefixInvalidException as e:
    print(e.reason, e.actual_input)

# Any exception from the package
try:
    cpf_gen(prefix='999999999')
except CpfGeneratorException as e:
    print(e)
```

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](./CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
