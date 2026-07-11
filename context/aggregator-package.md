---
id: aggregator-package
title: Aggregator package implementation
scope: packages/cpf-utils/src/, packages/cnpj-utils/src/, packages/br-utilities/src/
triggers:
  - implementing or changing an aggregator package
  - adding a method or option to CpfUtils, CnpjUtils, or BrUtils
  - reviewing aggregator src/ structure
  - updating cpf-utils or cnpj-utils after a sub-package API change
---

# aggregator-package

Implement and maintain the three aggregator packages (`cpf-utils`, `cnpj-utils`, `br-utilities`) that bundle leaf packages into a unified API. All paths are relative to the repo root.

## Repository constraints

- Aggregator packages are **thin wrappers** — they delegate to leaf-package instances and add no new business logic.
- Aggregators depend on leaf packages via their published PyPI versions; leaf packages must not depend on aggregators (see [`context/dependencies.md`](dependencies.md)).
- Aggregator specs import from the leaf-package namespaces (`from cnpj_fmt import ...`).

## `src/` layout

### Domain aggregator (`cnpj-utils`)

```
src/cnpj_utils/
  __init__.py          # exports CnpjUtils + a default cnpj_utils singleton
  cnpj_utils.py        # CnpjUtils façade delegating to CnpjFormatter/Generator/Validator
```

### Top aggregator (`br-utilities`)

```
src/br_utils/
  __init__.py          # exports BrUtils + default br_utils singleton; re-exports cpf/cnpj surfaces
  br_utils.py          # BrUtils façade exposing .cpf and .cnpj
  cnpj/__init__.py     # re-exports the full cnpj surface (CnpjUtils, cnpj_utils, classes, options, exceptions)
  cpf/__init__.py      # re-exports the full cpf surface
```

## Constructor pattern

The façade accepts **keyword-only** components. Each component may be omitted (defaults used), or passed as an instance, an `*Options` instance, or a plain `Mapping` of options:

```python
class CnpjUtils:
    __slots__ = ("_formatter", "_generator", "_validator")

    def __init__(
        self,
        *,
        formatter: CnpjFormatter | CnpjFormatterOptions | CnpjFormatterOptionsInput | None = None,
        generator: CnpjGenerator | CnpjGeneratorOptions | CnpjGeneratorOptionsInput | None = None,
        validator: CnpjValidator | CnpjValidatorOptions | CnpjValidatorOptionsInput | None = None,
    ) -> None:
        self._formatter = self._resolve_formatter(formatter)
        self._generator = self._resolve_generator(generator)
        self._validator = self._resolve_validator(validator)
```

Each `_resolve_*` static method normalizes the input: pass through an existing component instance, construct from an `*Options` instance or `Mapping`, or build a default when `None`.

`BrUtils` composes the two domain aggregators and additionally accepts flattened per-component kwargs (`cpf_formatter`, `cnpj_validator`, …) plus whole-domain `cpf` / `cnpj` overrides.

## Properties and setters

Expose each component as a property with a setter that **fully replaces** the component (re-running the same `_resolve_*` logic). Document in the docstring that the setter resets the whole component, and that to tweak a single option the caller should mutate the live instance (e.g. `utils.formatter.options.hidden = True`).

## Default singletons

Each aggregator `__init__.py` exposes a ready-to-use default instance:

```python
cnpj_utils = CnpjUtils()
"""Default CnpjUtils instance with default component options."""
```

`br-utilities` exposes `br_utils = BrUtils()`.

## Delegating methods

Each façade method forwards directly to the corresponding component, threading through per-call options and keyword overrides. Do **not** add business logic:

```python
def is_valid(self, cnpj_input, options=None, *, case_sensitive=None, type=None) -> bool:
    validator_kwargs = _validator_forward_kwargs(case_sensitive=case_sensitive, type=type)
    if options is not None:
        return self._validator.is_valid(cnpj_input, options, **validator_kwargs)
    if validator_kwargs:
        return self._validator.is_valid(cnpj_input, **validator_kwargs)
    return self._validator.is_valid(cnpj_input)
```

## Docstrings on the façade

The constructor and delegating methods must list every exception that the composed components can raise in their `Raises:` sections (see [`context/docstrings.md`](docstrings.md)). Aggregate the union of the leaf packages' failure modes.

## Aggregator cascade after a leaf API change

When a leaf package gains a new option, method, or exception:

1. Add or thread the new option through the façade constructor / method kwargs.
2. Extend the `Raises:` docstring sections for any new exceptions.
3. Add a delegation method if the leaf gains a new method.
4. Re-export any new public symbol from the aggregator's `__init__.py` and `__all__` (and, for `br-utilities`, from `cpf/__init__.py` or `cnpj/__init__.py`).
5. Update the aggregator's `README.md` options table.
6. Add a CHANGELOG entry per [`context/changelogs.md`](changelogs.md), including an `Updated dependencies` group.

## Checklist

- [ ] Façade constructor accepts instance / `*Options` / `Mapping` / `None` per component (keyword-only)
- [ ] All delegation methods call component methods directly (no added logic)
- [ ] Property setters fully re-resolve their component
- [ ] Default singleton exported from `__init__.py`
- [ ] Docstrings list every `Raises:` from all composed components
- [ ] New leaf symbols re-exported through the aggregator (and `br_utils.cpf` / `br_utils.cnpj`)
- [ ] CHANGELOG entry added if public API changed
- [ ] README options table reflects component option changes
- [ ] Specs validate delegation behavior

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Canonical file |
|---------|---------------|
| Domain aggregator class | `packages/cnpj-utils/src/cnpj_utils/cnpj_utils.py` |
| Top aggregator façade | `packages/br-utilities/src/br_utils/br_utils.py` |
| Top aggregator re-exports | `packages/br-utilities/src/br_utils/__init__.py`, `cnpj/__init__.py`, `cpf/__init__.py` |
