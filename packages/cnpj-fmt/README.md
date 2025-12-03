![cnpj-fmt for Python](https://br-utils.vercel.app/img/cover_cnpj-fmt.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-fmt)](https://pypi.org/project/cnpj-fmt)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-fmt)](https://pypi.org/project/cnpj-fmt)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-fmt)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility function/class to format CNPJ (Brazilian employer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cnpj-fmt
```

## Import

```python
# Using class-based resource
from cnpj_fmt import CnpjFormatter

# Or using function-based one
from cnpj_fmt import cnpj_fmt
```

## Usage

### Object-Oriented Usage

```python
formatter = CnpjFormatter()
cnpj = '03603568000195'

print(formatter.format(cnpj))       # returns '03.603.568/0001-95'

# With options
print(formatter.format(
    cnpj,
    hidden=True,
    hidden_key='#',
    hidden_start=5,
    hidden_end=13
))  # returns '03.603.###/####-##'
```

The options can be provided to the constructor or the `format()` method. If passed to the constructor, the options will be attached to the `CnpjFormatter` instance. When passed to the `format()` method, it only applies the options to that specific call.

```python
cnpj = '03603568000195'
formatter = CnpjFormatter(hidden=True)

print(formatter.format(cnpj))                  # '03.603.***/****-**'
print(formatter.format(cnpj, hidden=False))    # '03.603.568/0001-95' merges the options to the instance's
print(formatter.format(cnpj))                  # '03.603.***/****-**' uses only the instance options
```

### Functional programming

The helper function `cnpj_fmt()` is just a functional abstraction. Internally it creates an instance of `CnpjFormatter` and calls the `format()` method right away.

```python
cnpj = '03603568000195'

print(cnpj_fmt(cnpj))       # returns '03.603.568/0001-95'

print(cnpj_fmt(cnpj, hidden=True))     # returns '03.603.***/****-**'

print(cnpj_fmt(cnpj, dot_key='', slash_key='|', dash_key='_'))     # returns '03603568|0001_95'
```

### Formatting Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `escape` | `bool \| None` | `False` | Whether to HTML escape the result |
| `hidden` | `bool \| None` | `False` | Whether to hide digits with a mask |
| `hidden_key` | `str \| None` | `'*'` | Character to replace hidden digits |
| `hidden_start` | `int \| None` | `5` | Starting index for hidden range (0-13) |
| `hidden_end` | `int \| None` | `13` | Ending index for hidden range (0-13) |
| `dot_key` | `str \| None` | `'.'` | String to replace dot characters |
| `slash_key` | `str \| None` | `'/'` | String to replace slash character |
| `dash_key` | `str \| None` | `'-'` | String to replace dash character |
| `on_fail` | `Callable \| None` | `lambda value, error=None: value` | Fallback function for invalid input |

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-fmt/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
