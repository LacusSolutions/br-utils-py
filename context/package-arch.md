---
id: package-arch
title: Package implementation architecture
scope: packages/*/src/**/*.py
triggers:
  - implementing or changing package source code
  - adding a new class, exception, or option
  - designing or reviewing src/ layout
  - adding error handling (raising vs on_fail)
  - changing or adding snake_case helper functions
  - working on the exceptions or types modules
---

# package-arch

Follow the repeatable implementation architecture when adding or changing source code in any `packages/*` package. All paths are relative to the repo root.

## Single generation

Unlike the sibling PHP subrepo, the Python monorepo has **one current generation** — CPF and CNPJ are symmetric modern implementations. There is no legacy pattern to avoid. Use the CNPJ packages as the canonical reference for every archetype.

## Package archetypes

| Archetype | Examples | Role |
|-----------|----------|------|
| **DV** (check digits) | `cpf-dv`, `cnpj-dv` | Main class only; no helper function |
| **Val** (validator) | `cpf-val`, `cnpj-val` | Main class + snake_case helper + Options |
| **Fmt** (formatter) | `cpf-fmt`, `cnpj-fmt` | Main class + snake_case helper + Options |
| **Gen** (generator) | `cpf-gen`, `cnpj-gen` | Main class + snake_case helper + Options |
| **Foundation** | `utils` | Named functions/classes only; no aggregator |
| **Aggregator** | `cpf-utils`, `cnpj-utils`, `br-utilities` | Facade class wrapping leaf packages |

## Import namespaces

Source lives under `src/<import_namespace>/`. The import namespace equals the PyPI distribution name for most packages; two folders differ:

| Folder | PyPI name | Import namespace | `src/` path |
|--------|-----------|------------------|-------------|
| `cnpj-gen` (and most) | `cnpj-gen` | `cnpj_gen` | `src/cnpj_gen/` |
| `utils` | `lacus.utils` | `lacus.utils` | `src/lacus/utils/` |
| `br-utilities` | `br-utilities` | `br_utils` | `src/br_utils/` |

## Canonical `src/` layout

### DV

```
src/<ns>/
  __init__.py                  # exports + __version__
  <domain>_check_digits.py     # Main class + LENGTH constants
  exceptions.py                # Exception hierarchy
  types.py                     # Type aliases (e.g. CnpjInput)
```

### Val / Fmt / Gen

```
src/<ns>/
  __init__.py                  # exports + __version__
  <domain>_<role>.py           # Main class  (e.g. cnpj_generator.py → CnpjGenerator)
  <domain>_<role>_options.py   # Options class + DEFAULT_* + LENGTH constants
  <ns>.py                      # snake_case helper (e.g. cnpj_gen.py → cnpj_gen())
  exceptions.py                # Exception hierarchy
  types.py                     # Type aliases, Literals, TypedDicts
```

> A package with no configurable options omits the `<domain>_<role>_options.py` module (and its `DEFAULT_*` constants). `cpf-val` is the current example — the CPF validator takes no options, unlike `cnpj-val`. See [`context/domain-parity.md`](domain-parity.md#intentional-divergences-not-bugs).

### Foundation (`utils`)

```
src/lacus/utils/
  __init__.py
  describe_type.py
  generate_random_sequence.py
  types.py
```

### Aggregator (`cnpj-utils`)

```
src/cnpj_utils/
  __init__.py                  # exports CnpjUtils + cnpj_utils singleton
  cnpj_utils.py                # Façade class delegating to CnpjFormatter/Generator/Validator
```

`br-utilities` wraps both domains:

```
src/br_utils/
  __init__.py                  # exports BrUtils + br_utils singleton, re-exports cpf/cnpj
  br_utils.py                  # BrUtils façade
  cnpj/__init__.py             # re-exports CnpjUtils, cnpj_utils
  cpf/__init__.py              # re-exports CpfUtils, cpf_utils
```

## Public exports (`__init__.py`)

Every package exposes its public API from `__init__.py` with an explicit `__all__` (sorted) and a module-level `__version__` string. Ruff ignores `F401` (unused import) in `__init__.py` — re-exports are intentional.

```python
from .cnpj_gen import cnpj_gen
from .cnpj_generator import CnpjGenerator
from .cnpj_generator_options import CNPJ_LENGTH, CnpjGeneratorOptions
from .exceptions import CnpjGeneratorException, CnpjGeneratorTypeError
from .types import CnpjGeneratorOptionsInput, CnpjType

__all__ = [
    "CNPJ_LENGTH",
    "CnpjGenerator",
    "CnpjGeneratorException",
    "CnpjGeneratorOptions",
    "CnpjGeneratorOptionsInput",
    "CnpjGeneratorTypeError",
    "CnpjType",
    "cnpj_gen",
]

__version__ = "0.0.0"
```

The `__version__` placeholder stays `"0.0.0"` in source; the real version is injected at build time (see [`context/packaging.md`](packaging.md)).

## Main class pattern

- Use `__slots__` on service classes with fixed attributes (generators, formatters, validators, domain utils).
- Accept an optional first positional `options` argument (an options instance, a `Mapping`, or `None`) plus keyword-only per-option overrides.
- Expose an `options` property returning the internal options instance; mutating it affects future calls that omit per-call options.
- Use `from __future__ import annotations` and guard type-only imports under `TYPE_CHECKING`.

```python
class CnpjGenerator:
    __slots__ = ("_options",)

    def __init__(
        self,
        options: CnpjGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
        type: CnpjType | None = None,
    ) -> None:
        if isinstance(options, CnpjGeneratorOptions):
            self._options = options
        else:
            self._options = CnpjGeneratorOptions(options, format=format, prefix=prefix, type=type)
```

## snake_case helper pattern (Val / Fmt / Gen)

Each leaf package ships a one-shot helper named after the package (`cnpj_gen`, `cnpj_fmt`, `cnpj_val`) that constructs the class and calls its single action:

```python
def cnpj_gen(
    options: CnpjGeneratorOptionsInput = None,
    *,
    format: bool | None = None,
    prefix: str | None = None,
    type: CnpjType | None = None,
) -> str:
    return CnpjGenerator(options, format=format, prefix=prefix, type=type).generate()
```

Rationale: the helper is a stateless call-once API; the class is a stateful, reusable, configurable API. Both are first-class entry points.

## Options class pattern (Fmt / Gen / Val)

Options are **regular classes with property setters — not dataclasses**.

- Defaults live as class attributes `DEFAULT_<OPTION>` with attribute docstrings.
- The constructor accepts a single options mapping/instance, `*extra_overrides` merged in order, and keyword-only per-option values.
- Each option is a `@property` with a validating `@setter`. Setters coerce `None` to the default, validate the type (raise `*TypeError`), and validate the value (raise a domain `*Exception`).
- Expose an `all` property returning an immutable snapshot via `types.MappingProxyType`.
- Provide a `set(options)` method that updates only provided fields and returns `self`.

```python
class CnpjGeneratorOptions:
    DEFAULT_FORMAT = False
    """Default value for the ``format`` option."""

    @property
    def type(self) -> CnpjType:
        return self._options["type"]

    @type.setter
    def type(self, value: object | None) -> None:
        actual = CnpjGeneratorOptions.DEFAULT_TYPE if value is None else value
        if not isinstance(actual, str):
            raise CnpjGeneratorOptionsTypeError("type", actual, "str")
        if actual not in _CNPJ_TYPE_OPTIONS:
            raise CnpjGeneratorOptionTypeInvalidException(actual, _CNPJ_TYPE_OPTIONS_ORDER)
        self._options["type"] = actual
```

## Error handling: raise vs `on_fail`

The packages distinguish **errors** (wrong type) from **exceptions** (right type, invalid value / business-rule failure):

| Error category | Handling |
|----------------|---------|
| **Type errors** (wrong Python type passed) | Always `raise` a subclass of the package's `*TypeError` (which extends the builtin `TypeError`) |
| **Business-rule / value failures** (e.g. option out of range, invalid prefix) | `raise` a subclass of the package's `*Exception` (which extends the builtin `Exception`) |
| **Input length / normalization failure** (Fmt / Val) | Invoke the configured `on_fail` callback with `(value, exception)`; its return value is used as the result. The default `on_fail` returns an empty string and must never raise |

## `exceptions.py` structure

Each package defines two abstract-ish base classes plus concrete subclasses:

```python
class CnpjGeneratorTypeError(TypeError):
    """Base error for all cnpj-gen type-related errors."""

class CnpjGeneratorOptionsTypeError(CnpjGeneratorTypeError):
    """Raised when a generator option has an invalid type."""

class CnpjGeneratorException(Exception):
    """Base exception for all cnpj-gen rule-related failures."""

class CnpjGeneratorOptionPrefixInvalidException(CnpjGeneratorException):
    """Raised when the prefix option is invalid."""
```

Each concrete subclass covers one specific failure and stores structured attributes (`actual_input`, `actual_type`, `expected_type`, `reason`, `expected_values`, etc.) for callers to inspect. Do not collapse multiple failure cases into one exception class.

## `types.py`

Hold `Literal` sets, `TypedDict` resolved-option shapes, and `TypeAlias` input unions:

```python
CnpjType = Literal["alphanumeric", "alphabetic", "numeric"]

class CnpjGeneratorOptionsType(TypedDict):
    format: bool
    prefix: str
    type: CnpjType

CnpjGeneratorOptionsInput: TypeAlias = CnpjGeneratorOptions | Mapping[str, Any] | None
```

## Dependency direction

```
utils → {cpf,cnpj}-dv → {cpf,cnpj}-{fmt,gen,val} → {cpf,cnpj}-utils → br-utilities
```

Upstream packages must not import downstream ones. `utils` is a leaf with no internal deps. To inspect the live graph from `pyproject.toml` declarations, see [`context/dependencies.md`](dependencies.md#inspecting-internal-dependencies).

## Checklist

- [ ] `src/<ns>/` layout matches the archetype (DV / Val / Fmt / Gen / Foundation / Aggregator)
- [ ] `from __future__ import annotations` at the top; type-only imports under `TYPE_CHECKING`
- [ ] Public API exported from `__init__.py` with sorted `__all__` and `__version__ = "0.0.0"`
- [ ] `__slots__` on service classes with fixed attributes
- [ ] snake_case helper present for Val/Fmt/Gen; class is the primary entry point for DV
- [ ] Options are classes with property setters (not dataclasses); defaults as `DEFAULT_*` constants
- [ ] Type errors raise `*TypeError`; value failures raise `*Exception`; length/normalization failures use `on_fail`
- [ ] `exceptions.py` defines base + concrete subclasses with structured attributes
- [ ] `types.py` holds `Literal`/`TypedDict`/`TypeAlias` definitions
- [ ] Docstrings on all exported symbols per [`context/docstrings.md`](docstrings.md)
- [ ] Tests per [`context/unit-tests.md`](unit-tests.md)

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference packages

| Archetype | Canonical package | Key files |
|-----------|------------------|-----------|
| DV | `cnpj-dv` | `src/cnpj_dv/cnpj_check_digits.py`, `src/cnpj_dv/exceptions.py` |
| Fmt | `cnpj-fmt` | `src/cnpj_fmt/cnpj_formatter.py`, `..._options.py`, `cnpj_fmt.py` |
| Val | `cnpj-val` | `src/cnpj_val/cnpj_validator.py`, `..._options.py`, `types.py` |
| Gen | `cnpj-gen` | `src/cnpj_gen/cnpj_generator.py`, `..._options.py`, `cnpj_gen.py` |
| Foundation | `utils` | `src/lacus/utils/describe_type.py` |
| Aggregator | `cnpj-utils` | `src/cnpj_utils/cnpj_utils.py` |
| Top aggregator | `br-utilities` | `src/br_utils/br_utils.py`, `src/br_utils/cpf/`, `src/br_utils/cnpj/` |
