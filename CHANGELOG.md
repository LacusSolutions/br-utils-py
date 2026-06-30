# cnpj-val

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — Full support for the [14-character alphanumeric CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2023/julho/cnpj-alfa-numerico); default mode is alphanumeric, with optional `type="numeric"` for digits-only.
- ✨ **`type` and `case_sensitive` options** — Control validation mode and whether lowercase letters are accepted on alphanumeric input.
- 🛡️ **Structured errors** — Typed exception hierarchy for invalid input or options; invalid CNPJ data still returns `False`.
- 📥 **Flexible input** — Accepts `str` or `Sequence[str]` (formatted or raw); non-alphanumeric characters are stripped per `type`.

### BREAKING CHANGES

- **Default validation is alphanumeric and case-sensitive** — Without options, letters are kept and lowercase yields `False`; use `type="numeric"` for legacy numeric-only behavior and `case_sensitive=False` to accept lowercase.
- **Invalid input type now raises** — `cnpj_val()` and `CnpjValidator.is_valid()` raise `CnpjValidatorInputTypeError` when input is not a string or sequence of strings (v1 returned `False` or had unspecified behavior).
- **Expanded signatures** — `cnpj_val()` / `is_valid()` accept `str | Sequence[str]` and optional per-call options; v1 accepted only a single `str`.
- **New exports** — Package now exposes `CnpjValidatorOptions`, exception classes, type aliases, and `CNPJ_LENGTH` alongside `cnpj_val` and `CnpjValidator`.
- **Dependencies** — Requires `cnpj-dv` 2.x and adds runtime dependency `lacus.utils`; upgrade `cnpj-dv` before installing.
- **Stricter eligibility** — Zeroed base ID, zeroed branch ID, and 12 repeated numeric digits return `False` via `cnpj-dv` 2.x rules.

### New features

- **`CnpjValidatorOptions`** — Reusable options with `set()` merge, read-only frozen `all` snapshot, and static defaults `DEFAULT_CASE_SENSITIVE` / `DEFAULT_TYPE`.
- **Exception hierarchy** — `CnpjValidatorTypeError`, `CnpjValidatorInputTypeError`, `CnpjValidatorOptionsTypeError`, `CnpjValidatorException`, and `CnpjValidatorOptionTypeInvalidException`.
- **Per-call keyword options** — `CnpjValidator`, `cnpj_val()`, and `is_valid()` accept keyword-only `case_sensitive` and `type` besides an `options` mapping, matching `cnpj-fmt` and `cnpj-gen`.
- **Verifier-digit rule** — Rejects CNPJs whose last two characters are not digits (`0`–`9`).

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
