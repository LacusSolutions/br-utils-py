![cnpj-dv for Python](https://br-utils.vercel.app/img/cover_cnpj-dv.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-dv)](https://pypi.org/project/cnpj-dv)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-dv)](https://pypi.org/project/cnpj-dv)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-dv)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Full support for the [new alphanumeric CNPJ format](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-dv/README.pt.md)

A Python utility to calculate check digits on CNPJ (Brazilian Business Tax ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Alphanumeric CNPJ**: Full support for the new alphanumeric CNPJ format (introduced in 2026)
- ✅ **Flexible input**: Accepts `str` or `list[str]`
- ✅ **Format agnostic**: Strips non-alphanumeric characters from string input and uppercases letters
- ✅ **Auto-expansion**: Multi-character strings in lists are joined and parsed like a single string
- ✅ **Input validation**: Rejects ineligible CNPJs (all-zero base ID `00000000`, all-zero branch `0000`, or 12 numeric-only repeated digits)
- ✅ **Lazy evaluation**: Check digits are calculated only when accessed (via properties)
- ✅ **Caching**: Calculated values are cached for subsequent access
- ✅ **Type hints**: Built with Python 3.10+ type annotations
- ✅ **Minimal dependencies**: Only [`lacus.utils`](https://pypi.org/project/lacus.utils)
- ✅ **Error handling**: Specific types for type, length, and invalid CNPJ scenarios (`TypeError` vs `Exception` semantics)

## Installation

```bash
$ pip install cnpj-dv
```

## Quick Start

```python
from cnpj_dv import CnpjCheckDigits
```

Basic usage:

```python
check_digits = CnpjCheckDigits("914157320007")

check_digits.first   # '9'
check_digits.second  # '3'
check_digits.both    # '93'
check_digits.cnpj    # '91415732000793'
```

With alphanumeric CNPJ (new format):

```python
check_digits = CnpjCheckDigits("MGKGMJ9X0001")

check_digits.first   # '6'
check_digits.second  # '8'
check_digits.both    # '68'
check_digits.cnpj    # 'MGKGMJ9X000168'
```

## Usage

The main resource of this package is the class `CnpjCheckDigits`. Through an instance, you access CNPJ check-digit information:

- **`__init__`**: `CnpjCheckDigits(str | list[str])` — 12–14 alphanumeric characters after sanitization (formatting stripped from strings; letters uppercased). Only the **first 12** characters are used as the base; if you pass 13 or 14 characters (e.g. a full CNPJ including prior check digits), characters 13–14 are **ignored** and the digits are recalculated.
- **`first`**: First check digit (13th character of the full CNPJ). Lazy, cached.
- **`second`**: Second check digit (14th character of the full CNPJ). Lazy, cached.
- **`both`**: Both check digits concatenated as a string.
- **`cnpj`**: The complete CNPJ as a string of 14 characters (12 base characters + 2 check digits).

### Input formats

The `CnpjCheckDigits` class accepts multiple input formats:

**String input:** raw digits and/or letters, or formatted CNPJ (e.g. `91.415.732/0007-93`, `MG.KGM.J9X/0001-68`). Non-alphanumeric characters are removed; lowercase letters are uppercased.

**List of strings:** each element must be a string; values are concatenated and then parsed like a single string (e.g. `["9","1","4",…]`, `["9141","5732","0007"]`, `["MG","KGM","J9X","0001"]`). Non-string elements are not allowed.

```python
# String — plain, formatted, or with existing check digits (only first 12 chars used)
CnpjCheckDigits("914157320007")
CnpjCheckDigits("91.415.732/0007")
CnpjCheckDigits("91415732000793")

# List of strings — single- or multi-character elements
CnpjCheckDigits(["9", "1", "4", "1", "5", "7", "3", "2", "0", "0", "0", "7"])
CnpjCheckDigits(["9141", "5732", "0007"])
CnpjCheckDigits(["MG", "KGM", "J9X", "0001"])
```

### Errors & exceptions handling

This package uses **TypeError vs Exception** semantics: *type errors* indicate incorrect API use (e.g. wrong type); *exceptions* indicate invalid or ineligible data (e.g. invalid length or business rules). You can catch specific classes or use the base classes.

- **CnpjCheckDigitsTypeError** — base class for type errors; extends Python's `TypeError`
- **CnpjCheckDigitsInputTypeError** — input is not `str` or `list[str]` (or list contains a non-string element)
- **CnpjCheckDigitsException** — base class for data/flow exceptions; extends `Exception`
- **CnpjCheckDigitsInputLengthException** — sanitized length is not 12–14
- **CnpjCheckDigitsInputInvalidException** — base ID `00000000`, branch ID `0000`, or 12 identical numeric digits (repeated-digit pattern)

```python
from cnpj_dv import (
    CnpjCheckDigits,
    CnpjCheckDigitsException,
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
)

# Input type (e.g. integer not allowed)
try:
    CnpjCheckDigits(12345678000100)
except CnpjCheckDigitsInputTypeError as e:
    print(e)  # CNPJ input must be of type string or string[]. Got integer number.

# Length (must be 12–14 alphanumeric characters after sanitization)
try:
    CnpjCheckDigits("12345678901")
except CnpjCheckDigitsInputLengthException as e:
    print(e)  # CNPJ input "12345678901" does not contain 12 to 14 digits. Got 11.

# Invalid (e.g. all-zero base or branch, or repeated numeric digits)
try:
    CnpjCheckDigits("000000000001")
except CnpjCheckDigitsInputInvalidException as e:
    print(e)  # CNPJ input "000000000001" is invalid. Base ID "00000000" is not eligible.

# Any data exception from the package
try:
    CnpjCheckDigits("000000000001")
except CnpjCheckDigitsException as e:
    print(e)
```

### Other available resources

Import from `cnpj_dv`:

- **`CNPJ_MIN_LENGTH`**: `12`
- **`CNPJ_MAX_LENGTH`**: `14`
- **Exceptions**: see above

## Calculation algorithm

The package computes check digits with the official Brazilian modulo-11 rules extended to alphanumeric characters:

1. **Character value:** each character contributes `ord(character) − 48` (so `0`–`9` stay 0–9; letters use their ASCII offset from `0`).
2. **Weights:** from **right to left**, multiply by weights that cycle **2, 3, 4, 5, 6, 7, 8, 9**, then repeat from 2.
3. **First check digit (13th position):** apply steps 1–2 to the first **12** base characters; let `r = sum % 11`. The digit is `0` if `r < 2`, otherwise `11 − r`.
4. **Second check digit (14th position):** apply steps 1–2 to the first 12 characters **plus** the first check digit; same formula for `r`.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-dv/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
