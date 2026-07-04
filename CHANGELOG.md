# cnpj-utils

## 2.0.2

### Patch Changes

- Updated dependencies
  - `cnpj-fmt`: 2.0.1 → 2.0.2
  - `cnpj-gen`: 2.0.2 → 2.0.3
  - `cnpj-val`: 2.0.1 → 2.0.2

## 2.0.1

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.

### Patch Changes

- Updated dependencies
  - `cnpj-fmt`: 2.0.0 → 2.0.1
  - `cnpj-gen`: 2.0.1 → 2.0.2
  - `cnpj-val`: 2.0.0 → 2.0.1

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — Full support for the [14-character alphanumeric CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2023/julho/cnpj-alfa-numerico); `format()`, `generate()`, and `is_valid()` handle numeric and alphanumeric IDs via upgraded `cnpj-fmt`, `cnpj-gen`, and `cnpj-val` v2 dependencies.
- ⚙️ **Validator options** — New `CnpjValidatorOptions`; configure `type` and `case_sensitive` on the `CnpjUtils` or `CnpjValidator` constructor, or per `is_valid()` call.
- 🔧 **Component setters** — Replace `formatter`, `generator`, and `validator` on a `CnpjUtils` instance (component instance, `*Options`, or mapping).
- 📦 **Full re-exports** — Component classes, `*Options`, typed exceptions, and `cnpj_fmt` / `cnpj_gen` / `cnpj_val` helpers from bundled v2 packages.

### BREAKING CHANGES

- **Keyword-only constructor** — `CnpjUtils` parameters are keyword-only (`formatter`, `generator`, `validator`); positional `CnpjFormatterOptions` / `CnpjGeneratorOptions` arguments no longer work.
- **Dependencies** — Requires `cnpj-fmt`, `cnpj-gen`, and `cnpj-val` v2; upgrade the CNPJ stack together (`cnpj-dv` 2.x for alphanumeric check digits).
- **Legacy aliases** — Removed `CnpjFormatterError`, `CnpjGeneratorError`, and related alias names; use the `*Exception` types from bundled components.
- **Default generation** — `generate()` returns alphanumeric CNPJ by default; pass `type="numeric"` for numeric-only output.
- **Method signatures** — `format()`, `generate()`, and `is_valid()` accept an optional options object plus keyword overrides instead of v1 positional option parameters; `format()` and `is_valid()` accept `str | Sequence[str]`.
- **Invalid input in `is_valid()`** — Non-string input raises `CnpjValidatorInputTypeError` instead of returning `False`.

### New features

- **`encode` option** — `format()` can URL-encode the formatted CNPJ (from `cnpj-fmt` v2).
- **`type` generation modes** — `generate()` supports `numeric`, `alphabetic`, and `alphanumeric` output via the `type` option.

### Improvements

- **`CnpjUtils` API** — Constructor and façade methods forward v2 options objects and per-call keyword overrides without mutating instance defaults.

## 1.0.2

### Patch Changes

- Updated dependencies
  - `cnpj-gen`: 1.0.1 → 1.0.2
  - `cnpj-val`: 1.0.1 → 1.0.2

## 1.0.1

### Patch Changes

- 12cd360: Fix documentation hero image source.
- Updated dependencies
  - `cnpj-gen`: 1.0.0 → 1.0.1
  - `cnpj-val`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Unified toolkit to deal with CNPJ data (Brazilian legal entity ID): validation, formatting, and generation of valid IDs. Main features:

- **Unified interface**: single `CnpjUtils` class combining formatter, generator, and validator
- **Multiple paradigms**: supports both class-based (`CnpjUtils`) and function-based (`cnpj_fmt`, `cnpj_gen`, `cnpj_val`) usage
- **Configurable options**: formatter and generator accept customizable options via constructor or method calls
- **Component access**: individual formatter, generator, and validator instances accessible for direct use
- **Default instance**: pre-configured `cnpj_utils` instance available for immediate use
- **Re-exports**: all classes, functions, and exceptions from underlying packages available from a single import

For detailed usage and API reference, see the [README](./README.md).
