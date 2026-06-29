"""Type aliases for the ``cnpj_fmt`` package."""

from collections.abc import Callable, Mapping, Sequence
from typing import Any, TypeAlias, TypedDict

from .cnpj_formatter_options import CnpjFormatterOptions
from .exceptions import CnpjFormatterException

CnpjInput = str | Sequence[str]
"""Represents valid input types for CNPJ formatting.

A CNPJ can be provided as:

- A string containing alphanumeric characters (with or without
  formatting)
- A sequence of strings, where each string represents an alphanumeric
  character or group of alphanumeric characters.
"""

OnFailCallback = Callable[[Any, CnpjFormatterException], str]
"""Callback function type for handling formatting failures.

This function is invoked when the CNPJ formatter encounters an error
during formatting, such as invalid input length or other formatting
issues. The callback receives the original input value and the exception
object, and should return a string to use as the fallback output.
"""

CnpjFormatterOptionsInput: TypeAlias = CnpjFormatterOptions | Mapping[str, Any] | None


class CnpjFormatterOptionsType(TypedDict):
    """Configuration for CNPJ formatting options.

    Defines all available options for customizing how CNPJ characters are
    formatted, including delimiter characters, hidden character ranges,
    HTML escaping, URL encoding, and error handling. All properties have
    default values and are optional when creating a new
    :class:`CnpjFormatterOptions` instance.

    Attributes:
        hidden: When ``True``, characters within ``hidden_start`` to
            ``hidden_end`` (inclusive) are replaced with ``hidden_key``.
        hidden_key: String used to mask hidden characters when
            ``hidden`` is ``True``.
        hidden_start: Inclusive start index (0-13) for hiding
            characters.
        hidden_end: Inclusive end index (0-13) for hiding characters.
        dot_key: Dot delimiter between the first character groups.
        slash_key: Slash delimiter before the branch identifier block.
        dash_key: Dash delimiter before the final check characters.
        escape: When ``True``, HTML special characters are escaped.
        encode: When ``True``, the formatted string is URL-encoded.
        on_fail: Callback invoked when normalized input length is not
            14; default returns ``''``.
    """

    hidden: bool
    hidden_key: str
    hidden_start: int
    hidden_end: int
    dot_key: str
    slash_key: str
    dash_key: str
    escape: bool
    encode: bool
    on_fail: OnFailCallback


__all__ = [
    "CnpjFormatterOptionsInput",
    "CnpjFormatterOptionsType",
    "CnpjInput",
    "OnFailCallback",
]
