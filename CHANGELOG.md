# cnpj-dv

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — Supports the new 14-character alphanumeric format (letters `A–Z` plus digits); check digits stay numeric.
- 🛡️ **Structured errors** — Typed `TypeError` / `Exception` hierarchy with `actualInput`, `reason`, and length attributes on concrete classes.
- 📥 **Flexible input** — Accepts formatted `str` or `list[str]`; strips non-alphanumeric characters and uppercases letters.

### BREAKING CHANGES

- **Result API**: Replaced `first_digit`/`second_digit` (`int`), `to_list()`, and `to_string()` with `first`/`second`/`both`/`cnpj` string properties.
- **Exceptions**: Removed `CnpjCheckDigitsError`, `CnpjTypeError`, `CnpjInvalidLengthError`, and `CnpjCheckDigitsCalculationError`; import `CnpjCheckDigitsTypeError`, `CnpjCheckDigitsInputTypeError`, `CnpjCheckDigitsException`, `CnpjCheckDigitsInputLengthException`, and `CnpjCheckDigitsInputInvalidException` instead.
- **Input types**: Constructor accepts only `str | list[str]`; `list[int]` is no longer supported.
- **Validation rules**: Ineligible base ID (`00000000`), branch ID (`0000`), and repeated numeric digits now raise `CnpjCheckDigitsInputInvalidException`.
- **Dependencies**: Requires `lacus.utils` for type-error messages; v1 had zero runtime dependencies.

## 1.0.0

### 🚀 Stable Version Released!

Utility class to calculate check digits on CNPJ (Brazilian legal entity ID). Main features:

- **Multiple input formats**: accepts strings, lists of strings, or lists of integers
- **Format agnostic**: automatically strips non-numeric characters from input
- **Lazy evaluation**: check digits are calculated only when accessed
- **Zero dependencies**: no external packages required
- **Comprehensive error handling**: specific exceptions for different error scenarios

For detailed usage and API reference, see the [README](./README.md).
