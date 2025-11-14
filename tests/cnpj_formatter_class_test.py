from collections.abc import Callable

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions
from cnpj_formatter_test_cases import CnpjFormatterTestCases


class TestCnpjFormatterClass(CnpjFormatterTestCases):
    def setup_method(self):
        self.formatter = CnpjFormatter()

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
        return self.formatter.format(
            cnpj_string,
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

    def test_object_oriented_get_options(self):
        options = self.formatter.get_options()

        assert isinstance(options, CnpjFormatterOptions)
        assert options.is_escaped() is False
        assert options.is_hidden() is False
        assert options.get_hidden_key() == "*"
        assert options.get_hidden_start() == 5
        assert options.get_hidden_end() == 13
        assert options.get_dot_key() == "."
        assert options.get_slash_key() == "/"
        assert options.get_dash_key() == "-"
