"""Behavioral spec for ``CpfFormatter``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-fmt/tests/cpf-formatter.spec.ts``) and the PHP reference
suite (``php/packages/cpf-fmt/tests/CpfFormatterTestCases.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` input type (JavaScript-only; Python uses ``None`` with
  ``actual_type`` ``"NoneType"`` via ``lacus.utils.describe_type``).
- CNPJ-only letter/alphanumeric input scenarios (CPF accepts digits only).
"""

import re

import pytest
from cpf_fmt import (
    CpfFormatter,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
    CpfFormatterOptions,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfFormatterOptionsTypeError,
)

INVALID_LENGTH_CASES = [
    ("1", 1),
    ("12", 2),
    ("123", 3),
    ("1234", 4),
    ("12345", 5),
    ("123456", 6),
    ("1234567", 7),
    ("12345678", 8),
    ("123456789", 9),
    ("1234567890", 10),
    ("123456789012", 12),
    ("1234567890123", 13),
]

INVALID_TYPE_CASES = [
    (None, "NoneType"),
    (42, "integer number"),
    (3.14, "float number"),
    (False, "boolean"),
    (True, "boolean"),
    ({}, "dict"),
]


def _default_options_snapshot() -> dict:
    return CpfFormatterOptions().all


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def _format(cpf_input, options=None, **kwargs):
    return CpfFormatter().format(cpf_input, options, **kwargs)


def describe_cpf_formatter():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_default_options():
                formatter = CpfFormatter()

                _assert_options_snapshots_match(
                    formatter.options.all, _default_options_snapshot()
                )

        def describe_when_called_with_arguments():
            def it_sets_to_default_options_with_empty_mapping():
                formatter = CpfFormatter({})

                _assert_options_snapshots_match(
                    formatter.options.all, _default_options_snapshot()
                )

            def it_uses_the_provided_options_instance():
                options = CpfFormatterOptions()

                formatter = CpfFormatter(options)

                assert formatter.options is options

            def it_overrides_the_default_options_with_the_provided_ones_literal_mapping():
                options = {
                    "hidden": True,
                    "dot_key": "_",
                    "encode": True,
                }

                formatter = CpfFormatter(options)

                for key, value in options.items():
                    assert formatter.options.all[key] == value

            def it_overrides_the_default_options_with_the_provided_ones_options_instance():
                options = CpfFormatterOptions(
                    {
                        "hidden": True,
                        "dot_key": "_",
                        "encode": True,
                    }
                )

                formatter = CpfFormatter(options)

                _assert_options_snapshots_match(formatter.options.all, options.all)

            def it_exposes_default_options_through_the_options_property():
                formatter = CpfFormatter()
                options = formatter.options

                assert isinstance(options, CpfFormatterOptions)
                _assert_options_snapshots_match(
                    options.all, _default_options_snapshot()
                )

    def describe_format_method():
        def describe_when_input_is_a_string():
            def it_handles_the_input_with_no_formatting():
                assert _format("12345678910") == "123.456.789-10"

            def it_handles_the_input_with_standard_formatting():
                assert _format("123.456.789-10") == "123.456.789-10"

            def it_handles_the_input_with_custom_formatting():
                assert _format("123 456 789 _ 10") == "123.456.789-10"

            def it_handles_input_with_dashes():
                assert _format("809-765-110-61") == "809.765.110-61"

            def it_handles_input_with_spaces():
                assert _format("809 765 110 61") == "809.765.110-61"

            def it_handles_input_with_trailing_space():
                assert _format("80976511061 ") == "809.765.110-61"

            def it_handles_input_with_leading_space():
                assert _format(" 80976511061") == "809.765.110-61"

            def it_handles_input_with_individual_dots():
                assert _format("8.0.9.7.6.5.1.1.0.6.1") == "809.765.110-61"

            def it_handles_input_with_individual_dashes():
                assert _format("8-0-9-7-6-5-1-1-0-6-1") == "809.765.110-61"

            def it_handles_input_with_individual_spaces():
                assert _format("8 0 9 7 6 5 1 1 0 6 1") == "809.765.110-61"

            def it_strips_non_digit_characters():
                assert _format("80976511061abc") == "809.765.110-61"

            def it_strips_mixed_non_digit_separators():
                assert _format("809765110 dv 61") == "809.765.110-61"

        def describe_when_input_is_a_sequence_of_strings():
            def it_handles_sequence_of_only_digits():
                result = _format(
                    [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "1",
                        "0",
                    ]
                )

                assert result == "123.456.789-10"

            def it_handles_sequence_of_single_item():
                assert _format(["12345678910"]) == "123.456.789-10"

            def it_handles_sequence_of_grouped_digits():
                assert _format(["123", "456", "789", "10"]) == "123.456.789-10"

            def it_handles_sequence_of_grouped_digits_and_punctuation():
                assert (
                    _format(["123", ".", "456", ".", "789", "-", "10"])
                    == "123.456.789-10"
                )

        def describe_when_input_is_not_string_or_sequence_of_strings():
            @pytest.mark.parametrize(("input_value", "actual_type"), INVALID_TYPE_CASES)
            def it_raises_cpf_formatter_input_type_error(input_value, actual_type):
                with pytest.raises(CpfFormatterInputTypeError) as exc_info:
                    _format(input_value)

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input is input_value
                assert error.actual_type == actual_type

            def it_raises_cpf_formatter_input_type_error_for_sequences_with_non_strings():
                input_value = ["123", 45, "6789010"]

                with pytest.raises(CpfFormatterInputTypeError) as exc_info:
                    _format(input_value)

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input == input_value

        def describe_when_sanitized_input_length_is_not_11():
            @pytest.mark.parametrize(("input_value", "length"), INVALID_LENGTH_CASES)
            def it_fails_with_cpf_formatter_input_length_exception(input_value, length):
                def on_fail(value, error):
                    assert isinstance(error, CpfFormatterInputLengthException)
                    assert len(error.evaluated_input) == length
                    assert error.actual_input == value

                    return f'ERROR: "{value}"'

                assert (
                    _format(input_value, {"on_fail": on_fail})
                    == f'ERROR: "{input_value}"'
                )

            def it_returns_the_string_from_on_fail():
                assert (
                    _format("abc", {"on_fail": lambda value, _error: value.upper()})
                    == "ABC"
                )

            def it_returns_empty_string_from_default_on_fail():
                assert _format("abc") == ""

        def describe_when_on_fail_does_not_return_a_string():
            @pytest.mark.parametrize(
                ("return_value", "actual_type"),
                [
                    (42, "integer number"),
                    (True, "boolean"),
                    (None, "NoneType"),
                    ({}, "dict"),
                ],
            )
            def it_raises_cpf_formatter_options_type_error(return_value, actual_type):
                with pytest.raises(CpfFormatterOptionsTypeError) as exc_info:
                    _format(
                        "abc",
                        {"on_fail": lambda _value, _error: return_value},
                    )

                error = exc_info.value

                assert error.option_name == "on_fail"
                assert error.actual_input is return_value
                assert error.actual_type == actual_type
                assert error.expected_type == "string"
                assert (
                    str(error)
                    == f'CPF formatting option "on_fail" must be of type string. Got {actual_type}.'
                )

        def describe_when_using_per_call_keyword_overrides():
            def it_applies_keyword_overrides_without_mutating_default_options():
                formatter = CpfFormatter({"dot_key": " "})

                assert formatter.format("12345678910", hidden=True).count("*") > 0
                assert formatter.options.hidden is False
                assert formatter.options.dot_key == " "

            def it_gives_options_precedence_over_named_keyword_arguments():
                assert (
                    _format(
                        "12345678910",
                        {"hidden": False},
                        hidden=True,
                    ).count("*")
                    == 0
                )

            def it_applies_encode_via_keyword_override():
                assert (
                    _format("12345678910", encode=True, dash_key="/")
                    == "123.456.789%2F10"
                )

            def it_applies_on_fail_via_keyword_override():
                assert (
                    _format("abc", on_fail=lambda _value, _error: "fallback")
                    == "fallback"
                )

        def describe_when_using_hidden_option():
            default_hidden_length = (
                CpfFormatterOptions.DEFAULT_HIDDEN_END
                - CpfFormatterOptions.DEFAULT_HIDDEN_START
                + 1
            )
            standard_cpf_format_length = len("000.000.000-00")

            def it_replaces_some_digits_with_asterisk_when_simply_true():
                result = _format("12345678910", {"hidden": True})
                hidden_chars = [char for char in result if char == "*"]

                assert len(hidden_chars) == default_hidden_length
                assert len(result) == standard_cpf_format_length

            def it_replaces_digits_with_asterisk_in_a_given_range():
                result = _format(
                    "12345678910",
                    {"hidden": True, "hidden_start": 3, "hidden_end": 7},
                )

                assert result == "123.***.**9-10"
                assert len(result) == standard_cpf_format_length

            def it_replaces_digits_with_a_custom_key():
                result = _format("12345678910", {"hidden": True, "hidden_key": "#"})
                hidden_chars = [char for char in result if char == "#"]

                assert "*" not in result
                assert len(hidden_chars) == default_hidden_length
                assert len(result) == standard_cpf_format_length

            def it_replaces_digits_with_a_custom_zero_width_key():
                result = _format("12345678910", {"hidden": True, "hidden_key": ""})

                assert "*" not in result
                assert len(result) == standard_cpf_format_length - default_hidden_length

            def it_replaces_digits_with_a_custom_multi_character_key():
                result = _format("12345678910", {"hidden": True, "hidden_key": "[]"})
                bracket_chars = "".join(char for char in result if char in {"[", "]"})

                assert "*" not in result
                assert re.fullmatch(
                    rf"(\[\]){{{default_hidden_length}}}", bracket_chars
                )
                assert len(result) == standard_cpf_format_length + default_hidden_length

            def it_masks_from_a_custom_start_index():
                assert (
                    _format(
                        "80976511061",
                        {"hidden": True, "hidden_start": 6},
                    )
                    == "809.765.***-**"
                )

            def it_masks_up_to_a_custom_end_index():
                assert (
                    _format(
                        "80976511061",
                        {"hidden": True, "hidden_end": 8},
                    )
                    == "809.***.***-61"
                )

            def it_masks_a_full_custom_range():
                assert (
                    _format(
                        "80976511061",
                        {"hidden": True, "hidden_start": 0, "hidden_end": 8},
                    )
                    == "***.***.***-61"
                )

            def it_swaps_reversed_hidden_range_values():
                assert (
                    _format(
                        "80976511061",
                        {"hidden": True, "hidden_start": 9, "hidden_end": 3},
                    )
                    == "809.***.***-*1"
                )

            def it_masks_with_a_custom_key_and_start_index():
                assert (
                    _format(
                        "80976511061",
                        {"hidden": True, "hidden_key": "#", "hidden_start": 6},
                    )
                    == "809.765.###-##"
                )

            def it_raises_hidden_range_invalid_exception_for_start_below_zero():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    _format("12345678910", {"hidden": True, "hidden_start": -1})

            def it_raises_hidden_range_invalid_exception_for_start_above_10():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    _format("12345678910", {"hidden": True, "hidden_start": 11})

            def it_raises_hidden_range_invalid_exception_for_end_below_zero():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    _format("12345678910", {"hidden": True, "hidden_end": -1})

            def it_raises_hidden_range_invalid_exception_for_end_above_10():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    _format("12345678910", {"hidden": True, "hidden_end": 11})

        def describe_when_customizing_punctuation():
            def it_replaces_dots_with_a_custom_key():
                assert _format("12345678910", {"dot_key": " "}) == "123 456 789-10"

            def it_replaces_dots_with_a_custom_zero_width_key():
                assert _format("12345678910", {"dot_key": ""}) == "123456789-10"

            def it_replaces_dots_with_a_custom_multi_character_key():
                assert _format("12345678910", {"dot_key": "[]"}) == "123[]456[]789-10"

            def it_replaces_dash_with_a_custom_key():
                assert _format("12345678910", {"dash_key": "_"}) == "123.456.789_10"

            def it_replaces_dash_with_a_custom_zero_width_key():
                assert _format("12345678910", {"dash_key": ""}) == "123.456.78910"

            def it_replaces_dash_with_a_custom_multi_character_key():
                assert (
                    _format("12345678910", {"dash_key": " dv "}) == "123.456.789 dv 10"
                )

            def it_uses_dash_key_as_dot_delimiter():
                assert _format("80976511061", {"dash_key": "."}) == "809.765.110.61"

            def it_removes_all_delimiters():
                assert (
                    _format("809.765.110-61", {"dot_key": "", "dash_key": ""})
                    == "80976511061"
                )

        def describe_when_using_escape_option():
            def it_escapes_html_special_characters():
                result = _format(
                    "12345678910",
                    {
                        "dot_key": "&",
                        "dash_key": "<>",
                        "escape": True,
                    },
                )

                assert result == "123&amp;456&amp;789&lt;&gt;10"

            def it_escapes_custom_delimiters_from_php_reference_suite():
                result = _format(
                    "80976511061",
                    {
                        "dot_key": "<",
                        "dash_key": ">",
                        "escape": True,
                    },
                )

                assert result == "809&lt;765&lt;110&gt;61"

        def describe_when_using_encode_option():
            def it_url_encodes_the_result():
                assert (
                    _format("12345678910", {"dash_key": "/", "encode": True})
                    == "123.456.789%2F10"
                )

        def describe_edge_cases():
            def it_replaces_hidden_key_dot_key_and_dash_key_with_multi_character_values():
                result = _format(
                    "12345678910",
                    {
                        "hidden": True,
                        "hidden_start": 3,
                        "hidden_end": 7,
                        "hidden_key": "[*]",
                        "dot_key": "[.]",
                        "dash_key": "[-]",
                    },
                )

                assert result == "123[.][*][*][*][.][*][*]9[-]10"
