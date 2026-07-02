![cnpj-utils for Python](https://br-utils.vercel.app/img/cover_cnpj-utils.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-utils)](https://pypi.org/project/cnpj-utils)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-utils)](https://pypi.org/project/cnpj-utils)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-utils)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Full support for the [new alphanumeric CNPJ format](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Acessar documentação em português](./README.pt.md)

Utilities to deal with CNPJ (Brazilian Business Tax ID). This package wraps [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt), [`cnpj-gen`](https://pypi.org/project/cnpj-gen), and [`cnpj-val`](https://pypi.org/project/cnpj-val) in a single API and re-exports their public resources.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Unified API**: One default instance with `format`, `generate`, and `is_valid`; or use the underlying `cnpj_fmt`, `cnpj_gen`, and `cnpj_val` helpers
- ✅ **Alphanumeric CNPJ**: Format, generate, and validate 14-character numeric or alphanumeric CNPJ
- ✅ **Reusable instance**: `CnpjUtils` class with optional default settings (formatter, generator, validator options or instances)
- ✅ **Full re-exports**: All formatter, generator, and validator classes, options, and exceptions from the three component packages
- ✅ **Type hints**: Built for Python 3.10+ with full type annotations
- ✅ **Flexible input**: `format()` and `is_valid()` accept `str` or a sequence of `str` (elements concatenated in order)
- ✅ **Per-call overrides**: Instance defaults plus keyword or mapping overrides on each method call
- ✅ **Error handling**: Same type errors and exceptions as the underlying packages

## Installation

```bash
$ pip install cnpj-utils
```

This installs **`cnpj-utils`** together with [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt), [`cnpj-gen`](https://pypi.org/project/cnpj-gen), and [`cnpj-val`](https://pypi.org/project/cnpj-val). You do **not** need separate `pip install` calls for the component packages when using **`cnpj-utils`**.

## Quick Start

```python
from cnpj_utils import CnpjUtils, cnpj_fmt, cnpj_gen, cnpj_val, cnpj_utils
```

Basic usage with the default singleton:

```python
from cnpj_utils import cnpj_utils

cnpj = '03603568000195'

cnpj_utils.format(cnpj)                # '03.603.568/0001-95'
cnpj_utils.format(cnpj, hidden=True)   # '03.603.***/****-**'
cnpj_utils.format(                     # '03603568|0001_95'
    cnpj,
    dot_key='',
    slash_key='|',
    dash_key='_',
)

cnpj_utils.generate()                    # e.g. 'AB123CDE000155' (14-char alphanumeric)
cnpj_utils.generate(format=True)         # e.g. 'AB.123.CDE/0001-55'
cnpj_utils.generate(prefix='45623767')   # e.g. '45623767000296'
cnpj_utils.generate(type='numeric')      # e.g. '65453043000178' (digits only)

cnpj_utils.is_valid('98765432000198')       # True
cnpj_utils.is_valid('98.765.432/0001-98')   # True
cnpj_utils.is_valid('1QB5UKALPYFP59')       # True (alphanumeric)
cnpj_utils.is_valid('98765432000199')       # False
```

## Usage

You can work in three equivalent ways:

1. **`cnpj_utils`** — pre-built singleton for quick one-off calls.
2. **`CnpjUtils`** — configurable instance with shared defaults across format, generate, and validate.
3. **Component classes and helpers** — `CnpjFormatter`, `CnpjGenerator`, `CnpjValidator`, and `cnpj_fmt()`, `cnpj_gen()`, `cnpj_val()` (same classes used internally by `CnpjUtils`).

All three approaches expose the same options and behavior. For exhaustive option tables and component-specific details, see the README of each [bundled package](#bundled-packages).

### Formatter options

When calling `format(cnpj_input, options=None, …)`, all options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hidden` | `bool` | `False` | When `True`, mask characters in `hidden_start`–`hidden_end` with `hidden_key` |
| `hidden_key` | `str` | `'*'` | Character(s) used to replace masked characters |
| `hidden_start` | `int` | `5` | Start index (0–13, inclusive) of the range to hide |
| `hidden_end` | `int` | `13` | End index (0–13, inclusive) of the range to hide |
| `dot_key` | `str` | `'.'` | Dot delimiter (e.g. in `12.345.678`) |
| `slash_key` | `str` | `'/'` | Slash delimiter (e.g. before branch `…/0001-90`) |
| `dash_key` | `str` | `'-'` | Dash delimiter (e.g. before check digits `…-90`) |
| `escape` | `bool` | `False` | When `True`, escape HTML special characters in the result |
| `encode` | `bool` | `False` | When `True`, URL-encode the result (similar to JavaScript `encodeURIComponent`) |
| `on_fail` | `Callable` | returns `''` | Callback when sanitized input length ≠ 14; return value is used as result |

### Generator options

When calling `generate(options=None, …)`, all options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | When `True`, return the generated CNPJ in standard format (`00.000.000/0000-00`) |
| `prefix` | `str` | `''` | Partial start string (0–12 alphanumeric chars). Missing characters are generated and check digits computed. |
| `type` | `'numeric'` \| `'alphabetic'` \| `'alphanumeric'` | `'alphanumeric'` | Character set for the randomly generated part. **Check digits are always numeric.** |

Prefix rules: base ID (first 8 chars) and branch ID (chars 9–12) cannot be all zeros; 12 repeated digits (e.g. `111111111111`) are also not allowed.

### Validator options

When calling `is_valid(cnpj_input, options=None, …)`, all options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `case_sensitive` | `bool` | `True` | When `False`, lowercase letters are accepted for alphanumeric CNPJ (input is uppercased before validation). |
| `type` | `'numeric'` \| `'alphanumeric'` | `'alphanumeric'` | `'numeric'`: only digits (0–9); `'alphanumeric'`: digits and letters (0–9, A–Z). |

### `cnpj_utils` (default instance)

The module-level `cnpj_utils` is a pre-built `CnpjUtils` instance. Use it for quick one-off calls:

- **`format(cnpj_input, options=None, …)`**: Formats a CNPJ string or sequence of strings. Delegates to the internal formatter. Input must be 14 alphanumeric characters (after sanitization); otherwise `on_fail` is used.
- **`generate(options=None, …)`**: Generates a valid CNPJ. Delegates to the internal generator.
- **`is_valid(cnpj_input, options=None, …)`**: Returns `True` if the CNPJ is valid. Delegates to the internal validator.

### `CnpjUtils` (class)

For custom default formatter, generator, or validator, create your own instance:

```python
from cnpj_utils import CnpjUtils

utils = CnpjUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'type': 'numeric', 'format': True},
    validator={'type': 'numeric', 'case_sensitive': False},
)

utils.format('RK0CMT3W000100')        # 'RK.0CM.###/####-##'
utils.generate()                      # e.g. '73.008.535/0005-06'
utils.is_valid('98.765.432/0001-98')  # True

# Access or replace internal instances
utils.formatter  # CnpjFormatter
utils.generator  # CnpjGenerator
utils.validator  # CnpjValidator
```

- **`__init__(*, formatter=None, generator=None, validator=None)`**: Each keyword may be an options mapping, a `CnpjFormatterOptions` / `CnpjGeneratorOptions` / `CnpjValidatorOptions` instance (stored by reference — mutating it later affects subsequent calls with no per-call override), a component instance, or omitted for defaults. Passing `None` for a component creates a new instance with default options.
- **`format(cnpj_input, options=None, …)`**: Same as the default instance; per-call options override the formatter's defaults for that call only.
- **`generate(options=None, …)`**: Same as the default instance; per-call options override the generator's defaults.
- **`is_valid(cnpj_input, options=None, …)`**: Same as the default instance; per-call options override the validator's defaults.
- **`formatter`**, **`generator`**, **`validator`**: Properties with getters and setters for the internal formatter, generator, and validator. Setters accept the same shapes as the constructor. To change a single option without replacing the instance, mutate the component's options (e.g. `utils.formatter.options.hidden = True`).

Instance defaults and per-call overrides:

```python
utils = CnpjUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True},
    validator={'type': 'numeric'},
)

cnpj = '03603568000195'

utils.format(cnpj)                 # masked (instance formatter defaults)
utils.format(cnpj, hidden=False)   # this call only: unmasked
utils.generate(format=False)       # this call only: compact output
utils.is_valid('1QB5UKALPYFP59')   # False (instance validator is numeric-only)
utils.is_valid(                    # True for this call
    '1QB5UKALPYFP59',
    type='alphanumeric',
)
```

Options can also be passed as a mapping on each method:

```python
utils.format(cnpj, {'slash_key': '|'})
utils.generate({'prefix': '12345', 'type': 'numeric'})
utils.is_valid('1QB5UKALPYFP59', {'case_sensitive': False})
```

### Using the underlying helpers and classes

You can use the re-exported formatter, generator, and validator directly:

```python
from cnpj_utils import (
    cnpj_fmt,
    CnpjFormatter,
    cnpj_gen,
    CnpjGenerator,
    cnpj_val,
    CnpjValidator,
)

cnpj_fmt('01ABC234000X56', slash_key='|')   # '01.ABC.234|000X-56'
cnpj_gen(type='numeric')                    # e.g. '65453043000178'
cnpj_val('9JN7MGLJZXIO50')                  # True

formatter = CnpjFormatter({'hidden': True})
formatter.format('AB123XYZ000123')          # 'AB.123.***/****-**'
```

See [`cnpj-fmt`](./../cnpj-fmt/README.md), [`cnpj-gen`](./../cnpj-gen/README.md), and [`cnpj-val`](./../cnpj-val/README.md) for full option and error details.

## API

### Exports

- **`cnpj_utils`**: Pre-built `CnpjUtils` instance with `format`, `generate`, and `is_valid`.
- **`CnpjUtils`**: Class to create a utils instance with optional default formatter, generator, and validator settings.
- **Formatter**: `cnpj_fmt`, `CnpjFormatter`, `CnpjFormatterOptions`, and formatter exceptions (see [cnpj-fmt](./../cnpj-fmt/README.md)).
- **Generator**: `cnpj_gen`, `CnpjGenerator`, `CnpjGeneratorOptions`, and generator exceptions (see [cnpj-gen](./../cnpj-gen/README.md)).
- **Validator**: `cnpj_val`, `CnpjValidator`, `CnpjValidatorOptions`, and validator exceptions (see [cnpj-val](./../cnpj-val/README.md)).

### Errors & Exceptions

`CnpjUtils` does not define its own exception types; it propagates errors from the bundled packages:

- **Formatting**: `CnpjFormatterInputTypeError`, `CnpjFormatterOptionsTypeError`, `CnpjFormatterOptionsHiddenRangeInvalidException`, `CnpjFormatterOptionsForbiddenKeyCharacterException`, and related classes.
- **Generation**: `CnpjGeneratorOptionsTypeError`, `CnpjGeneratorOptionPrefixInvalidException`, `CnpjGeneratorOptionTypeInvalidException`, and related classes.
- **Validation**: `CnpjValidatorInputTypeError`, `CnpjValidatorOptionsTypeError`, `CnpjValidatorOptionTypeInvalidException`, and related classes.

Invalid option types are **`TypeError`** subclasses; invalid option values are **`Exception`** subclasses. Validation failure returns `False`; formatting length failure is handled by **`on_fail`** (default returns an empty string).

```python
from cnpj_utils import CnpjUtils, cnpj_fmt
from cnpj_fmt import CnpjFormatterInputTypeError
from cnpj_val import CnpjValidatorInputTypeError

try:
    CnpjUtils().format(12345)
except CnpjFormatterInputTypeError as e:
    print(e)

try:
    CnpjUtils().is_valid(12345678000198)
except CnpjValidatorInputTypeError as e:
    print(e)

# Custom on_fail for invalid length
def custom_fail(value, exception=None):
    return f'Invalid CNPJ: {value}'

cnpj_fmt('123', on_fail=custom_fail)  # 'Invalid CNPJ: 123'
cnpj_fmt('123')                       # '' (default on_fail)
```

### Bundled packages

| Package | Main resources | README |
|---------|----------------|--------|
| [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt) | `CnpjFormatter`, `CnpjFormatterOptions`, `cnpj_fmt()` | [docs](./../cnpj-fmt/README.md) |
| [`cnpj-gen`](https://pypi.org/project/cnpj-gen) | `CnpjGenerator`, `CnpjGeneratorOptions`, `cnpj_gen()` | [docs](./../cnpj-gen/README.md) |
| [`cnpj-val`](https://pypi.org/project/cnpj-val) | `CnpjValidator`, `CnpjValidatorOptions`, `cnpj_val()` | [docs](./../cnpj-val/README.md) |

All of the above are pulled in as dependencies of **`cnpj-utils`**. For exhaustive option tables, exception lists, and edge-case behavior, see each package README.

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
