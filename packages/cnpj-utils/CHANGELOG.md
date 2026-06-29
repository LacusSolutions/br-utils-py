# cnpj-utils

## 2.0.0

### BREAKING CHANGES

- **Dependencies** — Requires `cnpj-gen` 2.x for generation; upgrade the CNPJ stack (`cnpj-gen`, `cnpj-dv`, `cnpj-val`) together.

### Improvements

- **`CnpjUtils`**: Construct formatter and generator from options instances and forward v2 keyword-based `format` / `generate` calls.
- **Exports**: Re-export underlying v2 exception types and keep legacy alias names (`CnpjGeneratorError`, `CnpjFormatterError`, etc.).

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
