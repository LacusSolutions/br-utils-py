from abc import ABC, abstractmethod
from collections.abc import Callable

import pytest
from cnpj_fmt import CnpjRangeError


class CnpjFormatterTestCases(ABC):
    @abstractmethod
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
        pass

    def test_cnpj_with_dots_and_dash_formats_to_same_format(self):
        cnpj = self.format("03.603.568/0001-95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_without_formatting_formats_to_dots_and_dash(self):
        cnpj = self.format("03603568000195")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_dashes_formats_to_dots_and_dash(self):
        cnpj = self.format("03-603-568-0001-95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_spaces_formats_to_dots_and_dash(self):
        cnpj = self.format("03 603 568 0001 95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_trailing_space_formats_to_dots_and_dash(self):
        cnpj = self.format("03603568000195 ")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_leading_space_formats_to_dots_and_dash(self):
        cnpj = self.format(" 03603568000195")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_individual_dots_formats_to_dots_and_dash(self):
        cnpj = self.format("0.3.6.0.3.5.6.8.0.0.0.1.9.5")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_individual_dashes_formats_to_dots_and_dash(self):
        cnpj = self.format("0-3-6-0-3-5-6-8-0-0-0-1-9-5")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_individual_spaces_formats_to_dots_and_dash(self):
        cnpj = self.format("0 3 6 0 3 5 6 8 0 0 0 1 9 5")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_letters_formats_to_dots_and_dash(self):
        cnpj = self.format("03603568000195abc")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_mixed_characters_formats_correctly(self):
        cnpj = self.format("036035680001 dv 95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_slash_formats_to_dots_and_dash(self):
        cnpj = self.format("03/603/568/0001/95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_spaces_and_slash_formats_to_dots_and_dash(self):
        cnpj = self.format("03 603 568 / 0001 95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_slash_and_dash_mixed_formats_to_dots_and_dash(self):
        cnpj = self.format("03-603-568-0001/95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_letters_and_numbers_formats_to_dots_and_dash(self):
        cnpj = self.format("03603568slash0001dash95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_with_dv_text_formats_to_dots_and_dash(self):
        cnpj = self.format("036035680001 dv 95")

        assert cnpj == "03.603.568/0001-95"

    def test_cnpj_formats_to_custom_delimiters_without_dots(self):
        cnpj = self.format("03603568000195", dot_key="")

        assert cnpj == "03603568/0001-95"

    def test_cnpj_formats_to_custom_delimiters_with_slash_as_colon(self):
        cnpj = self.format("03603568000195", slash_key=":")

        assert cnpj == "03.603.568:0001-95"

    def test_cnpj_formats_to_custom_delimiters_with_dash_as_dot(self):
        cnpj = self.format("03603568000195", dash_key=".")

        assert cnpj == "03.603.568/0001.95"

    def test_cnpj_formats_to_no_delimiters(self):
        cnpj = self.format("03.603.568/0001-95", dot_key="", slash_key="", dash_key="")

        assert cnpj == "03603568000195"

    def test_cnpj_formats_to_custom_delimiters_with_escape(self):
        cnpj = self.format(
            "03603568000195", escape=True, dot_key="<", slash_key="&", dash_key=">"
        )

        assert cnpj == "03&lt;603&lt;568&amp;0001&gt;95"

    def test_cnpj_formats_to_hidden_format(self):
        cnpj = self.format("03603568000195", hidden=True)

        assert cnpj == "03.603.***/****-**"

    def test_cnpj_formats_to_hidden_format_with_start_range(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_start=8)

        assert cnpj == "03.603.568/****-**"

    def test_cnpj_formats_to_hidden_format_with_end_range(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_end=11)

        assert cnpj == "03.603.***/****-95"

    def test_cnpj_formats_to_hidden_format_with_start_and_end_range(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_start=0, hidden_end=7)

        assert cnpj == "**.***.***/0001-95"

    def test_cnpj_formats_to_hidden_format_with_reversed_range(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_start=11, hidden_end=2)

        assert cnpj == "03.***.***/****-95"

    def test_cnpj_formats_to_hidden_format_with_custom_key(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_key="#")

        assert cnpj == "03.603.###/####-##"

    def test_cnpj_formats_to_hidden_format_with_custom_key_and_range(self):
        cnpj = self.format(
            "03603568000195", hidden=True, hidden_key="#", hidden_start=8
        )

        assert cnpj == "03.603.568/####-##"

    def test_invalid_input_falls_back_to_on_fail_callback(self):
        def on_fail(value):
            return value.upper()

        cnpj = self.format("abc", on_fail=on_fail)

        assert cnpj == "ABC"

    def test_option_with_range_start_minus_one_throws_exception(self):
        with pytest.raises(CnpjRangeError):
            self.format("03603568000195", hidden=True, hidden_start=-1)

    def test_option_with_range_start_greater_than_13_throws_exception(self):
        with pytest.raises(CnpjRangeError):
            self.format("03603568000195", hidden=True, hidden_start=14)

    def test_option_with_range_end_minus_one_throws_exception(self):
        with pytest.raises(CnpjRangeError):
            self.format("03603568000195", hidden=True, hidden_end=-1)

    def test_option_with_range_end_greater_than_13_throws_exception(self):
        with pytest.raises(CnpjRangeError):
            self.format("03603568000195", hidden=True, hidden_end=14)

    def test_cnpj_formats_to_hidden_format_with_custom_key_and_start_range(self):
        cnpj = self.format(
            "03603568000195", hidden=True, hidden_key="#", hidden_start=8
        )

        assert cnpj == "03.603.568/####-##"

    def test_cnpj_formats_to_hidden_format_with_custom_key_and_end_range(self):
        cnpj = self.format("03603568000195", hidden=True, hidden_key="#", hidden_end=11)

        assert cnpj == "03.603.###/####-95"

    def test_cnpj_formats_to_hidden_format_with_custom_key_and_both_ranges(self):
        cnpj = self.format(
            "03603568000195", hidden=True, hidden_key="#", hidden_start=0, hidden_end=7
        )

        assert cnpj == "##.###.###/0001-95"

    def test_cnpj_formats_to_hidden_format_with_custom_key_and_reversed_range(self):
        cnpj = self.format(
            "03603568000195", hidden=True, hidden_key="#", hidden_start=11, hidden_end=2
        )

        assert cnpj == "03.###.###/####-95"

    def test_option_with_on_fail_as_not_function_throws_exception(self):
        with pytest.raises(TypeError):
            self.format("03603568000195", on_fail="testing")
