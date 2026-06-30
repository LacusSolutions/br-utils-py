![cnpj-val for Python](https://br-utils.vercel.app/img/cover_cnpj-val.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-val)](https://pypi.org/project/cnpj-val)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-val)](https://pypi.org/project/cnpj-val)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-val)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Full support for the [new alphanumeric CNPJ format](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-val/README.pt.md)

A Python utility to validate CNPJ (Brazilian Business Tax ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Alphanumeric CNPJ**: Validates 14-character CNPJ in numeric or alphanumeric format
- ✅ **Flexible input**: Accepts `str` or a sequence of `str`; sequence elements are concatenated in order
- ✅ **Format agnostic**: Strips non-alphanumeric characters (or non-digits when `type` is `numeric`) and optionally uppercases before validation
- ✅ **Optional case sensitivity**: When `case_sensitive` is `False`, lowercase letters are accepted for alphanumeric CNPJ
- ✅ **Per-call override model**: Instance defaults can be overridden for one `is_valid()` call only
- ✅ **Typed option validation**: Dedicated `TypeError` / `Exception` subclasses for invalid option or input usage
- ✅ **Minimal dependencies**: [`cnpj-dv`](https://pypi.org/project/cnpj-dv/) for check-digit calculation and [`lacus.utils`](https://pypi.org/project/lacus.utils/) for type descriptions in error messages
- ✅ **Dual API style**: Object-oriented (`CnpjValidator`) and functional (`cnpj_val()`)

## Installation

```bash
$ pip install cnpj-val
```

## Import

```python
from cnpj_val import CnpjValidator, CnpjValidatorOptions, cnpj_val
```

## Quick start

```python
from cnpj_val import CnpjValidator

validator = CnpjValidator()

validator.is_valid('98765432000198')       # True
validator.is_valid('98.765.432/0001-98')   # True
validator.is_valid('98765432000199')       # False

validator.is_valid('1QB5UKALPYFP59')                         # True (alphanumeric)
validator.is_valid('1QB5UKALpyfp59')                         # False (default is case-sensitive)
validator.is_valid('1QB5UKALpyfp59', case_sensitive=False)   # True

validator.is_valid('96206256120884')              # True (numeric)
validator.is_valid('1QB5UKALPYFP59', type='numeric')   # False (letters stripped → length ≠ 14)
```

Functional helper:

```python
from cnpj_val import cnpj_val

cnpj_val('98765432000198')      # True
cnpj_val('98.765.432/0001-98')  # True
cnpj_val('98765432000199')      # False
```

## Usage

The main entry points are the class `CnpjValidator`, the options class `CnpjValidatorOptions`, and the helper `cnpj_val()`.

### `CnpjValidator`

- **`__init__`**: Optional default validation options. The first parameter may be `None`, a mapping of option keys, or a `CnpjValidatorOptions` instance (that exact instance is stored; mutating it later affects subsequent `is_valid()` calls that do not pass per-call options). You may also pass option fields as keyword-only arguments (`case_sensitive`, `type`). Example: `CnpjValidator(type='numeric', case_sensitive=False)`.
- **`options`**: Property returning the instance’s `CnpjValidatorOptions` (same object used internally).
- **`is_valid(cnpj_input, options=None, *, case_sensitive=None, type=None)`**: Validates a CNPJ value.

  Input is normalized to a string (sequences of strings are concatenated). When `case_sensitive` is `False`, the string is uppercased before sanitization. Characters are stripped according to `type`. If the sanitized length is not exactly **14**, the last two characters are not digits, or check digits do not match (`CnpjCheckDigits` from **`cnpj-dv`**), the method returns `False` — no exception is thrown for validation failure.

  If the input is not a `str` or a sequence of `str`, **`CnpjValidatorInputTypeError`** is raised.

  Per-call options are merged over the instance defaults for that call only (instance defaults are unchanged). Pass a `CnpjValidatorOptions` instance or a mapping as the second argument, in addition to keyword-only arguments; when both are provided, the `options` argument wins.

```python
from cnpj_val import CnpjValidator

validator = CnpjValidator(type='numeric')

validator.is_valid('98.765.432/0001-98')   # True
validator.is_valid('1QB5UKALPYFP59')       # False (letters stripped → length ≠ 14)
validator.is_valid('1QB5UKALpyfp59', type='alphanumeric', case_sensitive=False)  # True
```

Default options on the instance; per-call overrides:

```python
validator = CnpjValidator(case_sensitive=False)

validator.is_valid('1qb5ukalpyfp59')                  # True (instance defaults)
validator.is_valid('1qb5ukalpyfp59', case_sensitive=True)  # this call only: False
validator.is_valid('1qb5ukalpyfp59')                  # True again
```

### `CnpjValidatorOptions`

Holds validator settings (`case_sensitive`, `type`). Construct with an optional options mapping or `CnpjValidatorOptions` instance, optional extra override objects (merged in order), and/or keyword-only arguments. Exposes properties: `case_sensitive`, `type`.

- **`all`**: Returns an immutable shallow snapshot of all current options (`MappingProxyType`).
- **`set(options)`**: Updates multiple fields at once; returns `self`. Accepts a mapping or another `CnpjValidatorOptions` instance.

```python
from cnpj_val import CnpjValidatorOptions

options = CnpjValidatorOptions(case_sensitive=False, type='numeric')
options.case_sensitive   # False
options.type             # 'numeric'
options.set({'type': 'alphanumeric'})  # merge and return self
options.all              # immutable snapshot of current options
```

### Functional helper

`cnpj_val()` builds a new `CnpjValidator` from the same constructor parameters and calls `is_valid(cnpj_input)` once. Use keyword-only arguments, a mapping, or a `CnpjValidatorOptions` instance for options:

```python
from cnpj_val import cnpj_val

cnpj_val('98765432000198')                              # True
cnpj_val('1QB5UKALpyfp59', case_sensitive=False)        # True
cnpj_val('1QB5UKALPYFP59', type='numeric')              # False
cnpj_val('1QB5UKALpyfp59', {                            # mapping form
    'type': 'alphanumeric',
    'case_sensitive': False,
})                                                      # True
```

### Input formats

**String:** Raw digits and/or letters, or formatted CNPJ (e.g. `98.765.432/0001-98`, `1Q.B5U.KAL/PYFP-59`). Characters are stripped according to `type`; when `case_sensitive` is `False`, letters are uppercased before alphanumeric validation.

**Sequence of strings:** Each element must be a `str`; values are concatenated (e.g. per digit, grouped segments, or mixed with punctuation). Non-string elements raise **`CnpjValidatorInputTypeError`**.

```python
from cnpj_val import cnpj_val

cnpj_val(['1', 'Q', 'B', '5', 'U', 'K', 'A', 'L', 'P', 'Y', 'F', 'P', '5', '9'])  # True
cnpj_val(['1Q.B5U', 'KAL', 'PYFP-59'])  # True
```

### Validation options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | `'alphanumeric'` \| `'numeric'` \| `None` | `'alphanumeric'` | Character set after sanitization: alphanumeric (`0`–`9`, `A`–`Z`, `a`–`z`) or numeric-only (`0`–`9`) |
| `case_sensitive` | `bool \| None` | `True` | When `False`, lowercase letters are uppercased before alphanumeric validation |

Invalid CNPJ (wrong length after sanitization, invalid check digits, ineligible base/branch `00000000` / `0000`, repeated digits, non-numeric verifier digits) returns **`False`** — no exception is thrown for validation failure.

Example with all options:

```python
from cnpj_val import cnpj_val

cnpj_val(
    '1QB5UKALpyfp59',
    type='alphanumeric',
    case_sensitive=False,
)
```

### Errors & exceptions

This package uses **TypeError** for invalid option/input types and **Exception** for invalid option values. Validation failures return `False`.

- **Wrong input type** (not `str` or a sequence of `str`): **`CnpjValidatorInputTypeError`** — extends **`CnpjValidatorTypeError`** (extends built-in `TypeError`).
- **Invalid option types when constructing or merging options**: **`CnpjValidatorOptionsTypeError`**.
- **Invalid `type` value** (not `alphanumeric` / `numeric`): **`CnpjValidatorOptionTypeInvalidException`** — extends **`CnpjValidatorException`**.

```python
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    cnpj_val,
)

# Input type (e.g. integer not allowed)
try:
    cnpj_val(12345678000198)
except CnpjValidatorInputTypeError as e:
    print(e)  # CNPJ input must be of type string or string[]. Got integer number.

# Option type (e.g. `type` must be string)
try:
    cnpj_val('98765432000198', type=123)
except CnpjValidatorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Invalid type value
try:
    cnpj_val('98765432000198', type='invalid')
except CnpjValidatorOptionTypeInvalidException as e:
    print(e.expected_values, e.actual_input)

# Any exception from the package
try:
    CnpjValidator(type='invalid')
except CnpjValidatorException as e:
    pass  # handle
```

## API

### Exports

All public symbols are available from the `cnpj_val` package:

- **`cnpj_val`**: `(cnpj_input: CnpjInput, options=None, *, case_sensitive=None, type=None) -> bool` — convenience helper.
- **`CnpjValidator`**: Class to validate CNPJ with optional default options; accepts `CnpjInput` in `is_valid()`.
- **`CnpjValidatorOptions`**: Class holding options; supports merge via constructor, `set()`, and keyword-only arguments.
- **`CNPJ_LENGTH`**: `14` (constant).
- **`CnpjInput`**: Type alias — `str | Sequence[str]`.
- **`CnpjType`**: Type alias — `Literal["alphanumeric", "numeric"]`.
- **`CnpjValidatorOptionsInput`**, **`CnpjValidatorOptionsType`**: Options typing helpers.
- **Exceptions**: `CnpjValidatorTypeError`, `CnpjValidatorInputTypeError`, `CnpjValidatorOptionsTypeError`, `CnpjValidatorException`, `CnpjValidatorOptionTypeInvalidException`.

### Other available resources

- **`CnpjValidatorOptions.CNPJ_LENGTH`**: `14`.
- **`CnpjValidatorOptions.DEFAULT_CASE_SENSITIVE`**: `True`.
- **`CnpjValidatorOptions.DEFAULT_TYPE`**: `'alphanumeric'`.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-val/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
