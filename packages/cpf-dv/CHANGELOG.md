# cpf-dv

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🛡️ **Structured errors** — Typed `TypeError` / `Exception` hierarchy with snake_case attributes such as `actual_input`, `actual_type`, `expected_type`, `evaluated_input`, `min_expected_length`, `max_expected_length`, and `reason` on concrete classes.
- 📥 **Flexible input** — Accepts formatted `str` or `list[str]`; strips non-digit characters and preserves leading zeros.
- 📏 **Module constants** — Exports `CPF_MIN_LENGTH`, `CPF_MAX_LENGTH`, and the `CpfInput` type alias.

### BREAKING CHANGES

- **Result API**: Replaced `first_digit`/`second_digit` (`int`), `to_list()`, and `to_string()` with `first`/`second`/`both`/`cpf` string properties.
- **Exceptions**: Removed `CpfCheckDigitsError`, `CpfCheckDigitsInputLengthError`, `CpfCheckDigitsInputNotValidError`, and `CpfCheckDigitsCalculationError`; import `CpfCheckDigitsTypeError`, `CpfCheckDigitsInputTypeError`, `CpfCheckDigitsException`, `CpfCheckDigitsInputLengthException`, and `CpfCheckDigitsInputInvalidException` instead.
- **Input types**: Constructor accepts only `str | list[str]`; `list[int]` is no longer supported.
- **Dependencies**: Requires `lacus.utils` for type-error messages; v1 had zero runtime dependencies.

## 1.0.0

### 🚀 Stable Version Released!

Utility class to calculate check digits on CPF (Brazilian individual taxpayer ID). Main features:

- **Multiple input formats**: accepts strings, lists of strings, or lists of integers
- **Format agnostic**: automatically strips non-numeric characters from input
- **Lazy evaluation**: check digits are calculated only when accessed
- **Zero dependencies**: no external packages required
- **Comprehensive error handling**: specific exceptions for different error scenarios

For detailed usage and API reference, see the [README](./README.md).
