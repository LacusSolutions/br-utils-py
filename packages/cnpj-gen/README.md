![cnpj-gen for Python](https://br-utils.vercel.app/img/cover_cnpj-gen.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-gen)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Full support for the [new alphanumeric CNPJ format](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Acessar documentação em português](./README.pt.md)

A Python utility to generate valid CNPJ (Brazilian Business Tax ID) values.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Alphanumeric CNPJ**: Generates 14-character CNPJ with optional numeric, alphabetic, or alphanumeric (default) character sets
- ✅ **Optional prefix**: Provide 0–12 alphanumeric characters to fix the start of the CNPJ (e.g. base ID) and generate the rest with valid check digits
- ✅ **Formatting**: Option to return the standard formatted string (`00.000.000/0000-00`)
- ✅ **Reusable generator**: `CnpjGenerator` class with default options and per-call overrides
- ✅ **Type hints**: Built for Python 3.10+ with full type annotations
- ✅ **Minimal dependencies**: Only internal packages `lacus.utils` and `cnpj-dv` for random sequence generation and check-digit calculation
- ✅ **Error handling**: Specific type errors and exceptions for invalid options

## Installation

```bash
$ pip install cnpj-gen
```

## Quick Start

```python
from cnpj_gen import cnpj_gen
```

Basic usage:

```python
cnpj_gen()                    # e.g. 'AB123CDE000155' (14-char alphanumeric)

cnpj_gen(format=True)         # e.g. 'AB.123.CDE/0001-55'

cnpj_gen(prefix='45623767')   # e.g. '45623767ABCD96'
cnpj_gen(                     # e.g. '45.623.767/ABCD-96'
    prefix='456237670002',
    format=True,
)

cnpj_gen(type='numeric')      # e.g. '65453043000178' (digits only)
cnpj_gen(type='alphabetic')   # e.g. 'ABCDEFGHIJKL80' (letters only, except check digits)
```

Options can also be passed as a mapping:

```python
cnpj_gen({'format': True, 'type': 'numeric'})
```

## Usage

### Generator options

All options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | When `True`, return the generated CNPJ in standard format (`00.000.000/0000-00`). Non-boolean values are coerced with `bool()`. |
| `prefix` | `str` | `''` | Partial start string (0–12 alphanumeric chars). Only alphanumeric characters are kept and uppercased; missing characters are generated randomly and check digits are computed. |
| `type` | `'numeric'` \| `'alphabetic'` \| `'alphanumeric'` | `'alphanumeric'` | Character set for the randomly generated part (`prefix` is kept as-is after sanitization). **Check digits are always numeric.** |

Prefix rules: base ID (first 8 chars) and branch ID (chars 9–12) cannot be all zeros; 12 repeated digits (e.g. `777777777777`) are also not allowed.

### `cnpj_gen` (helper function)

Generates a valid CNPJ string. With no options, returns a 14-character alphanumeric CNPJ. This is a convenience wrapper around `CnpjGenerator(options, ...).generate()`.

- **`options`** (optional): `CnpjGeneratorOptionsInput` — a `CnpjGeneratorOptions` instance, a partial mapping, or `None`. See [Generator options](#generator-options).
- **`format`**, **`prefix`**, **`type`** (keyword-only): Per-option overrides when `options` is omitted or to layer on top of a mapping.

### `CnpjGenerator` (class)

For reusable defaults or per-call overrides, use the class:

```python
from cnpj_gen import CnpjGenerator

generator = CnpjGenerator(type='numeric', format=True)

generator.generate()                    # e.g. '73.008.535/0005-06'
generator.generate(prefix='12345678')   # override for this call only
generator.options                       # current default options (CnpjGeneratorOptions)
```

- **`__init__(options=None, *, format=None, prefix=None, type=None)`**: Optional default options (plain mapping, `CnpjGeneratorOptions` instance, or keyword arguments).
- **`generate(options=None, *, format=None, prefix=None, type=None)`**: Returns a valid CNPJ; per-call options override instance defaults for that call only.
- **`options`**: Property returning the default options used when per-call options are not provided (same instance as used internally; mutating it affects future `generate` calls).

Default options on the instance; per-call overrides:

```python
generator = CnpjGenerator(format=True)

generator.generate()              # formatted CNPJ
generator.generate(format=False)  # this call only: unformatted
generator.generate()              # formatted again (instance defaults preserved)
```

### `CnpjGeneratorOptions` (class)

Holds options (`format`, `prefix`, `type`) with validation and merge support:

```python
from cnpj_gen import CnpjGeneratorOptions

options = CnpjGeneratorOptions(
    prefix='AB123XYZ',
    type='numeric',
    format=True,
)
options.prefix   # 'AB123XYZ'
options.type     # 'numeric'
options.format   # True
options.set({'format': False})  # merge and return self
options.all      # immutable shallow snapshot of current options
```

- **`__init__(default_options=None, *overrides, format=None, prefix=None, type=None)`**: Options merged in order (later overrides win).
- **`format`**, **`prefix`**, **`type`**: Properties with setters; `prefix` is validated (base/branch ineligible, repeated digits).
- **`set(options)`**: Update multiple options at once; omitted fields keep their current value; returns `self`.
- **`all`**: Read-only snapshot of current options (`MappingProxyType`).
- **`DEFAULT_FORMAT`**, **`DEFAULT_PREFIX`**, **`DEFAULT_TYPE`**: Class-level default constants.

## API

### Exports

- **`cnpj_gen`**: `(options=None, *, format=None, prefix=None, type=None) -> str`
- **`CnpjGenerator`**: Class to generate CNPJ with optional default options and per-call overrides.
- **`CnpjGeneratorOptions`**: Class holding options (`format`, `prefix`, `type`) with validation and merge.
- **`CNPJ_LENGTH`**: `14` (constant).
- **`CNPJ_PREFIX_MAX_LENGTH`**: `12` (constant).
- **Types**: `CnpjType`, `CnpjGeneratorOptionsInput`, `CnpjGeneratorOptionsType`.
- **Exceptions**: `CnpjGeneratorTypeError`, `CnpjGeneratorOptionsTypeError`, `CnpjGeneratorException`, `CnpjGeneratorOptionPrefixInvalidException`, `CnpjGeneratorOptionTypeInvalidException`.

### Errors & Exceptions

This package uses **TypeError** subclasses for invalid option types and **Exception** subclasses for invalid option values (`prefix` or `type`). You can catch specific classes or the base types.

- **CnpjGeneratorTypeError** (_abstract_) — base for option type errors
- **CnpjGeneratorOptionsTypeError** — an option has the wrong type (e.g. `prefix` not a string)
- **CnpjGeneratorException** (_abstract_) — base for option value exceptions
- **CnpjGeneratorOptionPrefixInvalidException** — prefix invalid (e.g. all-zero base/branch, repeated digits)
- **CnpjGeneratorOptionTypeInvalidException** — `type` is not one of `'numeric'`, `'alphabetic'`, `'alphanumeric'`

```python
from cnpj_gen import (
    cnpj_gen,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjGeneratorException,
)

# Option type (e.g. `prefix` must be string)
try:
    cnpj_gen(prefix=123)
except CnpjGeneratorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Invalid prefix (e.g. all-zero base)
try:
    cnpj_gen(prefix='000000000001')
except CnpjGeneratorOptionPrefixInvalidException as e:
    print(e.reason, e.actual_input)

# Invalid type value
try:
    cnpj_gen(type='invalid')
except CnpjGeneratorOptionTypeInvalidException as e:
    print(e.expected_values, e.actual_input)

# Any exception from the package
try:
    cnpj_gen(prefix='000000000000')
except CnpjGeneratorException as e:
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
