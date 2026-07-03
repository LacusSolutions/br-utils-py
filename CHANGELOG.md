# cpf-gen

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🏗️ **Class-based API** — `CpfGenerator` holds default options; `generate()` accepts optional per-call overrides; `cpf_gen()` remains for one-off usage.
- ✨ **Reusable options** — `CpfGeneratorOptions` with getters/setters, `set()` for bulk updates, and read-only `all` snapshot.
- 🛡️ **Structured errors** — Typed `CpfGeneratorTypeError` / `CpfGeneratorException` hierarchies for options and prefix validation.
- 📐 **Stricter prefix validation** — Prefix rejects zeroed base (9 zeros) and 9 repeated digits.

### BREAKING CHANGES

- **Constructor signatures** — `CpfGenerator` and `cpf_gen` now accept an optional options object/mapping plus keyword-only `format` and `prefix` instead of positional `format`/`prefix`.
- **Exception classes** — Removed `CpfGeneratorError`, `CpfGeneratorPrefixLengthError`, and `CpfGeneratorPrefixNotValidError`; migrate `except` clauses to `CpfGeneratorOptionsTypeError`, `CpfGeneratorOptionPrefixInvalidException`, and related subclasses.
- **Prefix behavior** — Prefix overflow truncates to 9 characters instead of raising a length error; zeroed base and 9 repeated-digit prefixes raise `CpfGeneratorOptionPrefixInvalidException`.
- **`CpfGeneratorOptions` refactor** — Replaced `merge()` with `set()` and layered constructor overrides; read-only `all` snapshot; static defaults `DEFAULT_FORMAT`, `DEFAULT_PREFIX`.
- **Dependencies** — Added runtime dependency `lacus.utils`; requires `cpf-dv` 2.x for check-digit calculation and retry.

### New features

- **Exports** — `CPF_LENGTH`, `CPF_PREFIX_MAX_LENGTH`, and options type aliases (`CpfGeneratorOptionsInput`, `CpfGeneratorOptionsType`).
- **Retry on invalid sequence** — Generator retries when `cpf-dv` rejects a random body candidate.

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.

## 1.0.1

### Patch Changes

- 344fbe7: Migrate internal dependency from `cpf-cd` to `cpf-dv` to calculate check digits.
- Dropped dependencies
  - `cpf-cd`
- Added dependencies
  - `cpf-dv` (1.0.0)

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to generate valid CPF (Brazilian personal ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CpfGenerator`) and function-based (`cpf_gen`) usage
- **Valid check digits**: automatically calculates and appends correct check digits using the official CPF algorithm
- **Prefix support**: generate CPFs starting with a custom prefix (up to 9 digits)
- **Optional formatting**: output with standard CPF format (dots and dash) or unformatted
- **Repeated digits validation**: prevents generating invalid CPFs with all repeated digits (e.g., `111.111.111-11`)
- **Zero external dependencies**: only relies on `cpf-cd` from the same package family
- **Lightweight**: only requires `cpf-cd`, from the same initiative, for check digit calculation

For detailed usage and API reference, see the [README](./README.md).
