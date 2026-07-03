# cpf-val

## 2.0.0

### 🎉 v2 at a glance 🎊

- 📥 **Flexible input** — Accepts `str` or `Sequence[str]` (formatted or raw); non-digit characters are stripped before validation.
- 🛡️ **Structured errors** — Typed exception hierarchy raised on invalid input type; invalid CPF data still returns `False`.
- 📦 **Explicit exports** — Now exposes `CpfValidator`, `CPF_LENGTH`, `CpfInput`, and the exception classes alongside `cpf_val`.
- 🔢 **Check digits** — Delegates check-digit and repeated-digit rejection to `cpf-dv` 2.x.

### BREAKING CHANGES

- **Invalid input type now raises** — `cpf_val()` and `CpfValidator.is_valid()` raise `CpfValidatorInputTypeError` when input is not a string or sequence of strings; v1 accepted only `str`.
- **Expanded signatures** — `cpf_val()` / `is_valid()` accept `str | Sequence[str]`; v1 accepted only a single `str`.
- **New exports** — Package now exposes `CpfValidator`, `CPF_LENGTH`, `CpfInput`, and the exception classes alongside `cpf_val`.
- **Dependencies** — Requires `cpf-dv` 2.x and adds runtime dependency `lacus.utils`; upgrade `cpf-dv` before installing.

### New features

- **Exception hierarchy** — `CpfValidatorTypeError` (abstract), `CpfValidatorInputTypeError`, and `CpfValidatorException` (abstract base).
- **Sequence input** — A `Sequence[str]` is joined and validated like a single string via the `CpfInput` alias.
- **`CPF_LENGTH` constant** — The `11`-digit CPF length constant is now part of the public API.

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.
- **Check digits** — Compares sanitized input to `CpfCheckDigits(...).cpf` from `cpf-dv` 2.x, which also rejects repeated-digit bases.

## 1.0.1

### Patch Changes

- 8d48436: Migrate internal dependency from `cpf-cd` to `cpf-dv` to calculate check digits.
- Dropped dependencies
  - `cpf-cd`
- Added dependencies
  - `cpf-dv` (1.0.0)

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to validate CPF (Brazilian personal ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CpfValidator`) and function-based (`cpf_val`) usage
- **Format agnostic**: accepts CPF with or without formatting (dots, dashes)
- **Strict validation**: validates both check digits according to the official Brazilian CPF algorithm
- **Type safety**: built with Python 3.10+ type hints
- **Lightweight**: only requires `cpf-cd`, from the same initiative, for check digit calculation
- **Graceful error handling**: returns `False` for invalid inputs without raising exceptions

For detailed usage and API reference, see the [README](./README.md).
