---
id: docstrings
title: Docstring conventions
scope: packages/*/src/**/*.py
triggers:
  - adding or updating docstrings
  - documenting a new class, function, method, or constant
  - reviewing docstrings on a changed API
  - adding Raises, Args, or Returns sections
---

# docstrings

Write and maintain docstrings for all exported and internal API symbols across br-utils-py packages. All paths are relative to the repo root.

## Repository constraints

- **All public symbols get docstrings** — modules, exported classes, methods, functions, constants, and exception classes.
- Follow **PEP 257**. Use one-line summaries where sufficient; multi-line docstrings with a summary line, blank line, then body.
- Do **not** narrate implementation steps or restate what the code obviously does. Document intent, behavior, constraints, and what can go wrong.
- Tone: concise and user-facing, as if writing PyPI package documentation.
- Follow the reference implementations: `packages/cnpj-gen/src/cnpj_gen/cnpj_generator.py`, `cnpj_generator_options.py`, `exceptions.py`, `types.py`.

## Before writing docstrings

1. Read the symbol's source and any related options and exceptions modules.
2. Identify: what it does, what can go wrong (exceptions raised or `on_fail` invoked), what options control behavior.
3. Skim docstrings in sibling modules in the same package — match style and verbosity.

## Module docstrings

Every source module starts with a one-line (or short) module docstring:

```python
"""Generator for CNPJ (Cadastro Nacional da Pessoa Jurídica) identifiers."""
```

## Class docstrings

```python
class CnpjGenerator:
    """Generator for CNPJ identifiers.

    Builds valid 14-character CNPJ values by combining an optional
    ``prefix`` with a randomly generated sequence and computed check
    digits. Options control ``prefix``, character ``type``, and whether
    the result is formatted (``00.000.000/0000-00``).
    """
```

### Rules

- One-sentence summary line; add a paragraph only when constraints or usage notes are needed.
- Wrap identifiers, option names, and literal values in double backticks (``` ``prefix`` ```), the reStructuredText convention used across the repo.
- Use Sphinx cross-references for other symbols: `` :class:`CnpjGeneratorOptions` ``, `` :meth:`generate` ``, `` :data:`~cnpj_gen.types.CnpjType` ``, `` :mod:`br_utils.cpf` ``.

## Method and function docstrings

Describe behavior, not implementation. Document per-call merge semantics, side effects, and every failure mode.

```python
def generate(self, options: CnpjGeneratorOptionsInput | None = None) -> str:
    """Generate a valid CNPJ value.

    Builds a 14-character CNPJ from the configured ``prefix`` (if any), a
    random sequence of the configured character ``type``, and two computed
    check digits. If ``format`` is enabled, the result is returned as
    ``00.000.000/0000-00``.

    Per-call options are merged over the instance default options for this
    call only; the instance defaults are unchanged.

    Raises:
        ``CnpjGeneratorOptionsTypeError``: If any option has an invalid type.
        ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix`` option
            contains an invalid combination of characters.
    """
```

### Section conventions

- Use a **`Raises:`** section listing every exception that can propagate, each led by the backtick-quoted concrete class name and a colon, then a one-clause trigger condition. This is the most important section — never omit it when the symbol can fail.
- Use **`Args:`** / **`Returns:`** (Google style) only when the parameter name and type hint are not self-explanatory or the return value is non-obvious. Do not repeat the type annotation in prose.
- Use **`Examples:`** with doctest-style `>>>` blocks for foundation helpers (see `describe_type`) where a concrete example clarifies output.
- Use a **`See Also:`** section only when it genuinely aids navigation (e.g. a helper pointing to its class).

## Attribute docstrings on constants and defaults

Document module constants and option defaults with a PEP 257 attribute docstring — a string literal immediately **after** the assignment:

```python
CNPJ_LENGTH = 14
"""The standard length of a CNPJ identifier (14 alphanumeric characters)."""


class CnpjGeneratorOptions:
    DEFAULT_FORMAT = False
    """Default value for the ``format`` option.

    When ``True``, the generated CNPJ string uses the standard formatting
    (``00.000.000/0000-00``).
    """
```

> Do not use the deprecated `check-docstring-first` pattern expectation — attribute docstrings after `CONST = ...` are intentional and the pre-commit config explicitly allows them.

## Exception class docstrings

```python
class CnpjGeneratorTypeError(TypeError):
    """Base error for all ``cnpj-gen`` type-related errors.

    Extends the builtin :class:`TypeError`. Stores ``actual_input``,
    ``actual_type``, and ``expected_type``.
    """


class CnpjGeneratorOptionPrefixInvalidException(CnpjGeneratorException):
    """Exception raised when the ``prefix`` option is invalid.

    Carries ``actual_input`` and ``reason``.
    """
```

Base classes explain the inheritance and which builtin they extend. Concrete subclasses document the specific failure they capture and the structured attributes they expose.

## Type alias and TypedDict docstrings

`Literal` aliases and `TypedDict` shapes in `types.py` get attribute docstrings; document each `TypedDict` field in the class docstring's `Attributes:` section:

```python
CnpjType = Literal["alphanumeric", "alphabetic", "numeric"]
"""Character type for the generated CNPJ sequence."""


class CnpjGeneratorOptionsType(TypedDict):
    """Resolved options used internally.

    Attributes:
        ``format``: Whether to format the CNPJ as ``00.000.000/0000-00``.
        ``prefix``: Partial start string (0–12 alphanumeric characters).
        ``type``: Character set for randomly generated segments.
    """

    format: bool
    prefix: str
    type: CnpjType
```

## What not to document

- Do not add `Args:` for every parameter when the name and type hint are self-explanatory.
- Do not add `Returns:` for trivial getters whose return type is clear.
- Do not repeat the type annotation in words.
- Do not narrate obvious code.

## Checklist

- [ ] Every source module has a module docstring
- [ ] Every exported class, method, and function has a docstring
- [ ] `Raises:` lists every propagating exception with concrete class name + trigger
- [ ] `on_fail`-based failures (Fmt / Val) are mentioned where relevant
- [ ] Constants and `DEFAULT_*` values have attribute docstrings
- [ ] `Literal` / `TypedDict` / `TypeAlias` definitions documented
- [ ] Identifiers use double-backtick reST style; cross-refs use `:class:` / `:meth:` / `:data:`
- [ ] No narration of obvious code

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Canonical example |
|---------|-------------------|
| Class + method docstrings | `packages/cnpj-gen/src/cnpj_gen/cnpj_generator.py` |
| Options class with attribute docstrings | `packages/cnpj-gen/src/cnpj_gen/cnpj_generator_options.py` |
| Exception hierarchy docstrings | `packages/cnpj-gen/src/cnpj_gen/exceptions.py` |
| Type aliases + TypedDict | `packages/cnpj-gen/src/cnpj_gen/types.py` |
| Doctest examples | `packages/utils/src/lacus/utils/describe_type.py` |
