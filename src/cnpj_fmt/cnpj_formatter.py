from collections.abc import Callable

from .cnpj_formatter_options import CnpjFormatterOptions


class CnpjFormatter:
    def __init__(
        self,
        escape: bool | None = None,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        on_fail: Callable | None = None,
    ) -> None:
        self._options = CnpjFormatterOptions(
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

    def format(
        self,
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
        pass

    def get_options(self) -> CnpjFormatterOptions:
        return self._options
