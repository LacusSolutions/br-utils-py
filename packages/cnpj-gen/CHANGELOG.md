# cnpj-gen

## 2.0.3

### Patch Changes

- **Exception bases** — Typed error base classes no longer inherit `ABC`; aligns with `cpf-dv`/`cnpj-dv` and removes a misleading “abstract” label from the docs.

## 2.0.2

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.

## 2.0.1

### Patch Changes

- cafaf27: **Type hints** — Align `cnpj_gen`'s `options` parameter annotation with `CnpjGeneratorOptionsInput`.
- 1b6c59c: **`CnpjGeneratorOptions::set()` signature** — Require `options` on `CnpjGeneratorOptions.set()`; bare `.set()` calls now raise `TypeError`.

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — Full support for the [14-character alphanumeric CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2023/julho/cnpj-alfa-numerico); default output is alphanumeric (`0-9A-Z`), with optional `numeric` or `alphabetic` via the `type` option.
- ✨ **`type` option** — Control character set: `numeric`, `alphabetic`, or `alphanumeric` (default); prefix is sanitized (alphanumeric only, uppercased); only the randomly generated part follows `type`.
- 🛡️ **Structured errors** — Typed `CnpjGeneratorTypeError` / `CnpjGeneratorException` hierarchies for options and prefix validation.
- 📐 **Stricter prefix validation** — Prefix rejects zeroed base ID, zeroed branch ID, and 12 repeated digits.

### BREAKING CHANGES

- **Default output is alphanumeric** — Without options, generated CNPJs are 14-character alphanumeric instead of numeric-only; use `type="numeric"` for numeric-only behavior.
- **Constructor signatures** — `CnpjGenerator` and `cnpj_gen` now accept an optional options object/mapping plus keyword-only `format`, `prefix`, and `type` instead of positional `format`/`prefix`.
- **Exception classes** — Removed `CnpjGeneratorError`, `CnpjGeneratorInvalidPrefixLengthError`, and `CnpjGeneratorInvalidPrefixBranchIdError`; migrate `except` clauses to `CnpjGeneratorOptionsTypeError`, `CnpjGeneratorOptionPrefixInvalidException`, and related subclasses.
- **Prefix behavior** — Prefix accepts alphanumeric input (non-alphanumeric stripped, letters uppercased); overflow truncates to 12 characters instead of raising a length error; invalid combinations raise `CnpjGeneratorOptionPrefixInvalidException`.
- **`CnpjGeneratorOptions` refactor** — Replaced `merge()` with `set()` and layered constructor overrides; read-only `all` snapshot; static defaults `DEFAULT_FORMAT`, `DEFAULT_PREFIX`, `DEFAULT_TYPE`.
- **Dependencies** — Added runtime dependency `lacus.utils`; requires `cnpj-dv` 2.x for alphanumeric check-digit rules.

### New features

- **Exports** — `CnpjType`, `CNPJ_LENGTH`, `CNPJ_PREFIX_MAX_LENGTH`, and options type aliases (`CnpjGeneratorOptionsInput`, `CnpjGeneratorOptionsType`).
- **Retry on invalid sequence** — Generator retries when check-digit computation rejects a random body candidate.

## 1.0.2

### Patch Changes

- 1f3fdf5: Migrate internal dependency from `cnpj-cd` to `cnpj-dv` to calculate check digits.
- Dropped dependencies
  - `cnpj-cd`
- Added dependencies
  - `cnpj-dv` (1.0.0)

## 1.0.1

### Patch Changes

- db1f01b: Fix documentation hero image source.
- Updated dependencies
  - `cnpj-cd`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to generate valid CNPJ (Brazilian legal entity ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CnpjGenerator`) and function-based (`cnpj_gen`) usage
- **Valid check digits**: automatically calculates and appends correct check digits using the official CNPJ algorithm
- **Prefix support**: generate CNPJs starting with a custom prefix (business ID or partial branch ID)
- **Optional formatting**: output with standard CNPJ format (dots, slash, dash) or unformatted
- **Branch ID validation**: ensures branch ID is never "0000" (invalid per CNPJ rules)
- **Zero external dependencies**: only relies on `cnpj-dv` from the same package family

For detailed usage and API reference, see the [README](./README.md).
