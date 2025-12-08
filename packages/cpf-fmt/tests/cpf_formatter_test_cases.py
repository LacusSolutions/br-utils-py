from abc import ABC, abstractmethod
from collections.abc import Callable

import pytest
from cpf_fmt import CpfFormatterHiddenRangeError


class CpfFormatterTestCases(ABC):
    @abstractmethod
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
        pass

    def test_cpf_with_dots_and_dash_formats_to_same_format(self):
        cpf = self.format("123.456.789-10")

        assert cpf == "123.456.789-10"

    def test_cpf_without_formatting_formats_to_dots_and_dash(self):
        cpf = self.format("12345678910")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_dashes_formats_to_dots_and_dash(self):
        cpf = self.format("123-456-789-10")

        assert cpf == "123.456.789-10"

    def test_cpf_with_spaces_formats_to_dots_and_dash(self):
        cpf = self.format("123 456 789 10")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_ending_trailing_space_formats_to_dots_and_dash(self):
        cpf = self.format("12345678910 ")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_starting_leading_space_formats_to_dots_and_dash(self):
        cpf = self.format(" 12345678910")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_individual_dots_formats_to_dots_and_dash(self):
        cpf = self.format("1.2.3.4.5.6.7.8.9.1.0")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_individual_dashes_formats_to_dots_and_dash(self):
        cpf = self.format("1-2-3-4-5-6-7-8-9-1-0")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_individual_spaces_formats_to_dots_and_dash(self):
        cpf = self.format("1 2 3 4 5 6 7 8 9 1 0")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_letters_formats_to_dots_and_dash(self):
        cpf = self.format("12345678910abc")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_mixed_characters_formats_correctly(self):
        cpf = self.format("123456789 dv 10")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_slash_formats_to_dots_and_dash(self):
        cpf = self.format("123/456/789/10")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_with_spaces_and_slash_formats_to_dots_and_dash(self):
        cpf = self.format("123 456 789 / 10")

        assert cpf == "123.456.789-10", f'Output: "{cpf}", Expected: "123.456.789-10"'

    def test_cpf_formats_to_custom_delimiters_without_dots(self):
        cpf = self.format("12345678910", dot_key="")

        assert cpf == "123456789-10", f'Output: "{cpf}", Expected: "123456789-10"'

    def test_cpf_formats_to_custom_delimiters_with_dash_as_dv_text(self):
        cpf = self.format("12345678910", dash_key=" dv ")

        assert (
            cpf == "123.456.789 dv 10"
        ), f'Output: "{cpf}", Expected: "123.456.789 dv 10"'

    def test_cpf_formats_to_no_delimiters(self):
        cpf = self.format("12345678910", dot_key="", dash_key="")

        assert cpf == "12345678910", f'Output: "{cpf}", Expected: "12345678910"'

    def test_cpf_formats_to_custom_delimiters_with_escape(self):
        cpf = self.format(
            "12345678910",
            escape=True,
            dot_key="&",
            dash_key="<>",
        )

        assert (
            cpf == "123&amp;456&amp;789&lt;&gt;10"
        ), f'Output: "{cpf}", Expected: "123&amp;456&amp;789&lt;1&gt;10"'

    def test_cpf_formats_to_hidden_format(self):
        cpf = self.format("12345678910", hidden=True)

        assert cpf == "123.***.***-**", f'Output: "{cpf}", Expected: "123.456.***-**"'

    def test_cpf_formats_to_hidden_format_with_start_range(self):
        cpf = self.format("12345678910", hidden=True, hidden_start=9)

        assert cpf == "123.456.789-**", f'Output: "{cpf}", Expected: "123.456.789-**"'

    def test_cpf_formats_to_hidden_format_with_end_range(self):
        cpf = self.format("12345678910", hidden=True, hidden_end=8)

        assert cpf == "123.***.***-10", f'Output: "{cpf}", Expected: "123.***.***-10"'

    def test_cpf_formats_to_hidden_format_with_start_and_end_range(self):
        cpf = self.format("12345678910", hidden=True, hidden_start=0, hidden_end=8)

        assert cpf == "***.***.***-10", f'Output: "{cpf}", Expected: "***.***.***-10"'

    def test_cpf_formats_to_hidden_format_with_reversed_range(self):
        cpf = self.format("12345678910", hidden=True, hidden_start=8, hidden_end=3)

        assert cpf == "123.***.***-10", f'Output: "{cpf}", Expected: "123.***.***-10"'

    def test_cpf_formats_to_hidden_format_with_custom_key(self):
        cpf = self.format("12345678910", hidden=True, hidden_key="#")

        assert cpf == "123.###.###-##", f'Output: "{cpf}", Expected: "123.###.###-##"'

    def test_cpf_formats_to_hidden_format_with_custom_key_and_range(self):
        cpf = self.format("12345678910", hidden=True, hidden_key="#", hidden_start=9)

        assert cpf == "123.456.789-##", f'Output: "{cpf}", Expected: "123.456.789-##"'

    def test_invalid_input_falls_back_to_on_fail_callback(self):
        def on_fail(value: str) -> str:
            return value.upper()

        cpf = self.format("abc", on_fail=on_fail)

        assert cpf == "ABC", f'Output: "{cpf}", Expected: "ABC"'

    def test_option_with_range_start_minus_one_throws_exception(self):
        with pytest.raises(CpfFormatterHiddenRangeError):
            self.format("12345678910", hidden=True, hidden_start=-1)

    def test_option_with_range_start_greater_than_10_throws_exception(self):
        with pytest.raises(CpfFormatterHiddenRangeError):
            self.format("12345678910", hidden=True, hidden_start=11)

    def test_option_with_range_end_minus_one_throws_exception(self):
        with pytest.raises(CpfFormatterHiddenRangeError):
            self.format("12345678910", hidden=True, hidden_end=-1)

    def test_option_with_range_end_greater_than_10_throws_exception(self):
        with pytest.raises(CpfFormatterHiddenRangeError):
            self.format("12345678910", hidden=True, hidden_end=11)

    def test_option_with_on_fail_as_not_function_throws_exception(self):
        with pytest.raises(TypeError):
            self.format("12345678910", on_fail="testing")
