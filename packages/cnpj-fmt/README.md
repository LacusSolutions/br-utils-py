![cnpj-fmt for Python](https://br-utils.vercel.app/img/cover_cnpj-fmt.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-fmt)](https://pypi.org/project/cnpj-fmt)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-fmt)](https://pypi.org/project/cnpj-fmt)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-fmt)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Full support for the [new alphanumeric CNPJ format](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Acessar documentação em português](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-fmt/README.pt.md)

A Python utility to format CNPJ (Brazilian Business Tax ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Alphanumeric CNPJ**: Supports 14-character alphanumeric CNPJ (digits and letters, e.g. `RK0CMT3W000100`)
- ✅ **Flexible input**: Accepts `str` or a sequence of `str`; sequence elements are concatenated in order
- ✅ **Format agnostic**: Strips non-alphanumeric characters and uppercases letters before formatting
- ✅ **Custom delimiters**: `dot_key`, `slash_key`, and `dash_key` may be empty, single-, or multi-character strings
- ✅ **Masking**: Optional hiding of a character range with a configurable replacement string (`hidden`, `hidden_key`, `hidden_start`, `hidden_end`)
- ✅ **HTML & URL output**: Optional `escape` (HTML entities) and `encode` (URI component encoding, similar to JavaScript `encodeURIComponent`)
- ✅ **Length errors without throwing**: Invalid length after sanitization is handled via `on_fail` (default returns an empty string)
- ✅ **Minimal dependencies**: Only [`lacus.utils`](https://pypi.org/project/lacus.utils/)
- ✅ **Error handling**: Type errors for wrong API use; option validation via dedicated exception classes

## Installation

```bash
$ pip install cnpj-fmt
```

## Import

```python
from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions, cnpj_fmt
```

## Quick start

```python
from cnpj_fmt import CnpjFormatter

formatter = CnpjFormatter()

formatter.format('03603568000195')   # '03.603.568/0001-95'
formatter.format('12ABC34500DE99')   # '12.ABC.345/00DE-99'
formatter.format('RK0CMT3W000100')   # 'RK.0CM.T3W/0001-00'
```

## Usage

The main entry points are the class `CnpjFormatter`, the options class `CnpjFormatterOptions`, and the helper `cnpj_fmt()`.

### `CnpjFormatter`

- **`__init__`**: Optional default formatting options. The first parameter may be `None`, a mapping of option keys, or a `CnpjFormatterOptions` instance (that exact instance is stored; mutating it later affects subsequent `format()` calls that do not pass per-call options). You may also pass option fields as keyword arguments (`hidden`, `hidden_key`, `dot_key`, …). Example: `CnpjFormatter(hidden=True, slash_key='|')`.
- **`options`**: Property returning the instance’s `CnpjFormatterOptions` (same object used internally).
- **`format(cnpj_input, options=None, …)`**: Formats a CNPJ value.

  Input is normalized by removing non-alphanumeric characters and uppercasing. If the sanitized length is not exactly **14**, the **`on_fail`** callback is invoked with the original input and a `CnpjFormatterInputLengthException`; its return value is the result (nothing is thrown for length).

  If the input is not a `str` or a sequence of `str`, **`CnpjFormatterInputTypeError`** is raised.

  Per-call options are merged over the instance defaults for that call only (instance defaults are unchanged). Pass a `CnpjFormatterOptions` instance or a mapping as the second argument, in addition to keyword arguments; later overrides win.

### `CnpjFormatterOptions`

Holds all formatter settings. Construct with an optional options mapping or `CnpjFormatterOptions` instance, optional extra override objects (merged in order), and/or keyword arguments. Exposes properties: `hidden`, `hidden_key`, `hidden_start`, `hidden_end`, `dot_key`, `slash_key`, `dash_key`, `escape`, `encode`, `on_fail`.

- **`all`**: Returns a shallow copy of all current options.
- **`copy()`**: Returns a shallow copy of this options instance.
- **`set(options)`**: Updates multiple fields at once; returns `self`. Accepts a mapping or another `CnpjFormatterOptions` instance.
- **`set_hidden_range(hidden_start, hidden_end)`**: Validates indices in **`[0, 13]`** (inclusive); if `hidden_start > hidden_end`, values are swapped. `None` arguments fall back to defaults (`DEFAULT_HIDDEN_START` / `DEFAULT_HIDDEN_END`).

**`hidden_start` / `hidden_end`**: Indices refer to the **14-character normalized CNPJ string** (before inserting punctuation). The inclusive range is replaced internally by placeholders, then `hidden_key` is substituted (supports multi-character keys and empty string).

**Key options** (`hidden_key`, `dot_key`, `slash_key`, `dash_key`): Must be strings and must not contain any character in `CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS` (reserved for internal formatting).

### Functional helper

`cnpj_fmt()` builds a new `CnpjFormatter` from the same constructor parameters and calls `format(cnpj_input)` once. Use keyword arguments, a mapping, or a `CnpjFormatterOptions` instance for options:

```python
from cnpj_fmt import cnpj_fmt

cnpj = '03603568000195'

cnpj_fmt(cnpj)                # '03.603.568/0001-95'
cnpj_fmt(cnpj, hidden=True)   # masked with defaults
cnpj_fmt(                     # '03603568|0001_95'
    cnpj,
    dot_key='',
    slash_key='|',
    dash_key='_',
)
cnpj_fmt(cnpj, {              # mapping form
    'hidden': True,
    'hidden_key': '#',
})
```

### Object-oriented examples

```python
from cnpj_fmt import CnpjFormatter

formatter = CnpjFormatter()
cnpj = '03603568000195'

formatter.format(cnpj)   # '03.603.568/0001-95'
formatter.format(        # '03.603.###/####-##'
    cnpj,
    hidden=True,
    hidden_key='#',
    hidden_start=5,
    hidden_end=13,
)
```

Default options on the instance; per-call overrides:

```python
formatter = CnpjFormatter(hidden=True)

formatter.format(cnpj)                 # uses instance masking
formatter.format(cnpj, hidden=False)   # this call only: unmasked
formatter.format(cnpj)                 # back to instance defaults
```

Alphanumeric input and sequence input:

```python
formatter.format('RK0CMT3W000100')   # 'RK.0CM.T3W/0001-00'
formatter.format([                   # 'RK.0CM.T3W/0001-00'
    'RK',
    '0CM',
    'T3W',
    '0001',
    '00',
])
```

### Input formats

**String:** Raw digits and/or letters, or already formatted CNPJ (e.g. `12.345.678/0009-10`, `12.ABC.345/00DE-99`). Non-alphanumeric characters are removed; lowercase letters are uppercased.

**Sequence of strings:** Each element must be a `str`; values are concatenated (e.g. per digit, grouped segments, or mixed with punctuation — all are stripped during normalization). Non-string elements are not allowed.

### Formatting options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hidden` | `bool \| None` | `False` | When `True`, replaces the inclusive index range `[hidden_start, hidden_end]` on the normalized 14-character string before punctuation is applied |
| `hidden_key` | `str \| None` | `'*'` | Replacement for each hidden position (may be multi-character or empty); must not use disallowed key characters |
| `hidden_start` | `int \| None` | `5` | Start index `0`–`13` (inclusive) |
| `hidden_end` | `int \| None` | `13` | End index `0`–`13` (inclusive); if `hidden_start > hidden_end`, they are swapped |
| `dot_key` | `str \| None` | `'.'` | Separator between groups `XX` / `XXX` / `XXX` |
| `slash_key` | `str \| None` | `'/'` | Separator before the branch block |
| `dash_key` | `str \| None` | `'-'` | Separator before the last two characters |
| `escape` | `bool \| None` | `False` | When `True`, HTML-escapes the final string |
| `encode` | `bool \| None` | `False` | When `True`, URL-encodes the final string (similar to `encodeURIComponent`) |
| `on_fail` | `Callable \| None` | see below | `(value, exception) -> str` — used when sanitized length ≠ 14 |

Default **`on_fail`** returns an empty string. The exception passed for length failures is **`CnpjFormatterInputLengthException`** (`actual_input`, `evaluated_input`, `expected_length`).

Example with all options:

```python
from cnpj_fmt import cnpj_fmt

cnpj = '03603568000195'

cnpj_fmt(
    cnpj,
    hidden=True,
    hidden_key='#',
    hidden_start=5,
    hidden_end=11,
    dot_key=' ',
    slash_key='|',
    dash_key='_-_',
    escape=True,
    encode=True,
    on_fail=lambda value, exception: str(value),
)
```

### Errors & exceptions

- **Wrong input type** (not `str` or a sequence of `str`): **`CnpjFormatterInputTypeError`** — extends **`CnpjFormatterTypeError`** (extends built-in `TypeError`).
- **Invalid option types or values when constructing or merging options**: **`CnpjFormatterOptionsTypeError`**, **`CnpjFormatterOptionsHiddenRangeInvalidException`**, **`CnpjFormatterOptionsForbiddenKeyCharacterException`** — extend **`CnpjFormatterTypeError`** or **`CnpjFormatterException`** as appropriate.

Length mismatch does **not** throw from `format()`; handle it inside **`on_fail`**.

```python
from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
)

try:
    CnpjFormatter().format(12345)
except CnpjFormatterInputTypeError as e:
    e  # handle type error

CnpjFormatter().format(
    'short',
    on_fail=lambda value, exception: 'invalid',
)  # 'invalid'
```

## API

### Exports

All public symbols are available from the `cnpj_fmt` package:

- **`cnpj_fmt`**: `(cnpj_input: CnpjInput, options=None, **kwargs) -> str` — convenience helper.
- **`CnpjFormatter`**: Class to format CNPJ with optional default options; accepts `CnpjInput` in `format()`.
- **`CnpjFormatterOptions`**: Class holding options; supports merge via constructor, `set()`, and keyword arguments.
- **`CNPJ_LENGTH`**: `14` (constant).
- **`CnpjInput`**: Type alias — `str | Sequence[str]`.
- **Exceptions**: `CnpjFormatterTypeError`, `CnpjFormatterInputTypeError`, `CnpjFormatterOptionsTypeError`, `CnpjFormatterException`, `CnpjFormatterInputLengthException`, `CnpjFormatterOptionsHiddenRangeInvalidException`, `CnpjFormatterOptionsForbiddenKeyCharacterException`.

### Other available resources

- **`CnpjFormatterOptions.CNPJ_LENGTH`**: `14`.
- **`CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS`**: Characters forbidden in `hidden_key`, `dot_key`, `slash_key`, `dash_key`.
- **`CnpjFormatterOptions.DEFAULT_*`**: Default values for each option.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-fmt/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
