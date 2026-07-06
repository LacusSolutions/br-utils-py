![cpf-utils for Python](https://br-utils.vercel.app/img/cover_cpf-utils.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-utils)](https://pypi.org/project/cpf-utils)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-utils)](https://pypi.org/project/cpf-utils)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-utils)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🌎 [Acessar documentação em português](./README.pt.md)

Utilities to deal with CPF (Brazilian Individual's Taxpayer ID). This package wraps [`cpf-fmt`](https://pypi.org/project/cpf-fmt), [`cpf-gen`](https://pypi.org/project/cpf-gen), and [`cpf-val`](https://pypi.org/project/cpf-val) in a single API and re-exports their public resources.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
| --- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Features

- ✅ **Unified API**: One default instance with `format`, `generate`, and `is_valid`; or use the underlying `cpf_fmt`, `cpf_gen`, and `cpf_val` helpers
- ✅ **Reusable instance**: `CpfUtils` class with optional default settings (formatter, generator, validator options or instances)
- ✅ **Full re-exports**: All formatter, generator, and validator classes, options, and exceptions from the three component packages
- ✅ **Type hints**: Built for Python 3.10+ with full type annotations
- ✅ **Flexible input**: `format()` and `is_valid()` accept `str` or a sequence of `str` (elements concatenated in order)
- ✅ **Per-call overrides**: Instance defaults plus keyword or mapping overrides on each method call
- ✅ **Error handling**: Same type errors and exceptions as the underlying packages

## Installation

```bash
$ pip install cpf-utils
```

This installs **`cpf-utils`** together with [`cpf-fmt`](https://pypi.org/project/cpf-fmt), [`cpf-gen`](https://pypi.org/project/cpf-gen), and [`cpf-val`](https://pypi.org/project/cpf-val). You do **not** need separate `pip install` calls for the component packages when using **`cpf-utils`**.

## Quick Start

```python
from cpf_utils import CpfUtils, cpf_fmt, cpf_gen, cpf_val, cpf_utils
```

Basic usage with the default singleton:

```python
from cpf_utils import cpf_utils

cpf = '12345678909'

cpf_utils.format(cpf)                # '123.456.789-09'
cpf_utils.format(cpf, hidden=True)   # '123.***.***-**'
cpf_utils.format(                     # '123456789_09'
    cpf,
    dot_key='',
    dash_key='_',
)

cpf_utils.generate()                   # e.g. '47844241055' (11-digit numeric)
cpf_utils.generate(format=True)        # e.g. '478.442.410-55'
cpf_utils.generate(prefix='528250911') # e.g. '52825091138'

cpf_utils.is_valid('12345678909')      # True
cpf_utils.is_valid('123.456.789-09')   # True
cpf_utils.is_valid('12345678900')      # False
```

## Usage

You can work in three equivalent ways:

1. **`cpf_utils`** — pre-built singleton for quick one-off calls.
2. **`CpfUtils`** — configurable instance with shared defaults across format, generate, and validate.
3. **Component classes and helpers** — `CpfFormatter`, `CpfGenerator`, `CpfValidator`, and `cpf_fmt()`, `cpf_gen()`, `cpf_val()` (same classes used internally by `CpfUtils`).

All three approaches expose the same options and behavior. For exhaustive option tables and component-specific details, see the README of each [bundled package](#bundled-packages).

### Formatter options

When calling `format(cpf_input, options=None, …)`, all options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hidden` | `bool` | `False` | When `True`, mask digits in `hidden_start`–`hidden_end` with `hidden_key` |
| `hidden_key` | `str` | `'*'` | Character(s) used to replace masked digits |
| `hidden_start` | `int` | `3` | Start index (0–10, inclusive) of the range to hide |
| `hidden_end` | `int` | `10` | End index (0–10, inclusive) of the range to hide |
| `dot_key` | `str` | `'.'` | Dot delimiter (e.g. in `123.456.789`) |
| `dash_key` | `str` | `'-'` | Dash delimiter (e.g. before check digits `…-09`) |
| `escape` | `bool` | `False` | When `True`, escape HTML special characters in the result |
| `encode` | `bool` | `False` | When `True`, URL-encode the result (similar to JavaScript `encodeURIComponent`) |
| `on_fail` | `Callable` | returns `''` | Callback when sanitized input length ≠ 11; return value is used as result |

### Generator options

When calling `generate(options=None, …)`, all options are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | When `True`, return the generated CPF in standard format (`000.000.000-00`) |
| `prefix` | `str` | `''` | Partial start string (0–9 digits). Non-digits are stripped; missing characters are generated and check digits computed. Prefixes longer than 9 digits are truncated silently. |

Prefix rules: the base (first 9 digits) cannot be all zeros; 9 repeated digits (e.g. `999999999`) are not allowed.

### `cpf_utils` (default instance)

The module-level `cpf_utils` is a pre-built `CpfUtils` instance. Use it for quick one-off calls:

- **`format(cpf_input, options=None, …)`**: Formats a CPF string or sequence of strings. Delegates to the internal formatter. Input must be 11 digits (after sanitization); otherwise `on_fail` is used.
- **`generate(options=None, …)`**: Generates a valid CPF. Delegates to the internal generator.
- **`is_valid(cpf_input)`**: Returns `True` if the CPF is valid. Delegates to the internal validator. No per-call options — the CPF validator has none.

### `CpfUtils` (class)

For custom default formatter, generator, or validator, create your own instance:

```python
from cpf_utils import CpfUtils

utils = CpfUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True, 'prefix': '123'},
)

utils.format('47844241055')        # '478.###.###-##'
utils.generate()                   # e.g. '005.265.352-88'
utils.is_valid('123.456.789-09')   # True

# Access or replace internal instances
utils.formatter  # CpfFormatter
utils.generator  # CpfGenerator
utils.validator  # CpfValidator
```

- **`__init__(*, formatter=None, generator=None, validator=None)`**: Each keyword may be an options mapping, a `CpfFormatterOptions` / `CpfGeneratorOptions` instance (stored by reference — mutating it later affects subsequent calls with no per-call override), a component instance, or omitted for defaults. Passing `None` for a component creates a new instance with default options.
- **`format(cpf_input, options=None, …)`**: Same as the default instance; per-call options override the formatter's defaults for that call only.
- **`generate(options=None, …)`**: Same as the default instance; per-call options override the generator's defaults.
- **`is_valid(cpf_input)`**: Same as the default instance. No per-call options.
- **`formatter`**, **`generator`**, **`validator`**: Properties with getters and setters for the internal formatter, generator, and validator. Setters accept the same shapes as the constructor. To change a single option without replacing the instance, mutate the component's options (e.g. `utils.formatter.options.hidden = True`).

Instance defaults and per-call overrides:

```python
utils = CpfUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True},
)

cpf = '12345678909'

utils.format(cpf)                 # masked (instance formatter defaults)
utils.format(cpf, hidden=False)   # this call only: unmasked
utils.generate(format=False)      # this call only: compact output
```

Options can also be passed as a mapping on each method:

```python
utils.format(cpf, {'dot_key': '|'})
utils.generate({'prefix': '123456', 'format': True})
```

### Using the underlying helpers and classes

You can use the re-exported formatter, generator, and validator directly:

```python
from cpf_utils import (
    cpf_fmt,
    CpfFormatter,
    cpf_gen,
    CpfGenerator,
    cpf_val,
    CpfValidator,
)

cpf_fmt('47844241055', dash_key='_')   # '478.442.410_55'
cpf_gen(prefix='123456')               # e.g. '12345678901'
cpf_val('123.456.789-09')              # True

formatter = CpfFormatter({'hidden': True})
formatter.format('47844241055')        # '478.***.***-**'
```

See [`cpf-fmt`](./../cpf-fmt/README.md), [`cpf-gen`](./../cpf-gen/README.md), and [`cpf-val`](./../cpf-val/README.md) for full option and error details.

## API

### Exports

- **`cpf_utils`**: Pre-built `CpfUtils` instance with `format`, `generate`, and `is_valid`.
- **`CpfUtils`**: Class to create a utils instance with optional default formatter, generator, and validator settings.
- **Formatter**: `cpf_fmt`, `CpfFormatter`, `CpfFormatterOptions`, and formatter exceptions (see [cpf-fmt](./../cpf-fmt/README.md)).
- **Generator**: `cpf_gen`, `CpfGenerator`, `CpfGeneratorOptions`, and generator exceptions (see [cpf-gen](./../cpf-gen/README.md)).
- **Validator**: `cpf_val`, `CpfValidator`, and validator exceptions (see [cpf-val](./../cpf-val/README.md)).

### Errors & Exceptions

`CpfUtils` does not define its own exception types; it propagates errors from the bundled packages:

- **Formatting**: `CpfFormatterInputTypeError`, `CpfFormatterOptionsTypeError`, `CpfFormatterOptionsHiddenRangeInvalidException`, `CpfFormatterOptionsForbiddenKeyCharacterException`, and related classes.
- **Generation**: `CpfGeneratorOptionsTypeError`, `CpfGeneratorOptionPrefixInvalidException`, and related classes.
- **Validation**: `CpfValidatorInputTypeError` and related classes.

Invalid option types are **`TypeError`** subclasses; invalid option values are **`Exception`** subclasses. Validation failure returns `False`; formatting length failure is handled by **`on_fail`** (default returns an empty string).

```python
from cpf_utils import CpfUtils, cpf_fmt
from cpf_fmt import CpfFormatterInputTypeError
from cpf_val import CpfValidatorInputTypeError

try:
    CpfUtils().format(12345)
except CpfFormatterInputTypeError as e:
    print(e)

try:
    CpfUtils().is_valid(12345678909)
except CpfValidatorInputTypeError as e:
    print(e)

# Custom on_fail for invalid length
def custom_fail(value, exception=None):
    return f'Invalid CPF: {value}'

cpf_fmt('123', on_fail=custom_fail)  # 'Invalid CPF: 123'
cpf_fmt('123')                       # '' (default on_fail)
```

### Bundled packages

| Package | Main resources | README |
|---------|----------------|--------|
| [`cpf-fmt`](https://pypi.org/project/cpf-fmt) | `CpfFormatter`, `CpfFormatterOptions`, `cpf_fmt()` | [docs](./../cpf-fmt/README.md) |
| [`cpf-gen`](https://pypi.org/project/cpf-gen) | `CpfGenerator`, `CpfGeneratorOptions`, `cpf_gen()` | [docs](./../cpf-gen/README.md) |
| [`cpf-val`](https://pypi.org/project/cpf-val) | `CpfValidator`, `cpf_val()` | [docs](./../cpf-val/README.md) |

All of the above are pulled in as dependencies of **`cpf-utils`**. For exhaustive option tables, exception lists, and edge-case behavior, see each package README.

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
