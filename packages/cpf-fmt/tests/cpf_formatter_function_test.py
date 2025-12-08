from collections.abc import Callable

from cpf_fmt import cpf_fmt

from .cpf_formatter_test_cases import CpfFormatterTestCases


class CpfFormatterFunctionTest(CpfFormatterTestCases):
    def format(
        self,
        cpf_string: str,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> str:
        return cpf_fmt(
            cpf_string,
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            dash_key,
            escape,
            on_fail,
        )
