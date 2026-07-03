"""Type aliases for the ``cpf_fmt`` package."""

from collections.abc import Callable, Mapping, Sequence
from typing import Any, TypeAlias, TypedDict

from .cpf_formatter_options import CpfFormatterOptions
from .exceptions import CpfFormatterException

CpfInput = str | Sequence[str]
"""Represents valid input types for CPF formatting.

A CPF can be provided as:

- A string containing digits (with or without formatting)
- A sequence of strings, where each string represents a digit or group of
  digits.
"""

OnFailCallback = Callable[[Any, CpfFormatterException], str]
"""Callback function type for handling formatting failures.

This function is invoked when the CPF formatter encounters an error during
formatting, such as invalid input length or other formatting issues. The
callback receives the original input value and the exception object, and
should return a string to use as the fallback output.
"""

CpfFormatterOptionsInput: TypeAlias = CpfFormatterOptions | Mapping[str, Any] | None


class CpfFormatterOptionsType(TypedDict):
    """Configuration for CPF formatting options.

    Defines all available options for customizing how CPF digits are formatted,
    including delimiter characters, hidden digit ranges, HTML escaping, URL
    encoding, and error handling. All properties have default values and are
    optional when creating a new :class:`CpfFormatterOptions` instance.

    Attributes:
        hidden: When ``True``, digits within ``hidden_start`` to ``hidden_end``
            (inclusive) are replaced with ``hidden_key``.
        hidden_key: String used to mask hidden digits when ``hidden`` is
            ``True``.
        hidden_start: Inclusive start index (0-10) for hiding digits.
        hidden_end: Inclusive end index (0-10) for hiding digits.
        dot_key: Dot delimiter between the first digit groups.
        dash_key: Dash delimiter before the final check digits.
        escape: When ``True``, HTML special characters are escaped.
        encode: When ``True``, the formatted string is URL-encoded.
        on_fail: Callback invoked when normalized input length is not 11;
            default returns ``''``.
    """

    hidden: bool
    hidden_key: str
    hidden_start: int
    hidden_end: int
    dot_key: str
    dash_key: str
    escape: bool
    encode: bool
    on_fail: OnFailCallback


__all__ = [
    "CpfFormatterOptionsInput",
    "CpfFormatterOptionsType",
    "CpfInput",
    "OnFailCallback",
]
