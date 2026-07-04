![cpf-val for Python](https://br-utils.vercel.app/img/cover_cpf-val.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-val)](https://pypi.org/project/cpf-val)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-val)](https://pypi.org/project/cpf-val)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-val)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-val/README.pt.md)

A Python utility to validate CPF (Brazilian Individual's Taxpayer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Fixed 11-digit CPF**: Validates the standard 11-digit Brazilian CPF via the official modulo-11 algorithm
- ✅ **Flexible input**: Accepts `str` or a sequence of `str`; sequence elements are concatenated in order
- ✅ **Format agnostic**: Strips every non-digit character before validation
- ✅ **Repeated-digit rejection**: All-identical-digit CPFs (e.g. `111.111.111-11`, `00000000000`) are rejected
- ✅ **Typed input validation**: Dedicated `TypeError` subclass for invalid input type
- ✅ **Minimal dependencies**: [`cpf-dv`](https://pypi.org/project/cpf-dv/) for check-digit calculation and [`lacus.utils`](https://pypi.org/project/lacus.utils/) for type descriptions in error messages
- ✅ **Dual API style**: Object-oriented (`CpfValidator`) and functional (`cpf_val()`)

## Installation

```bash
$ pip install cpf-val
```

## Import

```python
from cpf_val import CpfValidator, cpf_val
```

## Quick start

```python
from cpf_val import CpfValidator

validator = CpfValidator()

validator.is_valid('12345678909')       # True
validator.is_valid('123.456.789-09')    # True
validator.is_valid('12345678910')       # False (invalid check digits)
validator.is_valid('00000000000')       # False (repeated digits)
```

Functional helper:

```python
from cpf_val import cpf_val

cpf_val('12345678909')      # True
cpf_val('123.456.789-09')   # True
cpf_val('12345678910')      # False
```

## Usage

The main entry points are the class `CpfValidator` and the helper `cpf_val()`.

### `CpfValidator`

- **`__init__`**: Takes no arguments. CPF validation has no configuration options.
- **`is_valid(cpf_input)`**: Validates a CPF value.

  Input is normalized to a string (sequences of strings are concatenated). Every non-digit character is then stripped. If the sanitized length is not exactly **11**, its base is an all-identical-digit sequence, or the check digits do not match (`CpfCheckDigits` from **`cpf-dv`**), the method returns `False` — no exception is thrown for validation failure.

  If the input is not a `str` or a sequence of `str`, **`CpfValidatorInputTypeError`** is raised.

```python
from cpf_val import CpfValidator

validator = CpfValidator()

validator.is_valid('123.456.789-09')             # True
validator.is_valid('12345678909')                # True
validator.is_valid(['123', '456', '789', '09'])  # True
validator.is_valid('12345678910')                # False (invalid check digits)
validator.is_valid('11111111111')                # False (repeated digits)
```

### Functional helper

`cpf_val()` builds a new `CpfValidator` and calls `is_valid(cpf_input)` once. It takes only the input value:

```python
from cpf_val import cpf_val

cpf_val('11144477735')      # True
cpf_val('111.444.777-35')   # True
cpf_val('11144477736')      # False
```

### Input formats

**String:** Plain digits or a formatted CPF (e.g. `123.456.789-09`, `499.784.420-90`, `011_258_960_00`). Non-digit characters are stripped before validation; the result must be exactly 11 digits.

**Sequence of strings:** Each element must be a `str`; values are concatenated (e.g. per digit, grouped segments, or mixed with punctuation). Non-string elements raise **`CpfValidatorInputTypeError`**.

```python
from cpf_val import cpf_val

cpf_val(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '9'])  # True
cpf_val(['123.456', '789-09'])  # True
```

### Errors & exceptions

This package uses **TypeError** for invalid input types. Validation failures (wrong length, ineligible base such as repeated digits, invalid check digits) return `False` and do not throw.

- **Wrong input type** (not `str` or a sequence of `str`): **`CpfValidatorInputTypeError`** — extends **`CpfValidatorTypeError`** (extends built-in `TypeError`).
- **`CpfValidatorException`**: base for non-type (business) errors; currently has no concrete subclass in this package.

```python
from cpf_val import (
    CpfValidatorInputTypeError,
    CpfValidatorTypeError,
    cpf_val,
)

# Input type (e.g. integer not allowed)
try:
    cpf_val(12345678909)
except CpfValidatorInputTypeError as e:
    print(e)  # CPF input must be of type string or string[]. Got integer number.

# Any type error from the package
try:
    cpf_val(None)
except CpfValidatorTypeError as e:
    pass  # handle
```

## API

### Exports

All public symbols are available from the `cpf_val` package:

- **`cpf_val`**: `(cpf_input: CpfInput) -> bool` — convenience helper.
- **`CpfValidator`**: Class to validate CPF (no options); accepts `CpfInput` in `is_valid()`.
- **`CPF_LENGTH`**: `11` (constant).
- **`CpfInput`**: Type alias — `str | Sequence[str]`.
- **Exceptions**: `CpfValidatorTypeError`, `CpfValidatorInputTypeError`, `CpfValidatorException`.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-val/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
