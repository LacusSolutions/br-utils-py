---
id: dependencies
title: Dependency policy
scope: packages/*/pyproject.toml, requirements-dev.txt
triggers:
  - adding a new PyPI dependency
  - adding a dev dependency or changing requirements-dev.txt
  - changing runtime dependency constraints
  - deciding whether a dependency is allowed
  - exploring the internal dependency graph
  - identifying downstream packages affected by a dep change
---

# dependencies

Manage dependencies in the br-utils-py monorepo following the rules below. All paths are relative to the repo root.

## Repository constraints

### Hard rules

- **Always ask the developer** before adding any new runtime or dev dependency to any package or the root. Do not assume approval is implied by any task description.
- Follow the strict **dependency direction** — upstream packages must not depend on downstream ones:

```
utils → {cpf,cnpj}-dv → {cpf,cnpj}-{fmt,gen,val} → {cpf,cnpj}-utils → br-utilities
```

Reverse edges (e.g. `utils` importing from `cnpj-fmt`) are forbidden.

- Shared dev tooling lives in the root `requirements-dev.txt` — do not add per-package dev dependencies. Each package's `pyproject.toml` `dependencies` lists only its **runtime** deps.
- Internal dependencies reference **published PyPI versions**, not path/editable references. (The `python require` helper installs them editable locally, but the declared constraint targets the published distribution.)

### When developer approval is NOT needed

Bumping an **already-declared internal dependency** to a new published range that mirrors what a sibling package uses (e.g. raising `cnpj-dv>=2.0.0,<2.1.0` to `>=2.1.0,<2.2.0` across packages) is safe to replicate without explicit approval. Verify the existing declaration before updating.

## Before changing dependencies

1. Check the target package `pyproject.toml` `[project].dependencies`.
2. Check `requirements-dev.txt` to confirm shared dev tooling is not already available.
3. Identify downstream packages affected by an internal dep bump (see [Inspecting internal dependencies](#inspecting-internal-dependencies)).
4. Confirm the proposed edge respects [dependency direction](#dependency-direction-reference).
5. If approval is needed, stop and ask — do not speculatively add the dependency.

## Inspecting internal dependencies

`scripts/discover.py` builds the internal `<dist> → folder` graph from each `pyproject.toml` `dependencies` list and topologically sorts packages. The build/lint/test/require commands use it to install and process packages in dependency order. To inspect the closure of a package (the package plus its internal deps in topological order), the resolver is exposed via `get_dependency_closure()` / `get_sorted_packages()` in `scripts/discover.py`; `python require <pkg>` installs exactly that closure.

```bash
python require              # install dev tools + every package (editable), in dependency order
python require cnpj-utils   # install dev tools + cnpj-utils and its internal deps only
python require --dev-only   # dev tools only
```

## Internal dependencies (PyPI versioning)

Python packages depend on each other via published PyPI version constraints in `pyproject.toml`:

```toml
[project]
dependencies = [
  "cnpj-dv>=2.0.0,<2.1.0",
  "lacus.utils>=1.0.0,<2.0.0",
]
```

### Version constraint convention

- **BR Utils monorepo packages** (`cpf-*`, `cnpj-*`, `br-utilities`): pin to a single minor line — `>=X.Y.0,<X.(Y+1).0` — allowing only patch updates. This prevents unexpected minor-version features from propagating between packages without an explicit constraint bump and changelog visibility.
- **`lacus.utils`** (standalone foundation package with its own roadmap): allow the whole major line — `>=X.Y.0,<(X+1).0.0` — so bug fixes and new features are adopted while excluding major versions.

When bumping a monorepo internal dependency, look up the latest published tag:

```bash
cd python && git tag -l '<dist-name>@*' | grep -vE '(rc|beta|alpha|dev)' | sort -V | tail -n 1
```

Strip the `<dist-name>@` prefix (e.g. `2.0.3`) and write the new pinned range.

## Dependency direction reference

| Package | Allowed upstream deps |
|---------|----------------------|
| `utils` | (none — foundation) |
| `{cpf,cnpj}-dv` | `lacus.utils` |
| `{cpf,cnpj}-{fmt,gen,val}` | `lacus.utils`, same-domain `-dv` |
| `{cpf,cnpj}-utils` | all same-domain leaf packages |
| `br-utilities` | `cpf-utils`, `cnpj-utils` (and by extension all leaves) |

## Root dev tooling (`requirements-dev.txt`)

Shared dev tooling used across all packages: `ruff`, `black`, `pytest`, `pytest-describe`, `pytest-cov`, `coverage`, `pre-commit`, `build`, `setuptools`, `wheel`, `twine`, `python-dotenv`, and `tomli` (only for Python < 3.11). Do not duplicate these into package `pyproject.toml` files.

## Changelog

Adding or bumping a runtime constraint in `[project].dependencies` is user-facing and requires a CHANGELOG entry (see [`context/changelogs.md`](changelogs.md)). Changing `requirements-dev.txt` or `[tool.*]`/dev-only config does not.

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Path |
|---------|------|
| Internal dependency resolver | `scripts/discover.py` |
| Dependency closure install | `python require [pkg]` |
| Root dev tooling | `requirements-dev.txt` |
| Package runtime deps | `packages/<pkg>/pyproject.toml` `[project].dependencies` |
| Canonical package config | `packages/cnpj-gen/pyproject.toml` |
