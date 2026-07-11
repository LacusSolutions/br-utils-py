---
id: public-api
title: Public API change coordination
scope: packages/*/src/, packages/*/tests/, packages/*/README.md, packages/*/CHANGELOG.md
triggers:
  - adding, removing, or renaming a public class or function
  - changing a function, method, or constructor signature
  - adding or changing options or defaults
  - changing __all__ or a package's exported surface
  - behavior changes visible to package consumers
  - reviewing a PR that modifies the public API
---

# public-api

This is a meta-checklist harness. When a change touches the public API of any `packages/*` package, use this file as the coordination checklist — it ties together the specialized harnesses that each govern one artifact type. All paths are relative to the repo root.

## What counts as a public API change

A change is public-API if it affects anything a downstream PyPI consumer would observe:

- Adding, removing, or renaming an exported class, function, constant, `Literal`, or `TypedDict` in `__all__`
- Changing a method or function signature (parameter name, type, keyword-only-ness, order, default)
- Adding or removing an option from an options class, or changing an option's `DEFAULT_*`
- Changing raised exception types or their class hierarchy
- Changing the import namespace or moving a symbol between modules that alters the import path
- Changing `[project].dependencies`, `name`, or `requires-python` in `pyproject.toml`

Changes that are **not** public-API: specs, CI configs, private (`_`-prefixed) helpers, `[tool.*]` config, `requirements-dev.txt`, `.gitignore`.

## Coordinated artifacts checklist

For every public API change, work through the following in order:

| # | Artifact | Harness |
|---|----------|---------|
| 1 | Source (`src/`) changes + `exceptions.py` + `types.py` + `__all__` | [`context/package-arch.md`](package-arch.md) |
| 2 | Docstrings on all changed/new symbols | [`context/docstrings.md`](docstrings.md) |
| 3 | Behavior specs | [`context/unit-tests.md`](unit-tests.md) |
| 4 | README update (options table, usage example) | [`context/readme-docs.md`](readme-docs.md) |
| 5 | CHANGELOG entry | [`context/changelogs.md`](changelogs.md) |
| 6 | `pyproject.toml` `dependencies` / `requires-python` (if changed) | [`context/packaging.md`](packaging.md), [`context/dependencies.md`](dependencies.md) |
| 7 | Domain parity check (if `cpf-*` / `cnpj-*`) | [`context/domain-parity.md`](domain-parity.md) |
| 8 | Aggregator cascade (if a sub-package changed) | [`context/aggregator-package.md`](aggregator-package.md) |

> There is no separate "distribution test" step — the import contract is validated by importing from the package namespace in the behavior specs plus lint. When a symbol is added/removed, update the package's `__all__` and any spec that imports it.

## Decision flow

```
src/ change?
  │
  ├─ yes → always update behavior specs (step 3)
  │
  └─ export surface change? (new/removed/renamed symbol in __all__, moved module)
       │
       ├─ yes → update README (step 4) and __all__ (step 1)
       │
       └─ user-facing? (src/, pyproject runtime keys, public README)
            │
            ├─ yes → add CHANGELOG entry (step 5)
            │
            └─ dev-only (specs, CI, lint, dev deps) → skip CHANGELOG
```

## Before starting

1. Identify all packages affected (direct change + any aggregator that wraps the changed package).
2. For each affected package, run through the 8-step checklist above.
3. Do not mark a task complete until every artifact step is verified or explicitly skipped with a reason.

## Aggregator cascade

When changing a sub-package public API, check whether the aggregator wrapping it needs updating:

| Changed sub-package | Check aggregator |
|--------------------|-----------------|
| `cpf-{fmt,gen,val}` | `cpf-utils` re-exports + `CpfUtils` class |
| `cnpj-{fmt,gen,val}` | `cnpj-utils` re-exports + `CnpjUtils` class |
| `cpf-utils` or `cnpj-utils` | `br-utilities` (`br_utils.cpf` / `br_utils.cnpj`) |

If the aggregator does not yet expose a new symbol or delegate a new method/option, update its `src/` and `__all__`. See [`context/aggregator-package.md`](aggregator-package.md).

## Checklist

- [ ] All `src/` changes implemented per [`context/package-arch.md`](package-arch.md)
- [ ] `__all__` updated for added/removed exports
- [ ] Docstrings updated on all changed symbols per [`context/docstrings.md`](docstrings.md)
- [ ] Behavior specs added or updated in `tests/`
- [ ] README updated if an option, default, or public behavior changed
- [ ] CHANGELOG entry added unless the change is entirely dev-only
- [ ] `pyproject.toml` `dependencies` / `requires-python` updated if needed
- [ ] Domain parity check done if the change is in `cpf-*` or `cnpj-*`
- [ ] Aggregator packages updated if a new symbol needs re-exporting or delegating

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).
