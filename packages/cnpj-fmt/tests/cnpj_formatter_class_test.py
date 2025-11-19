from collections.abc import Callable

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions

from .cnpj_formatter_test_cases import CnpjFormatterTestCases


class CnpjFormatterClassTest(CnpjFormatterTestCases):
    def setup_method(self):
        self.formatter = CnpjFormatter()

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
        return self.formatter.format(
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

    def test_object_oriented_get_options(self):
        options = self.formatter.options

        assert isinstance(options, CnpjFormatterOptions)
        assert options.hidden is False
        assert options.hidden_key == "*"
        assert options.hidden_start == 5
        assert options.hidden_end == 13
        assert options.dot_key == "."
        assert options.slash_key == "/"
        assert options.dash_key == "-"
        assert options.escape is False
        assert callable(options.on_fail)
