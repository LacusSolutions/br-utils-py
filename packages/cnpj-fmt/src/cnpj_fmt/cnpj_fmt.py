from collections.abc import Callable

from .cnpj_formatter import CnpjFormatter


def cnpj_fmt(
    cnpj_string: str,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
    slash_key: str | None = None,
    dash_key: str | None = None,
    escape: bool | None = None,
    on_fail: Callable | None = None,
) -> str:
    formatter = CnpjFormatter(
        hidden,
        hidden_key,
        hidden_start,
        hidden_end,
        dot_key,
        slash_key,
        dash_key,
        escape,
        on_fail,
    )

    return formatter.format(cnpj_string)
