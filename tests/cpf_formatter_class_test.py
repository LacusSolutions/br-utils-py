from collections.abc import Callable

from cpf_fmt import (
    DEFAULT_DASH_KEY,
    DEFAULT_DOT_KEY,
    DEFAULT_ESCAPE,
    DEFAULT_HIDDEN,
    DEFAULT_HIDDEN_END,
    DEFAULT_HIDDEN_KEY,
    DEFAULT_HIDDEN_START,
    DEFAULT_ON_FAIL,
    CpfFormatter,
    CpfFormatterOptions,
)

from .cpf_formatter_test_cases import CpfFormatterTestCases


class CpfFormatterClassTest(CpfFormatterTestCases):
    def setup_method(self):
        self.formatter = CpfFormatter()

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
        return self.formatter.format(
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

    def test_object_oriented_get_options(self):
        options = self.formatter.options

        assert isinstance(options, CpfFormatterOptions)
        assert options.hidden is DEFAULT_HIDDEN
        assert options.hidden_key == DEFAULT_HIDDEN_KEY
        assert options.hidden_start == DEFAULT_HIDDEN_START
        assert options.hidden_end == DEFAULT_HIDDEN_END
        assert options.dot_key == DEFAULT_DOT_KEY
        assert options.dash_key == DEFAULT_DASH_KEY
        assert options.escape is DEFAULT_ESCAPE
        assert options.on_fail is DEFAULT_ON_FAIL
