![cpf-fmt for Python](https://br-utils.vercel.app/img/cover_cpf-fmt.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-fmt)](https://pypi.org/project/cpf-fmt)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-fmt)](https://pypi.org/project/cpf-fmt)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-fmt)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-fmt/README.pt.md)

A Python utility to format CPF (Brazilian Individual's Taxpayer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Flexible input**: Accepts `str` or a sequence of `str`; sequence elements are concatenated in order
- ✅ **Format agnostic**: Strips non-digit characters before formatting
- ✅ **Custom delimiters**: `dot_key` and `dash_key` may be empty, single-, or multi-character strings
- ✅ **Masking**: Optional hiding of a digit range with a configurable replacement string (`hidden`, `hidden_key`, `hidden_start`, `hidden_end`)
- ✅ **HTML & URL output**: Optional `escape` (HTML entities) and `encode` (URI component encoding, similar to JavaScript `encodeURIComponent`)
- ✅ **Length errors without throwing**: Invalid length after sanitization is handled via `on_fail` (default returns an empty string)
- ✅ **Minimal dependencies**: Only [`lacus.utils`](https://pypi.org/project/lacus.utils/)
- ✅ **Error handling**: Type errors for wrong API use; option validation via dedicated exception classes

## Installation

```bash
$ pip install cpf-fmt
```

## Import

```python
from cpf_fmt import CpfFormatter, CpfFormatterOptions, cpf_fmt
```

## Quick start

```python
from cpf_fmt import CpfFormatter

formatter = CpfFormatter()

formatter.format('03603568195')      # '036.035.681-95'
formatter.format('123.456.789-10')   # '123.456.789-10'
formatter.format('12345678910')      # '123.456.789-10'
```

## Usage

The main entry points are the class `CpfFormatter`, the options class `CpfFormatterOptions`, and the helper `cpf_fmt()`.

### `CpfFormatter`

- **`__init__`**: Optional default formatting options. The first parameter may be `None`, a mapping of option keys, or a `CpfFormatterOptions` instance (that exact instance is stored; mutating it later affects subsequent `format()` calls that do not pass per-call options). You may also pass option fields as keyword arguments (`hidden`, `hidden_key`, `dot_key`, …). Example: `CpfFormatter(hidden=True, dash_key='_')`.
- **`options`**: Property returning the instance’s `CpfFormatterOptions` (same object used internally).
- **`format(cpf_input, options=None, …)`**: Formats a CPF value.

  Input is normalized by removing non-digit characters. If the sanitized length is not exactly **11**, the **`on_fail`** callback is invoked with the original input and a `CpfFormatterInputLengthException`; its return value is the result (nothing is thrown for length).

  If the input is not a `str` or a sequence of `str`, **`CpfFormatterInputTypeError`** is raised.

  Per-call options are merged over the instance defaults for that call only (instance defaults are unchanged). Pass a `CpfFormatterOptions` instance or a mapping as the second argument, in addition to keyword arguments; when both are provided, the `options` argument wins.

### `CpfFormatterOptions`

Holds all formatter settings. Construct with an optional options mapping or `CpfFormatterOptions` instance, optional extra override objects (merged in order), and/or keyword arguments. Exposes properties: `hidden`, `hidden_key`, `hidden_start`, `hidden_end`, `dot_key`, `dash_key`, `escape`, `encode`, `on_fail`.

- **`all`**: Returns a shallow copy of all current options.
- **`copy()`**: Returns a shallow copy of this options instance.
- **`set(options)`**: Updates multiple fields at once; returns `self`. Accepts a mapping or another `CpfFormatterOptions` instance.
- **`set_hidden_range(hidden_start, hidden_end)`**: Validates indices in **`[0, 10]`** (inclusive); if `hidden_start > hidden_end`, values are swapped. `None` arguments fall back to defaults (`DEFAULT_HIDDEN_START` / `DEFAULT_HIDDEN_END`).

**`hidden_start` / `hidden_end`**: Indices refer to the **11-digit normalized CPF string** (before inserting punctuation). The inclusive range is replaced internally by placeholders, then `hidden_key` is substituted (supports multi-character keys and empty string).

**Key options** (`hidden_key`, `dot_key`, `dash_key`): Must be strings and must not contain any character in `CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS` (reserved for internal formatting).

### Functional helper

`cpf_fmt()` builds a new `CpfFormatter` from the same constructor parameters and calls `format(cpf_input)` once. Use keyword arguments, a mapping, or a `CpfFormatterOptions` instance for options:

```python
from cpf_fmt import cpf_fmt

cpf = '03603568195'

cpf_fmt(cpf)                # '036.035.681-95'
cpf_fmt(cpf, hidden=True)   # masked with defaults
cpf_fmt(                    # '036035681_95'
    cpf,
    dot_key='',
    dash_key='_',
)
cpf_fmt(cpf, {              # mapping form
    'hidden': True,
    'hidden_key': '#',
})
```

### Object-oriented examples

```python
from cpf_fmt import CpfFormatter

formatter = CpfFormatter()
cpf = '12345678910'

formatter.format(cpf)   # '123.456.789-10'
formatter.format(       # '123.###.###-##'
    cpf,
    hidden=True,
    hidden_key='#',
    hidden_start=3,
    hidden_end=10,
)
```

Default options on the instance; per-call overrides:

```python
formatter = CpfFormatter(hidden=True)

formatter.format(cpf)                 # uses instance masking
formatter.format(cpf, hidden=False)   # this call only: unmasked
formatter.format(cpf)                 # back to instance defaults
```

Sequence input:

```python
formatter.format([                   # '123.456.789-10'
    '123',
    '456',
    '789',
    '10',
])
```

### Input formats

**String:** Raw digits, or already formatted CPF (e.g. `123.456.789-10`, `123 456 789 10`). Non-digit characters are removed; leading zeros are preserved.

**Sequence of strings:** Each element must be a `str`; values are concatenated (e.g. per digit, grouped segments, or mixed with punctuation — all non-digits are stripped during normalization). Non-string elements are not allowed.

### Formatting options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hidden` | `bool \| None` | `False` | When `True`, replaces the inclusive index range `[hidden_start, hidden_end]` on the normalized 11-digit string before punctuation is applied |
| `hidden_key` | `str \| None` | `'*'` | Replacement for each hidden position (may be multi-character or empty); must not use disallowed key characters |
| `hidden_start` | `int \| None` | `3` | Start index `0`–`10` (inclusive) |
| `hidden_end` | `int \| None` | `10` | End index `0`–`10` (inclusive); if `hidden_start > hidden_end`, they are swapped |
| `dot_key` | `str \| None` | `'.'` | Separator after the 3rd and 6th digits |
| `dash_key` | `str \| None` | `'-'` | Separator after the 9th digit |
| `escape` | `bool \| None` | `False` | When `True`, HTML-escapes the final string |
| `encode` | `bool \| None` | `False` | When `True`, URL-encodes the final string (similar to `encodeURIComponent`) |
| `on_fail` | `Callable \| None` | see below | `(value, exception) -> str` — used when sanitized length ≠ 11 |

Default **`on_fail`** returns an empty string. The exception passed for length failures is **`CpfFormatterInputLengthException`** (`actual_input`, `evaluated_input`, `expected_length`).

Example with all options:

```python
from cpf_fmt import cpf_fmt

cpf = '12345678910'

cpf_fmt(
    cpf,
    hidden=True,
    hidden_key='#',
    hidden_start=3,
    hidden_end=9,
    dot_key=' ',
    dash_key='_-_',
    escape=True,
    encode=True,
    on_fail=lambda value, exception: str(value),
)
```

### Errors & exceptions

- **Wrong input type** (not `str` or a sequence of `str`): **`CpfFormatterInputTypeError`** — extends **`CpfFormatterTypeError`** (extends built-in `TypeError`).
- **Invalid option types or values when constructing or merging options**: **`CpfFormatterOptionsTypeError`**, **`CpfFormatterOptionsHiddenRangeInvalidException`**, **`CpfFormatterOptionsForbiddenKeyCharacterException`** — extend **`CpfFormatterTypeError`** or **`CpfFormatterException`** as appropriate.

Length mismatch does **not** throw from `format()`; handle it inside **`on_fail`**.

```python
from cpf_fmt import (
    CpfFormatter,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
)

try:
    CpfFormatter().format(12345)
except CpfFormatterInputTypeError as e:
    e  # handle type error

CpfFormatter().format(
    'short',
    on_fail=lambda value, exception: 'invalid',
)  # 'invalid'
```

## API

### Exports

All public symbols are available from the `cpf_fmt` package:

- **`cpf_fmt`**: `(cpf_input: CpfInput, options=None, **kwargs) -> str` — convenience helper.
- **`CpfFormatter`**: Class to format CPF with optional default options; accepts `CpfInput` in `format()`.
- **`CpfFormatterOptions`**: Class holding options; supports merge via constructor, `set()`, and keyword arguments.
- **`CPF_LENGTH`**: `11` (constant).
- **`CpfInput`**: Type alias — `str | Sequence[str]`.
- **Exceptions**: `CpfFormatterTypeError`, `CpfFormatterInputTypeError`, `CpfFormatterOptionsTypeError`, `CpfFormatterException`, `CpfFormatterInputLengthException`, `CpfFormatterOptionsHiddenRangeInvalidException`, `CpfFormatterOptionsForbiddenKeyCharacterException`.

### Other available resources

- **`CpfFormatterOptions.CPF_LENGTH`**: `11`.
- **`CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS`**: Characters forbidden in `hidden_key`, `dot_key`, `dash_key`.
- **`CpfFormatterOptions.DEFAULT_*`**: Default values for each option.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-fmt/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
