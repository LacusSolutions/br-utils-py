"""Behavioral spec for ``CnpjFormatter``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-fmt/tests/cnpj-formatter.spec.ts``) and the PHP reference
suite (``php/packages/cnpj-fmt/tests/specs/CnpjFormatter.spec.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` input type (JavaScript-only; Python uses ``None`` with
  ``actual_type`` ``"NoneType"`` via ``lacus.utils.describe_type``).
"""

import re

import pytest
from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
    CnpjFormatterOptions,
    CnpjFormatterOptionsTypeError,
)

INVALID_LENGTH_CASES = [
    ("1", 1),
    ("12", 2),
    ("12.A", 3),
    ("12.AB", 4),
    ("12.ABC", 5),
    ("12.ABC.3", 6),
    ("12.ABC.34", 7),
    ("12.ABC.345", 8),
    ("12.ABC.345/0", 9),
    ("12.ABC.345/00", 10),
    ("12.ABC.345/00D", 11),
    ("12.ABC.345/00DE", 12),
    ("12.ABC.345/00DE-6", 13),
    ("12.ABC.345/00DE-678", 15),
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
    return CnpjFormatterOptions().all


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def _format(cnpj_input, options=None):
    return CnpjFormatter().format(cnpj_input, options)


def describe_cnpj_formatter():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_default_options():
                formatter = CnpjFormatter()

                _assert_options_snapshots_match(
                    formatter.options.all, _default_options_snapshot()
                )

        def describe_when_called_with_arguments():
            def it_sets_to_default_options_with_empty_mapping():
                formatter = CnpjFormatter({})

                _assert_options_snapshots_match(
                    formatter.options.all, _default_options_snapshot()
                )

            def it_uses_the_provided_options_instance():
                options = CnpjFormatterOptions()

                formatter = CnpjFormatter(options)

                assert formatter.options is options

            def it_overrides_the_default_options_with_the_provided_ones_literal_mapping():
                options = {
                    "hidden": True,
                    "slash_key": "|",
                    "dot_key": "_",
                    "encode": True,
                }

                formatter = CnpjFormatter(options)

                for key, value in options.items():
                    assert formatter.options.all[key] == value

            def it_overrides_the_default_options_with_the_provided_ones_options_instance():
                options = CnpjFormatterOptions(
                    {
                        "hidden": True,
                        "slash_key": "|",
                        "dot_key": "_",
                        "encode": True,
                    }
                )

                formatter = CnpjFormatter(options)

                _assert_options_snapshots_match(formatter.options.all, options.all)

    def describe_format_method():
        def describe_when_input_is_a_string_with_only_digits():
            def it_handles_the_input_with_no_formatting():
                assert _format("12345678000910") == "12.345.678/0009-10"

            def it_handles_the_input_with_standard_formatting():
                assert _format("12.345.678/0009-10") == "12.345.678/0009-10"

            def it_handles_the_input_with_custom_formatting():
                assert _format("12 345 678 | 0009 _ 10") == "12.345.678/0009-10"

        def describe_when_input_is_a_string_with_only_letters():
            def it_handles_the_input_with_no_formatting():
                assert _format("ABCDEFGHIJKLMN") == "AB.CDE.FGH/IJKL-MN"

            def it_handles_the_input_with_standard_formatting():
                assert _format("AB.CDE.FGH/IJKL-MN") == "AB.CDE.FGH/IJKL-MN"

            def it_handles_the_input_with_custom_formatting():
                assert _format("AB CDE FGH | IJKL _ MN") == "AB.CDE.FGH/IJKL-MN"

            def it_converts_lowercase_letters_to_uppercase():
                assert _format("AbCdEfGhIjKlMn") == "AB.CDE.FGH/IJKL-MN"

        def describe_when_input_is_a_string_with_mixed_digits_and_letters():
            def it_handles_the_input_with_no_formatting():
                assert _format("12ABC34500DE00") == "12.ABC.345/00DE-00"

            def it_handles_the_input_with_standard_formatting():
                assert _format("12.ABC.345/00DE-00") == "12.ABC.345/00DE-00"

            def it_handles_the_input_with_custom_formatting():
                assert _format("12 ABC 345 | 00DE _ 00") == "12.ABC.345/00DE-00"

            def it_converts_lowercase_letters_to_uppercase():
                assert _format("12abcDEF00eF00") == "12.ABC.DEF/00EF-00"

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
                        "0",
                        "0",
                        "0",
                        "9",
                        "1",
                        "0",
                    ]
                )

                assert result == "12.345.678/0009-10"

            def it_handles_sequence_of_single_item_with_only_digits():
                assert _format(["12345678000910"]) == "12.345.678/0009-10"

            def it_handles_sequence_of_grouped_digits():
                assert (
                    _format(["12", "345", "678", "0009", "10"]) == "12.345.678/0009-10"
                )

            def it_handles_sequence_of_grouped_digits_and_punctuation():
                assert (
                    _format(["12", ".", "345", ".", "678", "/", "0009", "-", "10"])
                    == "12.345.678/0009-10"
                )

            def it_handles_sequence_of_only_letters():
                result = _format(
                    [
                        "A",
                        "B",
                        "C",
                        "D",
                        "E",
                        "F",
                        "G",
                        "H",
                        "I",
                        "J",
                        "K",
                        "L",
                        "M",
                        "N",
                    ]
                )

                assert result == "AB.CDE.FGH/IJKL-MN"

            def it_handles_sequence_of_single_item_with_only_letters():
                assert _format(["ABCDEFGHIJKLMN"]) == "AB.CDE.FGH/IJKL-MN"

            def it_handles_sequence_of_lowercase_letters():
                assert _format(["abcdefghijklmn"]) == "AB.CDE.FGH/IJKL-MN"

            def it_handles_sequence_of_grouped_letters():
                assert (
                    _format(["AB", "CDE", "FGH", "IJKL", "MN"]) == "AB.CDE.FGH/IJKL-MN"
                )

            def it_handles_sequence_of_grouped_letters_and_punctuation():
                assert (
                    _format(["AB", ".", "CDE", ".", "FGH", "/", "IJKL", "-", "MN"])
                    == "AB.CDE.FGH/IJKL-MN"
                )

            def it_handles_sequence_of_mixed_digits_and_letters():
                result = _format(
                    [
                        "1",
                        "2",
                        "a",
                        "b",
                        "c",
                        "D",
                        "E",
                        "F",
                        "0",
                        "0",
                        "g",
                        "H",
                        "3",
                        "4",
                    ]
                )

                assert result == "12.ABC.DEF/00GH-34"

            def it_handles_sequence_of_single_item_with_mixed_digits_and_letters():
                assert _format(["12abcDEF00gH34"]) == "12.ABC.DEF/00GH-34"

            def it_handles_sequence_of_grouped_digits_and_letters():
                assert (
                    _format(["12", "abc", "DEF", "00gH", "34"]) == "12.ABC.DEF/00GH-34"
                )

            def it_handles_sequence_of_grouped_digits_letters_and_punctuation():
                assert (
                    _format(["12", ".", "abc", ".", "DEF", "/", "00gH", "-", "34"])
                    == "12.ABC.DEF/00GH-34"
                )

        def describe_when_input_is_not_string_or_sequence_of_strings():
            @pytest.mark.parametrize(("input_value", "actual_type"), INVALID_TYPE_CASES)
            def it_raises_cnpj_formatter_input_type_error(input_value, actual_type):
                with pytest.raises(CnpjFormatterInputTypeError) as exc_info:
                    _format(input_value)

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input is input_value
                assert error.actual_type == actual_type

            def it_raises_cnpj_formatter_input_type_error_for_sequences_with_non_strings():
                input_value = ["12", 34, "56"]

                with pytest.raises(CnpjFormatterInputTypeError) as exc_info:
                    _format(input_value)

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input == input_value

        def describe_when_sanitized_input_length_is_not_14():
            @pytest.mark.parametrize(("input_value", "length"), INVALID_LENGTH_CASES)
            def it_fails_with_cnpj_formatter_input_length_exception(
                input_value, length
            ):
                def on_fail(value, error):
                    assert isinstance(error, CnpjFormatterInputLengthException)
                    assert len(error.evaluated_input) == length
                    assert error.actual_input == value

                    return f'ERROR: "{value}"'

                _format(input_value, {"on_fail": on_fail})

            def it_returns_the_string_from_on_fail():
                assert (
                    _format("short", {"on_fail": lambda _value, _error: "fallback"})
                    == "fallback"
                )

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
            def it_raises_cnpj_formatter_options_type_error(return_value, actual_type):
                with pytest.raises(CnpjFormatterOptionsTypeError) as exc_info:
                    _format(
                        "short",
                        {"on_fail": lambda _value, _error: return_value},
                    )

                error = exc_info.value

                assert error.option_name == "on_fail"
                assert error.actual_input is return_value
                assert error.actual_type == actual_type
                assert error.expected_type == "string"
                assert (
                    str(error)
                    == f'CNPJ formatting option "on_fail" must be of type string. Got {actual_type}.'
                )

        def describe_when_using_hidden_option():
            default_hidden_length = (
                CnpjFormatterOptions.DEFAULT_HIDDEN_END
                - CnpjFormatterOptions.DEFAULT_HIDDEN_START
                + 1
            )
            standard_cnpj_format_length = len("00.000.000/0000-00")

            def it_replaces_some_characters_with_asterisk_when_simply_true():
                result = _format("12ABC34500DE99", {"hidden": True})
                hidden_chars = [char for char in result if char == "*"]

                assert len(hidden_chars) == default_hidden_length
                assert len(result) == standard_cnpj_format_length

            def it_replaces_characters_with_asterisk_in_a_given_range():
                result = _format(
                    "12ABC34500DE99",
                    {"hidden": True, "hidden_start": 8, "hidden_end": 11},
                )

                assert result == "12.ABC.345/****-99"
                assert len(result) == standard_cnpj_format_length

            def it_replaces_characters_with_a_custom_key():
                result = _format("12ABC34500DE99", {"hidden": True, "hidden_key": "#"})
                hidden_chars = [char for char in result if char == "#"]

                assert "*" not in result
                assert len(hidden_chars) == default_hidden_length
                assert len(result) == standard_cnpj_format_length

            def it_replaces_characters_with_a_custom_zero_width_key():
                result = _format("12ABC34500DE99", {"hidden": True, "hidden_key": ""})

                assert "*" not in result
                assert (
                    len(result) == standard_cnpj_format_length - default_hidden_length
                )

            def it_replaces_characters_with_a_custom_multi_character_key():
                result = _format("12ABC34500DE99", {"hidden": True, "hidden_key": "[]"})
                bracket_chars = "".join(char for char in result if char in {"[", "]"})

                assert "*" not in result
                assert re.fullmatch(
                    rf"(\[\]){{{default_hidden_length}}}", bracket_chars
                )
                assert (
                    len(result) == standard_cnpj_format_length + default_hidden_length
                )

        def describe_when_customizing_punctuation():
            def it_replaces_dots_with_a_custom_key():
                assert (
                    _format("12ABC34500DE99", {"dot_key": " "}) == "12 ABC 345/00DE-99"
                )

            def it_replaces_dots_with_a_custom_zero_width_key():
                assert _format("12ABC34500DE99", {"dot_key": ""}) == "12ABC345/00DE-99"

            def it_replaces_dots_with_a_custom_multi_character_key():
                assert (
                    _format("12ABC34500DE99", {"dot_key": "[]"})
                    == "12[]ABC[]345/00DE-99"
                )

            def it_replaces_slash_with_a_custom_key():
                assert (
                    _format("12ABC34500DE99", {"slash_key": "|"})
                    == "12.ABC.345|00DE-99"
                )

            def it_replaces_slash_with_a_custom_zero_width_key():
                assert (
                    _format("12ABC34500DE99", {"slash_key": ""}) == "12.ABC.34500DE-99"
                )

            def it_replaces_slash_with_a_custom_multi_character_key():
                assert (
                    _format("12ABC34500DE99", {"slash_key": "[]"})
                    == "12.ABC.345[]00DE-99"
                )

            def it_replaces_dash_with_a_custom_key():
                assert (
                    _format("12ABC34500DE99", {"dash_key": "_"}) == "12.ABC.345/00DE_99"
                )

            def it_replaces_dash_with_a_custom_zero_width_key():
                assert (
                    _format("12ABC34500DE99", {"dash_key": ""}) == "12.ABC.345/00DE99"
                )

            def it_replaces_dash_with_a_custom_multi_character_key():
                assert (
                    _format("12ABC34500DE99", {"dash_key": "[]"})
                    == "12.ABC.345/00DE[]99"
                )

        def describe_when_using_escape_option():
            def it_escapes_html_special_characters():
                result = _format(
                    "12ABC34500DE99",
                    {
                        "dot_key": "&",
                        "slash_key": '"',
                        "dash_key": "<>",
                        "escape": True,
                    },
                )

                assert result == "12&amp;ABC&amp;345&quot;00DE&lt;&gt;99"

        def describe_when_using_encode_option():
            def it_url_encodes_the_result():
                assert (
                    _format("12ABC34500DE99", {"encode": True})
                    == "12.ABC.345%2F00DE-99"
                )

        def describe_edge_cases():
            def it_replaces_hidden_key_dot_key_slash_key_and_dash_key_with_multi_character_values():
                result = _format(
                    "12ABC34500DE99",
                    {
                        "hidden": True,
                        "hidden_start": 5,
                        "hidden_end": 9,
                        "hidden_key": "[*]",
                        "dot_key": "[.]",
                        "slash_key": "[/]",
                        "dash_key": "[-]",
                    },
                )

                assert result == "12[.]ABC[.][*][*][*][/][*][*]DE[-]99"
