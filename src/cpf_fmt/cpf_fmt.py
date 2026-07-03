from __future__ import annotations

from typing import TYPE_CHECKING

from .cpf_formatter import CpfFormatter

if TYPE_CHECKING:
    from .types import CpfFormatterOptionsInput, CpfInput, OnFailCallback


def cpf_fmt(
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
    """Helper function to simplify the usage of :class:`CpfFormatter`.

    Formats a CPF string according to the given options. With no
    options, returns the traditional CPF format (e.g.
    ``123.456.789-10``). Invalid input length is handled by the
    configured ``on_fail`` callback instead of throwing.

    Raises:
        CpfFormatterInputTypeError: If ``cpf_input`` is not a
            ``str`` or sequence of ``str``.
        CpfFormatterOptionsTypeError: If any option has an invalid
            type.
        CpfFormatterOptionsHiddenRangeInvalidException: If
            ``hidden_start`` or ``hidden_end`` are out of valid range.
        CpfFormatterOptionsForbiddenKeyCharacterException: If any key
            option contains a disallowed character.

    See Also:
        :class:`CpfFormatter` for detailed option descriptions.
    """
    return CpfFormatter(
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
    ).format(cpf_input)


__all__ = ["cpf_fmt"]
