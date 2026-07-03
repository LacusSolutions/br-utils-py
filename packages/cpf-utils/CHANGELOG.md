# cpf-utils

## 2.0.0

### 🎉 v2 at a glance 🎊

- ⚙️ **Flexible formatter API** — `format()` accepts an options object plus keyword overrides; supports `encode` and `str | Sequence[str]` input via upgraded `cpf-fmt` v2.
- 🔧 **Component setters** — Replace `formatter`, `generator`, and `validator` on a `CpfUtils` instance (component instance, `*Options`, or mapping).
- 📦 **Full re-exports** — Component classes, `*Options`, typed exceptions, and `cpf_fmt` / `cpf_gen` / `cpf_val` helpers from bundled v2 components.

### BREAKING CHANGES

- **Keyword-only constructor** — `CpfUtils` parameters are keyword-only (`formatter`, `generator`, `validator`); positional `CpfFormatterOptions` / `CpfGeneratorOptions` arguments no longer work.
- **Dependencies** — Requires `cpf-fmt` and `cpf-gen` v2; upgrade the CPF stack together with this package.
- **Legacy aliases** — Removed `CpfFormatterError`, `CpfGeneratorError`, and related alias names; use the `*Exception` types from bundled components.
- **Method signatures** — `format()` and `generate()` accept an optional options object plus keyword overrides instead of v1 positional option parameters; `format()` accepts `str | Sequence[str]`.

### New features

- **`encode` option** — `format()` can URL-encode the formatted CPF (from `cpf-fmt` v2).

### Improvements

- **`CpfUtils` API** — Constructor and façade methods forward v2 options objects and per-call keyword overrides without mutating instance defaults.
- **requires-python** — Declares support for Python `>=3.10,<4.0`.

## 1.0.1

### Patch Changes

- Updated dependencies
  - `cpf-gen`: 1.0.0 → 1.0.1
  - `cpf-val`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Unified toolkit to deal with CPF data (Brazilian legal entity ID): validation, formatting, and generation of valid IDs. Main features:

- **Unified interface**: single `CpfUtils` class combining formatter, generator, and validator
- **Multiple paradigms**: supports both class-based (`CpfUtils`) and function-based (`cpf_fmt`, `cpf_gen`, `cpf_val`) usage
- **Configurable options**: formatter and generator accept customizable options via constructor or method calls
- **Component access**: individual formatter, generator, and validator instances accessible for direct use
- **Default instance**: pre-configured `cpf_utils` instance available for immediate use
- **Re-exports**: all classes, functions, and exceptions from underlying packages available from a single import

For detailed usage and API reference, see the [README](./README.md).
