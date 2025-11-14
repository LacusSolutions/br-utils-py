from collections.abc import Callable

from .cnpj_formatter import CnpjFormatter

CNPJ_LENGTH = 14


def cnpj_fmt(
    cnpj_string: str,
    escape: bool | None = None,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
    slash_key: str | None = None,
    dash_key: str | None = None,
    on_fail: Callable | None = None,
) -> str:
    formatter = CnpjFormatter(
        escape=escape,
        hidden=hidden,
        hidden_key=hidden_key,
        hidden_start=hidden_start,
        hidden_end=hidden_end,
        dot_key=dot_key,
        slash_key=slash_key,
        dash_key=dash_key,
        on_fail=on_fail,
    )

    return formatter.format(cnpj_string)
