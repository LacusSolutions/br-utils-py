# cnpj-fmt

## 2.0.2

### Patch Changes

- **Exception bases** — Typed error base classes no longer inherit `ABC`; aligns with `cpf-dv`/`cnpj-dv` and removes a misleading “abstract” label from the docs.

## 2.0.1

### Improvements

- **requires-python** — Declares support for Python `>=3.10,<4.0`.

## 2.0.0

### 🎉 v2 at a glance 🎊

- 🆕 **Alphanumeric CNPJ** — Full support for the [14-character alphanumeric CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2023/julho/cnpj-alfa-numerico) (digits and letters); input is sanitized and uppercased, with a fast path for already-normalized values.
- 🛡️ **Structured errors** — Typed `CnpjFormatterTypeError` / `CnpjFormatterException` hierarchies with attributes such as `actual_input`, `evaluated_input`, and `expected_length` on concrete classes.
- ⚙️ **Flexible options API** — Pass `CnpjFormatterOptions`, a mapping, and/or named kwargs on `CnpjFormatter`, `cnpj_fmt`, and `format()`; includes `encode`, exported `CNPJ_LENGTH` and `CnpjInput`, and an explicit `__all__` public surface.

### BREAKING CHANGES

- **Letters retained** — Sanitization keeps ASCII letters (uppercased) instead of stripping non-digit characters before formatting.
- **`on_fail` default** — Default callback returns `''` instead of the original input for invalid length; signature is `(value, exception)`.
- **`on_fail` single-arg callbacks** — v1 silently retried with one argument when the two-arg call raised `TypeError`; v2 always passes `(value, exception)` (update callbacks to accept both parameters).
- **Exception classes** — Removed `CnpjFormatterError`, `CnpjFormatterInvalidLengthError`, and `CnpjFormatterHiddenRangeError`; migrate `except` clauses to `CnpjFormatterInputLengthException`, `CnpjFormatterOptionsHiddenRangeInvalidException`, and the new type/exception hierarchies.
- **`merge()` removed** — Build per-call options with `CnpjFormatterOptions.copy()` + `set()`, constructor overrides, or a fresh `CnpjFormatterOptions` instance instead of `CnpjFormatterOptions.merge()`.
- **Input type** — `CnpjFormatter.format()` and `cnpj_fmt()` accept `str | Sequence[str]` (sequences are concatenated); other types raise `CnpjFormatterInputTypeError` (v1 only accepted `str`).
- **`CnpjFormatter` constructor** — First argument is now an optional `CnpjFormatterOptions` instance or mapping; v1 accepted only flat option parameters in a fixed order.
- **Dependencies** — Added runtime dependency `lacus.utils` (v1 had zero external dependencies).

### New features

- **Alphanumeric CNPJ** — Both numeric and alphanumeric 14-character CNPJs are supported after stripping punctuation and uppercasing letters.
- **`encode` option** — When `True`, the formatted CNPJ is URL-encoded (similar to JavaScript's `encodeURIComponent`).
- **`format()` per-call options** — Accept a `CnpjFormatterOptions` instance or mapping plus named kwargs; all merge over instance defaults for that call only, with `options` winning over keyword arguments when both are set.
- **Explicit error model** — `CnpjFormatterInputTypeError`, `CnpjFormatterOptionsTypeError`, `CnpjFormatterInputLengthException`, `CnpjFormatterOptionsHiddenRangeInvalidException`, and `CnpjFormatterOptionsForbiddenKeyCharacterException` for typed errors and clearer handling.
- **`CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS`** — Reserved characters for `hidden_key`, `dot_key`, `slash_key`, and `dash_key` (internal masking pipeline).
- **`get_default_on_fail()`** — Shared default failure callback used by `CnpjFormatterOptions.DEFAULT_ON_FAIL`.

### Improvements

- **Options as properties** — `CnpjFormatterOptions` uses validated properties and `set()` / `set_hidden_range()` instead of a frozen dataclass with `merge()`.
- **Shared options instance** — Passing a `CnpjFormatterOptions` instance to `CnpjFormatter` shares it by reference; mutating it affects future `format()` calls without per-call overrides.
- **Per-call precedence docs** — README (EN/PT) and the `format()` docstring document that the `options` argument overrides named keyword parameters on conflict.

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to format CNPJ (Brazilian legal entity ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CnpjFormatter`) and function-based (`cnpj_fmt`) usage
- **Format agnostic**: automatically strips non-numeric characters from input
- **Customizable output**: configurable delimiters (dot, slash, dash) for flexible formatting
- **Privacy masking**: hide sensitive digits with configurable range and mask character
- **HTML escaping**: built-in support for safe HTML output
- **Graceful error handling**: customizable fallback via `on_fail` callback for invalid inputs
- **Zero dependencies**: no external packages required

For detailed usage and API reference, see the [README](./README.md).
