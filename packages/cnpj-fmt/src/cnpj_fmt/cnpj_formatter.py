"""Formatter for CNPJ (Cadastro Nacional da Pessoa Jurídica) identifiers."""

from __future__ import annotations

import html
import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from .cnpj_formatter_options import CNPJ_LENGTH, CnpjFormatterOptions
from .exceptions import (
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
    CnpjFormatterOptionsTypeError,
)

if TYPE_CHECKING:
    from .types import CnpjFormatterOptionsInput, CnpjInput, OnFailCallback

HIDDEN_KEY_PLACEHOLDER = CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS[0]
"""A rarely-used 1-length character that is replaced with ``hidden_key``
when ``hidden`` is ``True``.
"""

_ALPHANUMERIC_PATTERN = re.compile(r"[^0-9A-Za-z]")


def _sanitize_cnpj_input(value: str) -> str:
    """Strip non-alphanumeric characters and uppercase the remainder."""
    if len(value) == CNPJ_LENGTH and value.isascii() and value.isalnum():
        if value.isupper():
            return value

        return value.upper()

    sanitized = _ALPHANUMERIC_PATTERN.sub("", value)

    return sanitized.upper()


def _has_per_call_overrides(
    options: CnpjFormatterOptionsInput,
    *,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
    slash_key: str | None = None,
    dash_key: str | None = None,
    escape: bool | None = None,
    encode: bool | None = None,
    on_fail: OnFailCallback | None = None,
) -> bool:
    return (
        options is not None
        or hidden is not None
        or hidden_key is not None
        or hidden_start is not None
        or hidden_end is not None
        or dot_key is not None
        or slash_key is not None
        or dash_key is not None
        or escape is not None
        or encode is not None
        or on_fail is not None
    )


def _per_call_option_overrides(
    *,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
    slash_key: str | None = None,
    dash_key: str | None = None,
    escape: bool | None = None,
    encode: bool | None = None,
    on_fail: OnFailCallback | None = None,
) -> dict[str, Any]:
    overrides: dict[str, Any] = {}

    if hidden is not None:
        overrides["hidden"] = hidden
    if hidden_key is not None:
        overrides["hidden_key"] = hidden_key
    if hidden_start is not None:
        overrides["hidden_start"] = hidden_start
    if hidden_end is not None:
        overrides["hidden_end"] = hidden_end
    if dot_key is not None:
        overrides["dot_key"] = dot_key
    if slash_key is not None:
        overrides["slash_key"] = slash_key
    if dash_key is not None:
        overrides["dash_key"] = dash_key
    if escape is not None:
        overrides["escape"] = escape
    if encode is not None:
        overrides["encode"] = encode
    if on_fail is not None:
        overrides["on_fail"] = on_fail

    return overrides


def _invoke_on_fail(
    on_fail: OnFailCallback,
    cnpj_input: CnpjInput,
    exception: CnpjFormatterInputLengthException,
) -> str:
    result = on_fail(cnpj_input, exception)

    if not isinstance(result, str):
        raise CnpjFormatterOptionsTypeError("on_fail", result, "string")

    return result


class CnpjFormatter:
    """Formatter for CNPJ identifiers.

    Normalizes and optionally masks, HTML-escapes, or URL-encodes
    14-character alphanumeric CNPJ input. Accepts a string or sequence
    of strings; non-alphanumeric characters are stripped and the result
    is uppercased. Invalid input type is handled by throwing; invalid
    length is handled via the configured ``on_fail`` callback instead
    of throwing.
    """

    __slots__ = ("_options",)

    def __init__(
        self,
        options: CnpjFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: OnFailCallback | None = None,
    ) -> None:
        """Create a new formatter with optional default options.

        Default options apply to every call to :meth:`format` unless
        overridden by the per-call ``options`` argument. Options control
        masking, HTML escaping, URL encoding, and the callback used when
        formatting fails.

        When ``options`` is a :class:`CnpjFormatterOptions` instance,
        that instance is used directly (no copy is created). Mutating it
        later (e.g. via the :attr:`options` property or the original
        reference) affects future :meth:`format` calls that do not pass
        per-call options. When a plain mapping or nothing is passed, a
        new :class:`CnpjFormatterOptions` instance is created from it.

        Raises:
            CnpjFormatterOptionsTypeError: If any option has an invalid
                type.
            CnpjFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        if isinstance(options, CnpjFormatterOptions):
            self._options = options
        else:
            self._options = CnpjFormatterOptions(
                options,
                hidden=hidden,
                hidden_key=hidden_key,
                hidden_start=hidden_start,
                hidden_end=hidden_end,
                dot_key=dot_key,
                slash_key=slash_key,
                dash_key=dash_key,
                escape=escape,
                encode=encode,
                on_fail=on_fail,
            )

    @property
    def options(self) -> CnpjFormatterOptions:
        """Return the default options used by this formatter.

        The returned object is the same instance used internally;
        mutating it (e.g. via setters on
        :class:`CnpjFormatterOptions`) affects future :meth:`format`
        calls that do not pass ``options``.
        """
        return self._options

    def format(
        self,
        cnpj_input: CnpjInput,
        options: CnpjFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: OnFailCallback | None = None,
    ) -> str:
        """Format a CNPJ value into a human-readable string.

        Input is normalized by stripping non-alphanumeric characters
        and converting to uppercase. If the result length is not
        exactly 14, the configured ``on_fail`` callback is invoked with
        the original value and an error; its return value is used as
        the result.

        When valid, the result may be further transformed according to
        options:

        - If ``hidden`` is ``True``, characters between
          ``hidden_start`` and ``hidden_end`` (inclusive) are replaced
          with ``hidden_key``.
        - If ``escape`` is ``True``, HTML special characters are
          escaped.
        - If ``encode`` is ``True``, the string is URL-encoded (similar
          to JavaScript's ``encodeURIComponent``).

        Per-call ``options`` are merged over the instance default
        options for this call only; the instance defaults are
        unchanged.

        Raises:
            CnpjFormatterInputTypeError: If the input is not a ``str``
                or sequence of ``str``.
            CnpjFormatterOptionsTypeError: If any option has an invalid
                type.
            CnpjFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        actual_input = self._to_string_input(cnpj_input)

        if _has_per_call_overrides(
            options,
            hidden=hidden,
            hidden_key=hidden_key,
            hidden_start=hidden_start,
            hidden_end=hidden_end,
            dot_key=dot_key,
            slash_key=slash_key,
            dash_key=dash_key,
            escape=escape,
            encode=encode,
            on_fail=on_fail,
        ):
            actual_options = self._options.copy()
            keyword_overrides = _per_call_option_overrides(
                hidden=hidden,
                hidden_key=hidden_key,
                hidden_start=hidden_start,
                hidden_end=hidden_end,
                dot_key=dot_key,
                slash_key=slash_key,
                dash_key=dash_key,
                escape=escape,
                encode=encode,
                on_fail=on_fail,
            )

            if keyword_overrides:
                actual_options.set(keyword_overrides)

            if options is not None:
                actual_options.set(options)
        else:
            actual_options = self._options

        formatted_cnpj = _sanitize_cnpj_input(actual_input)

        if len(formatted_cnpj) != CNPJ_LENGTH:
            exception = CnpjFormatterInputLengthException(
                cnpj_input,
                formatted_cnpj,
                CNPJ_LENGTH,
            )

            return _invoke_on_fail(actual_options.on_fail, cnpj_input, exception)

        if actual_options.hidden:
            starting_part = formatted_cnpj[: actual_options.hidden_start]
            ending_part = formatted_cnpj[actual_options.hidden_end + 1 :]
            hidden_part_length = (
                actual_options.hidden_end - actual_options.hidden_start + 1
            )
            hidden_part = HIDDEN_KEY_PLACEHOLDER * hidden_part_length
            formatted_cnpj = starting_part + hidden_part + ending_part

        formatted_cnpj = (
            formatted_cnpj[:2]
            + actual_options.dot_key
            + formatted_cnpj[2:5]
            + actual_options.dot_key
            + formatted_cnpj[5:8]
            + actual_options.slash_key
            + formatted_cnpj[8:12]
            + actual_options.dash_key
            + formatted_cnpj[12:14]
        )

        if actual_options.hidden:
            formatted_cnpj = formatted_cnpj.replace(
                HIDDEN_KEY_PLACEHOLDER,
                actual_options.hidden_key,
            )

        if actual_options.escape:
            formatted_cnpj = html.escape(formatted_cnpj, quote=True)

        if actual_options.encode:
            formatted_cnpj = quote(formatted_cnpj, safe="")

        return formatted_cnpj

    @staticmethod
    def _to_string_input(cnpj_input: Any) -> str:
        """Normalize the input to a string.

        Raises:
            CnpjFormatterInputTypeError: If the input is not a
                ``str`` or sequence of ``str``.
        """
        if isinstance(cnpj_input, str):
            return cnpj_input

        if isinstance(cnpj_input, Sequence) and not isinstance(
            cnpj_input, (str, bytes)
        ):
            for item in cnpj_input:
                if not isinstance(item, str):
                    raise CnpjFormatterInputTypeError(cnpj_input, "string or string[]")

            return "".join(cnpj_input)

        raise CnpjFormatterInputTypeError(cnpj_input, "string or string[]")


__all__ = ["CnpjFormatter"]
