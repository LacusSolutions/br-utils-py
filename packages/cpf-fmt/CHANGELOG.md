# cpf-fmt

## 2.0.1

### Patch Changes

- **Exception bases** — Typed error base classes no longer inherit `ABC`; aligns with `cpf-dv`/`cnpj-dv` and removes a misleading “abstract” label from the docs.


## 2.0.0

### 🎉 v2 at a glance 🎊

- 🛡️ **Structured errors** — Typed `CpfFormatterTypeError` / `CpfFormatterException` hierarchies with attributes such as `actual_input`, `evaluated_input`, and `expected_length` on concrete classes.
- ⚙️ **Flexible options API** — Pass `CpfFormatterOptions`, a mapping, and/or named kwargs on `CpfFormatter`, `cpf_fmt`, and `format()`; includes `encode`, exported `CPF_LENGTH` and `CpfInput`, and an explicit `__all__` public surface.
- 📥 **Sequence input** — `format()` and `cpf_fmt()` accept `str | Sequence[str]`; sequences are concatenated before digit sanitization.

### BREAKING CHANGES

- **`on_fail` default** — Default callback returns `''` instead of the original input for invalid length; signature is `(value, exception)`.
- **`on_fail` single-arg callbacks** — v1 silently retried with one argument when the two-arg call raised `TypeError`; v2 always passes `(value, exception)` (update callbacks to accept both parameters).
- **Exception classes** — Removed `CpfFormatterError`, `CpfFormatterInputLengthError`, `CpfFormatterHiddenRangeError`, and `CpfFormatterOptionTypeError`; migrate `except` clauses to `CpfFormatterInputLengthException`, `CpfFormatterOptionsHiddenRangeInvalidException`, `CpfFormatterOptionsTypeError`, and the new type/exception hierarchies.
- **`merge()` removed** — Build per-call options with `CpfFormatterOptions.copy()` + `set()`, constructor overrides, or a fresh `CpfFormatterOptions` instance instead of positional `CpfFormatterOptions.merge()`.
- **Input type** — `CpfFormatter.format()` and `cpf_fmt()` accept `str | Sequence[str]` (sequences are concatenated); other types raise `CpfFormatterInputTypeError` (v1 only accepted `str`).
- **`CpfFormatter` constructor** — First argument is now an optional `CpfFormatterOptions` instance or mapping; v1 accepted only flat option parameters in a fixed order.
- **Module-level defaults** — `DEFAULT_DOT_KEY`, `DEFAULT_DASH_KEY`, `DEFAULT_ON_FAIL`, and related constants are no longer exported from the package root; use `CpfFormatterOptions.DEFAULT_*` instead.
- **Dependencies** — Added runtime dependency `lacus.utils` (v1 had zero external dependencies).

### New features

- **`encode` option** — When `True`, the formatted CPF is URL-encoded (similar to JavaScript's `encodeURIComponent`).
- **`format()` per-call options** — Accept a `CpfFormatterOptions` instance or mapping plus named kwargs; all merge over instance defaults for that call only, with `options` winning over keyword arguments when both are set.
- **Explicit error model** — `CpfFormatterInputTypeError`, `CpfFormatterOptionsTypeError`, `CpfFormatterInputLengthException`, `CpfFormatterOptionsHiddenRangeInvalidException`, and `CpfFormatterOptionsForbiddenKeyCharacterException` for typed errors and clearer handling.
- **`CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS`** — Reserved characters for `hidden_key`, `dot_key`, and `dash_key` (internal masking pipeline).
- **`get_default_on_fail()`** — Shared default failure callback used by `CpfFormatterOptions.DEFAULT_ON_FAIL`.

### Improvements

- **Options as properties** — `CpfFormatterOptions` uses validated properties and `set()` / `set_hidden_range()` instead of a dataclass with positional `merge()`.
- **Shared options instance** — Passing a `CpfFormatterOptions` instance to `CpfFormatter` shares it by reference; mutating it affects future `format()` calls without per-call overrides.
- **Multi-character `hidden_key`** — Masking uses an internal placeholder so multi-character keys preserve output length (v1 repeated the key string per digit index).
- **Per-call precedence docs** — The `format()` docstring documents that the `options` argument overrides named keyword parameters on conflict.

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to format CPF (Brazilian individual taxpayer ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CpfFormatter`) and function-based (`cpf_fmt`) usage
- **Format agnostic**: accepts CPF with or without formatting (dots, dashes, spaces)
- **Flexible output**: configurable delimiters for dots and dashes
- **Privacy support**: masking/hidden digits with customizable character and range
- **HTML escaping**: optional HTML entity escaping for safe web rendering
- **Graceful error handling**: configurable fallback function for invalid input
- **Type safety**: built with Python 3.10+ type hints
- **Zero dependencies**: no external packages required

For detailed usage and API reference, see the [README](./README.md).
