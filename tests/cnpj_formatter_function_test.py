from collections.abc import Callable

from cnpj_fmt import cnpj_fmt
from cnpj_formatter_test_cases import CnpjFormatterTestCases


class CnpjFormatterFunctionTest(CnpjFormatterTestCases):
    def format(
        self,
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
        return cnpj_fmt(
            cnpj_string,
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
