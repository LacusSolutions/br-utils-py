---
id: unit-tests
title: Package unit tests
scope: packages/*/tests/
triggers:
  - writing or updating unit tests
  - adding test coverage for new behavior
  - fixing failing tests
  - reviewing test changes
  - running package tests
---

# unit-tests

Write and maintain specs under `packages/<pkg>/tests/` using the established br-utils-py conventions. All paths are relative to the repo root.

## Repository constraints

### Runner and style

Tests use **pytest** with **pytest-describe** for BDD-style nesting. Do not add other test frameworks (unittest classes, nose, etc.).

Each package configures pytest in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "9.0"
addopts = [ "--import-mode=importlib" ]
testpaths = [ "tests/" ]
python_files = [ "*.spec.py" ]
python_functions = [ "describe_*", "it_*", "test_*" ]
```

### Location and naming

- Specs live in `tests/` at the package root (never under `src/`).
- Files use the `.spec.py` suffix.
- Name the file after the unit under test (e.g. `src/cnpj_gen/cnpj_generator.py` → `tests/cnpj_generator.spec.py`).
- Specs are organized by behavior, not as a 1:1 mirror of `src/`.
- A `tests/__init__.py` and `tests/conftest.py` may be present for shared fixtures/helpers.

### Imports

- Import from the installed package namespace (e.g. `from cnpj_gen import CnpjGenerator, CnpjGeneratorOptions`). Packages are installed editable via `python require`, so import by distribution namespace — not relative `../src` paths.
- Aggregator specs import from their sub-package namespaces (`from cnpj_fmt import ...`).

### Lint

Specs are linted with the package's other sources by `python run lint`. `tests/**/*.py` has the `ARG` (unused-argument) Ruff rule relaxed. Follow existing patterns in sibling spec files.

### Changelog

Test-only changes are **dev-only** — do not add a changelog entry for spec edits, coverage tooling, or test refactors with no user-facing change.

### Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

---

## Before writing tests

1. Check for `packages/<pkg>/AGENTS.md` and `packages/<pkg>/context/`; apply overrides when present.
2. Read the source file(s) under test and list public behaviors, options, and error paths.
3. Skim existing specs in `packages/<pkg>/tests/` — match structure, naming, and assertion style.
4. Identify the **package archetype** (below); only create or extend the spec files that archetype uses.

---

## Package archetypes

| Archetype | Examples | Typical spec files |
|-----------|----------|-------------------|
| **Foundation** | `utils` | One `*.spec.py` per `src/` module |
| **Single-purpose** | `cnpj-fmt`, `cnpj-val`, `cnpj-gen`, `cnpj-dv`, `cpf-*` | Main class spec, options spec, helper spec, `exceptions.spec.py` |
| **Aggregator** | `cnpj-utils`, `cpf-utils`, `br-utilities` | Aggregator class spec delegating to sub-packages |

## Spec file roles

| File pattern | Tests |
|--------------|-------|
| `<module>.spec.py` | Primary class from `src/<ns>/<module>.py` — constructor, methods, edge cases, `on_fail` |
| `<pkg-short>.spec.py` | snake_case helper (e.g. `cnpj_gen`) — delegates to the class; input/output contract |
| `<resource>_options.spec.py` | Options class — defaults, validation, setters, invalid inputs |
| `exceptions.spec.py` | Error and exception classes — inheritance, message, structured attributes |

---

## Structure and style (Better Specs / pytest-describe)

Use nested `describe_*` functions for context and `it_*` functions for individual behaviors:

```python
"""Behavioral spec for ``CnpjGenerator``."""

import pytest
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorOptionPrefixInvalidException,
)


def describe_cnpj_generator():
    def describe_generate():
        def it_returns_a_14_character_string():
            cnpj = CnpjGenerator().generate()

            assert isinstance(cnpj, str)
            assert len(cnpj) == 14

        def it_returns_a_formatted_string_when_format_is_true():
            cnpj = CnpjGenerator({"format": True}).generate()

            assert "." in cnpj
            assert "/" in cnpj

        def it_raises_when_prefix_is_invalid():
            with pytest.raises(CnpjGeneratorOptionPrefixInvalidException):
                CnpjGenerator({"prefix": "00000000"}).generate()
```

### Rules

- **`describe_*`** — component or context (class name, method name, or `when_<condition>`).
- **`it_*`** — one behavior per example; present-tense phrasing (`it_returns_...`, `it_raises_...`, `it_calls_on_fail_...`).
- **Nesting** — group by method, input type, or option; avoid flat lists of unrelated examples.
- **Arrange–act–assert** — keep each `it_*` focused.
- Use plain `test_*` functions only when the describe/it pattern does not fit (e.g. `pytest.mark.parametrize` tables). Module-level fixtures via `conftest.py`.

### Error and exception testing

Two patterns, matching the source's two-tier model (see [`context/package-arch.md`](package-arch.md#error-handling-raise-vs-on_fail)):

1. **Raised errors/exceptions** — assert the class and (optionally) structured attributes:

```python
def it_raises_when_type_is_invalid():
    with pytest.raises(CnpjGeneratorOptionsTypeError) as exc_info:
        CnpjGeneratorOptions(type=123)

    assert exc_info.value.expected_type == "str"
```

2. **`on_fail` callback** — pass a spy callback in the options and assert it is invoked (used by formatters/validators for length failures that do not raise by default):

```python
def it_calls_on_fail_when_length_is_invalid():
    calls = []
    CnpjFormatter(on_fail=lambda value, error: calls.append(error) or "").format("123")

    assert len(calls) == 1
```

### Cross-language alignment

The Python packages mirror the JS and PHP reference suites. Prefer extending existing reference-suite cases over inventing new ones; document any dropped or Python-specific cases in the module docstring.

---

## Running tests

From the **python/** repository root:

| Goal | Command |
|------|---------|
| All packages | `python run test` |
| Single package | `python run test cnpj-gen` |
| Quiet / verbose | `python run test -q cnpj-gen` / `python run test -v cnpj-gen` |
| Watch mode | `python run test -w cnpj-gen` |

From a package directory (`packages/<pkg>/`): `python run test` (delegates to the root CLI with the package name).

Optional local coverage from a package directory: `pytest --cov=src --cov-report=term-missing` (coverage tooling is available but not enforced in CI).

---

## Checklist for agents

- [ ] New behavior has at least one focused `it_*` in the appropriate `*.spec.py`.
- [ ] Error paths covered: type errors (`raise`), value failures (`raise`), length failures (`on_fail`), invalid options.
- [ ] Options spec covers defaults and all validation branches.
- [ ] `exceptions.spec.py` verifies inheritance chain, message, and structured attributes.
- [ ] Style matches siblings: nested `describe_*` / `it_*`, imports from the package namespace.
- [ ] `python run test <pkg>` passes.
- [ ] No new test frameworks or dependencies without developer approval.
