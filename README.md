![cpf-dv for Python](https://br-utils.vercel.app/img/cover_cpf-dv.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-dv)](https://pypi.org/project/cpf-dv)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-dv)](https://pypi.org/project/cpf-dv)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-dv)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-dv/README.pt.md)

A Python utility to calculate check digits on CPF (Brazilian Individual's Taxpayer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Flexible input**: Accepts `str` or `list[str]`
- ✅ **Format agnostic**: Strips non-numeric characters from string input
- ✅ **Auto-expansion**: Multi-character strings in lists are joined and parsed like a single string
- ✅ **Input validation**: Rejects ineligible CPFs (9 identical digits in the base — repeated-digit pattern)
- ✅ **Lazy evaluation**: Check digits are calculated only when accessed (via properties)
- ✅ **Caching**: Calculated values are cached for subsequent access
- ✅ **Type hints**: Built with Python 3.10+ type annotations
- ✅ **Minimal dependencies**: Only [`lacus.utils`](https://pypi.org/project/lacus.utils)
- ✅ **Error handling**: Specific types for type, length, and invalid CPF scenarios (`TypeError` vs `Exception` semantics)

## Installation

```bash
$ pip install cpf-dv
```

## Quick Start

```python
from cpf_dv import CpfCheckDigits
```

Basic usage:

```python
check_digits = CpfCheckDigits("054496519")

check_digits.first   # '1'
check_digits.second  # '0'
check_digits.both    # '10'
check_digits.cpf     # '05449651910'
```

## Usage

The main resource of this package is the class `CpfCheckDigits`. Through an instance, you access CPF check-digit information:

- **`__init__`**: `CpfCheckDigits(str | list[str])` — 9–11 digits after sanitization (formatting stripped from strings). Only the **first 9** digits are used as the base; if you pass 10 or 11 digits (e.g. a full CPF including prior check digits), digits 10–11 are **ignored** and the check digits are recalculated.
- **`first`**: First check digit (10th digit of the full CPF). Lazy, cached.
- **`second`**: Second check digit (11th digit of the full CPF). Lazy, cached.
- **`both`**: Both check digits concatenated as a string.
- **`cpf`**: The complete CPF as a string of 11 digits (9 base digits + 2 check digits).

### Input formats

The `CpfCheckDigits` class accepts multiple input formats:

**String input:** plain digits or formatted CPF (e.g. `054.496.519-10`, `123.456.789`). Non-numeric characters are removed. Leading zeros are preserved.

**List of strings:** each element must be a string; values are concatenated and then parsed like a single string (e.g. `["0","5","4",…]`, `["054","496","519"]`, `["054496519"]`). Non-string elements are not allowed.

```python
# String — plain, formatted, or with existing check digits (only first 9 digits used)
CpfCheckDigits("054496519")
CpfCheckDigits("054.496.519-10")
CpfCheckDigits("05449651910")

# List of strings — single- or multi-character elements
CpfCheckDigits(["0", "5", "4", "4", "9", "6", "5", "1", "9"])
CpfCheckDigits(["054", "496", "519"])
CpfCheckDigits(["054496519"])
```

### Errors & exceptions handling

This package uses **TypeError vs Exception** semantics: *type errors* indicate incorrect API use (e.g. wrong type); *exceptions* indicate invalid or ineligible data (e.g. invalid length or business rules). You can catch specific classes or use the base classes.

- **CpfCheckDigitsTypeError** — base class for type errors; extends Python's `TypeError`
- **CpfCheckDigitsInputTypeError** — input is not `str` or `list[str]` (or list contains a non-string element)
- **CpfCheckDigitsException** — base class for data/flow exceptions; extends `Exception`
- **CpfCheckDigitsInputLengthException** — sanitized length is not 9–11
- **CpfCheckDigitsInputInvalidException** — first 9 digits are all identical (repeated-digit pattern)

```python
from cpf_dv import (
    CpfCheckDigits,
    CpfCheckDigitsException,
    CpfCheckDigitsInputInvalidException,
    CpfCheckDigitsInputLengthException,
    CpfCheckDigitsInputTypeError,
)

# Input type (e.g. integer not allowed)
try:
    CpfCheckDigits(12345678901)
except CpfCheckDigitsInputTypeError as e:
    print(e)  # CPF input must be of type string or string[]. Got integer number.

# Length (must be 9–11 digits after sanitization)
try:
    CpfCheckDigits("12345678")
except CpfCheckDigitsInputLengthException as e:
    print(e)  # CPF input "12345678" does not contain 9 to 11 digits. Got 8.

# Invalid (e.g. repeated digits)
try:
    CpfCheckDigits(["999", "999", "999"])
except CpfCheckDigitsInputInvalidException as e:
    print(e)  # CPF input ["999","999","999"] is invalid. Repeated digits are not considered valid.

# Any data exception from the package
try:
    CpfCheckDigits(["999", "999", "999"])
except CpfCheckDigitsException as e:
    print(e)
```

### Other available resources

Import from `cpf_dv`:

- **`CPF_MIN_LENGTH`**: `9`
- **`CPF_MAX_LENGTH`**: `11`
- **`CpfInput`**: type alias (`str | list[str]`)
- **Exceptions**: see above

## Calculation algorithm

The package calculates CPF check digits using the official Brazilian modulo-11 algorithm:

1. **First check digit (10th position):** apply to the first **9** base digits; weights **10, 9, 8, 7, 6, 5, 4, 3, 2** (left to right); let `remainder = 11 - (sum(digit × weight) % 11)`. The digit is `0` if `remainder > 9`, otherwise `remainder`.
2. **Second check digit (11th position):** apply to the first 9 base digits **plus** the first check digit; weights **11, 10, 9, 8, 7, 6, 5, 4, 3, 2** (left to right); same formula for `remainder`.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-dv/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
