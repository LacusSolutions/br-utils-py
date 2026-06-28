from __future__ import annotations

from typing import TYPE_CHECKING

from .cnpj_formatter import CnpjFormatter

if TYPE_CHECKING:
    from .types import CnpjFormatterOptionsInput, CnpjInput, OnFailCallback


def cnpj_fmt(
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
    """Helper function to simplify the usage of :class:`CnpjFormatter`.

    Formats a CNPJ string according to the given options. With no
    options, returns the traditional CNPJ format (e.g.
    ``12.345.678/0009-10``). Invalid input length is handled by the
    configured ``on_fail`` callback instead of throwing.

    Raises:
        CnpjFormatterInputTypeError: If ``cnpj_input`` is not a
            ``str`` or sequence of ``str``.
        CnpjFormatterOptionsTypeError: If any option has an invalid
            type.
        CnpjFormatterOptionsHiddenRangeInvalidException: If
            ``hidden_start`` or ``hidden_end`` are out of valid range.
        CnpjFormatterOptionsForbiddenKeyCharacterException: If any key
            option contains a disallowed character.

    See Also:
        :class:`CnpjFormatter` for detailed option descriptions.
    """
    return CnpjFormatter(
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
    ).format(cnpj_input)


__all__ = ["cnpj_fmt"]
