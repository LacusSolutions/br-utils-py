---
id: new-package
title: Scaffold a new package
scope: packages/
triggers:
  - adding a new package to the monorepo
  - scaffolding a new cpf-*, cnpj-*, or br-* package
  - creating a new workspace member
---

# new-package

Step-by-step checklist for adding a new package to the br-utils-py monorepo. Adding a package is a rare, high-blast-radius operation. All paths are relative to the repo root.

## Prerequisites

- **Developer approval is required** before adding any new package or dependency. Stop and confirm before starting. See [`context/dependencies.md`](dependencies.md).
- Identify the archetype (DV / Val / Fmt / Gen / Foundation / Aggregator) — this determines the `src/` layout. See [`context/package-arch.md`](package-arch.md).
- Identify the canonical sibling to clone from (table below).

## Clone-from table

| New package type | Clone from |
|-----------------|-----------|
| `{domain}-fmt` | `cnpj-fmt` |
| `{domain}-val` | `cnpj-val` |
| `{domain}-gen` | `cnpj-gen` |
| `{domain}-dv` | `cnpj-dv` |
| `{domain}-utils` (aggregator) | `cnpj-utils` |
| `br-*` (multi-domain aggregator) | `br-utilities` |
| Foundation utility | `utils` |

## Step 1 — Create the directory structure

The import namespace is the underscored distribution name (e.g. `cnpj-gen` → `cnpj_gen`); foundation uses `lacus/<pkg>` and a top aggregator uses its own namespace.

```
packages/<pkg>/
  src/<import_ns>/
    __init__.py
    <domain>_<role>.py          # main class (or <domain>_check_digits.py for DV)
    <domain>_<role>_options.py  # Val/Fmt/Gen only
    <import_ns>.py              # snake_case helper (Val/Fmt/Gen only)
    exceptions.py
    types.py
  tests/
    __init__.py
    conftest.py                 # if shared fixtures are needed
    <module>.spec.py
    exceptions.spec.py
  pyproject.toml
  run
  README.md
  README.pt.md
  CHANGELOG.md
  LICENSE
```

## Step 2 — `pyproject.toml`

Copy from the sibling package of the same archetype and update all package-specific fields (`name`, `description`, `keywords`, `dependencies`, dynamic-version `attr`). Follow [`context/packaging.md`](packaging.md) for the full anatomy. Ensure:

- `dynamic = ["version"]` and `[tool.setuptools.dynamic.version].attr = "<import_ns>.__version__"`.
- `requires-python = ">=3.10,<4.0"` and the Python 3.10–3.14 classifiers.
- `[tool.setuptools.packages.find].where = ["src/"]`.
- The pytest and coverage `[tool.*]` blocks copied verbatim.
- Runtime `dependencies` respect [dependency direction](dependencies.md#dependency-direction-reference).

## Step 3 — `run` script

Copy the sibling's `run` script and change only the `PACKAGE_NAME` constant. It routes `lint`/`test`/`build`/`clean`/`publish` to the monorepo root `run`.

## Step 4 — Implement `src/`

Follow [`context/package-arch.md`](package-arch.md):

- Choose the archetype layout (DV / Val / Fmt / Gen / Foundation / Aggregator).
- Implement the main class with `__slots__` and `from __future__ import annotations`.
- Write `exceptions.py` (base `*TypeError` + `*Exception` and concrete subclasses).
- Write the snake_case helper for Val/Fmt/Gen.
- Write `types.py` (`Literal`/`TypedDict`/`TypeAlias`).
- Export the public API from `__init__.py` with sorted `__all__` and `__version__ = "0.0.0"`.
- Add docstrings per [`context/docstrings.md`](docstrings.md).

## Step 5 — Add `tests/`

Follow [`context/unit-tests.md`](unit-tests.md): main class spec, options spec, helper spec, and `exceptions.spec.py`, using nested `describe_*` / `it_*`.

## Step 6 — Install and verify

```bash
python require <pkg>          # install the package + its internal deps (editable)
python run lint <pkg>
python run test <pkg>
python run build <pkg>        # smoke-build the wheel/sdist
```

CI discovers the package automatically once it has a `run` script and `tests/` directory (see [`context/ci-release.md`](ci-release.md)).

## Step 7 — README and CHANGELOG

- Write `README.md` and `README.pt.md` per [`context/readme-docs.md`](readme-docs.md).
- Create `CHANGELOG.md` with a `## 1.0.0` section (heading `# <dist-name>`) per [`context/changelogs.md`](changelogs.md).

## Final checklist

- [ ] Directory structure matches the archetype
- [ ] `pyproject.toml`: correct `name`, dynamic version `attr`, `requires-python`, `src/` find, pytest config
- [ ] `run` script present with correct `PACKAGE_NAME`
- [ ] `src/` implemented per `package-arch.md`; `__all__` + `__version__` in `__init__.py`
- [ ] `tests/` implemented per `unit-tests.md`
- [ ] Internal `dependencies` respect dependency direction
- [ ] `python require <pkg>` succeeds
- [ ] `python run lint <pkg>` passes
- [ ] `python run test <pkg>` passes
- [ ] `python run build <pkg>` succeeds
- [ ] `README.md` and `README.pt.md` written
- [ ] `CHANGELOG.md` created with initial `## 1.0.0` section
- [ ] Commit scope added to the conventional-commit scope list if the folder name is new (see root `AGENTS.md`)

## Package-level overrides

Before applying this harness, check whether a package-level `AGENTS.md` or `context/` directory was created for this package. If so, follow it over this file for any conflicting instructions (see [`context/README.md`](README.md#instruction-precedence)).
