# cnpj-val

## 2.0.0

### BREAKING CHANGES

- **Dependencies** — Requires `cnpj-dv` 2.x; upgrade `cnpj-dv` before installing this version.

### Bug fixes

- **`CnpjValidator`**: Pass a digit string to `CnpjCheckDigits` so validation works with the `cnpj-dv` 2.x API.

## 1.0.2

### Patch Changes

- ddb8e61: Migrate internal dependency from `cnpj-cd` to `cnpj-dv` to calculate check digits.
- Dropped dependencies
  - `cnpj-cd`
- Added dependencies
  - `cnpj-dv` (1.0.0)

## 1.0.1

### Patch Changes

- f853dbc: Fix documentation hero image source.
- Updated dependencies
  - `cnpj-cd`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to validate CNPJ (Brazilian legal entity ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CnpjValidator`) and function-based (`cnpj_val`) usage
- **Format agnostic**: accepts CNPJ with or without formatting (dots, slashes, dashes)
- **Strict validation**: validates both check digits according to the official Brazilian CNPJ algorithm
- **Type safety**: built with Python 3.10+ type hints
- **Lightweight**: minimal dependencies, only requires `cnpj-dv` for check digit calculation
- **Graceful error handling**: returns `False` for invalid inputs without raising exceptions

For detailed usage and API reference, see the [README](./README.md).
