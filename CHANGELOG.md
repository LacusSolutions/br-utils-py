# cpf-utils

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
