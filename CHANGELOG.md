# br-utilities

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — `br_utils.cnpj` supports 14-character alphanumeric IDs via upgraded `cnpj-utils` v2.
- 🏗️ **`BrUtils` v2** — Constructor accepts `cpf`/`cnpj` instances or config mappings (including `cnpj_validator`); property setters swap utils after construction.
- 📦 **Full v2 re-exports** — `br_utils.cpf` and `br_utils.cnpj` expose the complete v2 component surface (classes, `*Options`, helpers, typed exceptions).

### BREAKING CHANGES

- **CPF re-exports** — Legacy `*Error` alias names removed; `br_utils.cpf` mirrors `cpf-utils` v2 (`*Exception` types, `encode`, keyword-only options, `str | Sequence[str]` input).
- **CNPJ re-exports** — Legacy `*Error` alias names removed; `br_utils.cnpj` mirrors `cnpj-utils` v2 (`CnpjValidatorOptions`, alphanumeric default generation, typed exceptions).
- **Dependencies** — Requires `cpf-utils` `>=2.0.0,<2.1.0` and `cnpj-utils` `>=2.0.2,<2.1.0`.

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.

## 1.0.1

### Patch Changes

- Updated dependencies
  - `cnpj-utils`: 1.0.1 → 1.0.2
  - `cpf-utils`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Unified toolkit to deal with Brazilian documents (CPF and CNPJ): validation, formatting, and generation of valid IDs. Main features:

- **All-in-one**: single `BrUtils` class combining CPF and CNPJ utilities
- **Unified interface**: consolidates `CpfUtils` and `CnpjUtils` in a single class
- **Configurable options**: CPF and CNPJ formatter/generator accept customizable options via constructor
- **Component access**: individual `cpf` and `cnpj` instances accessible for direct use
- **Default instance**: pre-configured `br_utils` instance available for immediate use
- **Re-exports**: all classes, functions, and exceptions from `cpf-utils` and `cnpj-utils` available from a single import

For detailed usage and API reference, see the [README](./README.md).
