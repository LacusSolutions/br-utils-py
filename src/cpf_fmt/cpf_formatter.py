"""Formatter for CPF (Cadastro de Pessoa Física) identifiers."""

from __future__ import annotations

import html
import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from .cpf_formatter_options import CPF_LENGTH, CpfFormatterOptions
from .exceptions import (
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
    CpfFormatterOptionsTypeError,
)

if TYPE_CHECKING:
    from .types import CpfFormatterOptionsInput, CpfInput, OnFailCallback

HIDDEN_KEY_PLACEHOLDER = CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS[0]
"""A rarely-used 1-length character that is replaced with ``hidden_key``
when ``hidden`` is ``True``.
"""

_NON_DIGIT_PATTERN = re.compile(r"\D")


def _sanitize_cpf_input(value: str) -> str:
    """Strip non-digit characters from the input."""
    if len(value) == CPF_LENGTH and value.isascii() and value.isdigit():
        return value

    return _NON_DIGIT_PATTERN.sub("", value)


def _has_per_call_overrides(
    options: CpfFormatterOptionsInput,
    *,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
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
    cpf_input: CpfInput,
    exception: CpfFormatterInputLengthException,
) -> str:
    result = on_fail(cpf_input, exception)

    if not isinstance(result, str):
        raise CpfFormatterOptionsTypeError("on_fail", result, "string")

    return result


class CpfFormatter:
    """Formatter for CPF identifiers.

    Normalizes and optionally masks, HTML-escapes, or URL-encodes
    11-digit CPF input. Accepts a string or sequence of strings;
    non-digit characters are stripped. Invalid input type is handled by
    throwing; invalid length is handled via the configured ``on_fail``
    callback instead of throwing.
    """

    __slots__ = ("_options",)

    def __init__(
        self,
        options: CpfFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
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

        When ``options`` is a :class:`CpfFormatterOptions` instance,
        that instance is used directly (no copy is created). Mutating it
        later (e.g. via the :attr:`options` property or the original
        reference) affects future :meth:`format` calls that do not pass
        per-call options. When a plain mapping or nothing is passed, a
        new :class:`CpfFormatterOptions` instance is created from it.

        Raises:
            CpfFormatterOptionsTypeError: If any option has an invalid
                type.
            CpfFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CpfFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        if isinstance(options, CpfFormatterOptions):
            self._options = options
        else:
            self._options = CpfFormatterOptions(
                options,
                hidden=hidden,
                hidden_key=hidden_key,
                hidden_start=hidden_start,
                hidden_end=hidden_end,
                dot_key=dot_key,
                dash_key=dash_key,
                escape=escape,
                encode=encode,
                on_fail=on_fail,
            )

    @property
    def options(self) -> CpfFormatterOptions:
        """Return the default options used by this formatter.

        The returned object is the same instance used internally;
        mutating it (e.g. via setters on
        :class:`CpfFormatterOptions`) affects future :meth:`format`
        calls that do not pass ``options``.
        """
        return self._options

    def format(
        self,
        cpf_input: CpfInput,
        options: CpfFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: OnFailCallback | None = None,
    ) -> str:
        """Format a CPF value into a human-readable string.

        Input is normalized by stripping non-digit characters. If the
        result length is not exactly 11, the configured ``on_fail``
        callback is invoked with the original value and an error; its
        return value is used as the result.

        When valid, the result may be further transformed according to
        options:

        - If ``hidden`` is ``True``, digits between ``hidden_start`` and
          ``hidden_end`` (inclusive) are replaced with ``hidden_key``.
        - If ``escape`` is ``True``, HTML special characters are
          escaped.
        - If ``encode`` is ``True``, the string is URL-encoded (similar
          to JavaScript's ``encodeURIComponent``).

        Per-call ``options`` are merged over the instance default
        options for this call only; the instance defaults are
        unchanged. When both the ``options`` argument and named
        keyword parameters are provided, ``options`` takes precedence.

        Raises:
            CpfFormatterInputTypeError: If the input is not a ``str``
                or sequence of ``str``.
            CpfFormatterOptionsTypeError: If any option has an invalid
                type.
            CpfFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CpfFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        actual_input = self._to_string_input(cpf_input)

        if _has_per_call_overrides(
            options,
            hidden=hidden,
            hidden_key=hidden_key,
            hidden_start=hidden_start,
            hidden_end=hidden_end,
            dot_key=dot_key,
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

        formatted_cpf = _sanitize_cpf_input(actual_input)

        if len(formatted_cpf) != CPF_LENGTH:
            exception = CpfFormatterInputLengthException(
                cpf_input,
                formatted_cpf,
                CPF_LENGTH,
            )

            return _invoke_on_fail(actual_options.on_fail, cpf_input, exception)

        if actual_options.hidden:
            starting_part = formatted_cpf[: actual_options.hidden_start]
            ending_part = formatted_cpf[actual_options.hidden_end + 1 :]
            hidden_part_length = (
                actual_options.hidden_end - actual_options.hidden_start + 1
            )
            hidden_part = HIDDEN_KEY_PLACEHOLDER * hidden_part_length
            formatted_cpf = starting_part + hidden_part + ending_part

        formatted_cpf = (
            formatted_cpf[:3]
            + actual_options.dot_key
            + formatted_cpf[3:6]
            + actual_options.dot_key
            + formatted_cpf[6:9]
            + actual_options.dash_key
            + formatted_cpf[9:11]
        )

        if actual_options.hidden:
            formatted_cpf = formatted_cpf.replace(
                HIDDEN_KEY_PLACEHOLDER,
                actual_options.hidden_key,
            )

        if actual_options.escape:
            formatted_cpf = html.escape(formatted_cpf, quote=True)

        if actual_options.encode:
            formatted_cpf = quote(formatted_cpf, safe="")

        return formatted_cpf

    @staticmethod
    def _to_string_input(cpf_input: Any) -> str:
        """Normalize the input to a string.

        Raises:
            CpfFormatterInputTypeError: If the input is not a
                ``str`` or sequence of ``str``.
        """
        if isinstance(cpf_input, str):
            return cpf_input

        if isinstance(cpf_input, Sequence) and not isinstance(cpf_input, (str, bytes)):
            for item in cpf_input:
                if not isinstance(item, str):
                    raise CpfFormatterInputTypeError(cpf_input, "string or string[]")

            return "".join(cpf_input)

        raise CpfFormatterInputTypeError(cpf_input, "string or string[]")


__all__ = ["CpfFormatter"]
