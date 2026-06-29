"""Behavioral spec for ``CnpjGeneratorOptions``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-gen/tests/cnpj-generator-options.spec.ts``) and the PHP
reference suite
(``php/packages/cnpj-gen/tests/specs/CnpjGeneratorOptions.spec.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` nullish option values (JavaScript-only; Python uses ``None``).
- PHP ``CnpjType`` enum assignment cases (Python accepts string literals per
  ``AGENTS.md`` §8; enum-specific setter cases are covered by string tests).
"""

import re

import pytest
from cnpj_gen import (
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
)

DEFAULT_PARAMETERS = {
    "format": CnpjGeneratorOptions.DEFAULT_FORMAT,
    "prefix": CnpjGeneratorOptions.DEFAULT_PREFIX,
    "type": CnpjGeneratorOptions.DEFAULT_TYPE,
}

REPEATED_DIGIT_PREFIXES = [
    "111111111111",
    "222222222222",
    "333333333333",
    "444444444444",
    "555555555555",
    "666666666666",
    "777777777777",
    "888888888888",
    "999999999999",
]

REPEATED_LETTER_PREFIXES = [
    "AAAAAAAAAAAA",
    "BBBBBBBBBBBB",
    "CCCCCCCCCCCC",
    "DDDDDDDDDDDD",
    "EEEEEEEEEEEE",
    "FFFFFFFFFFFF",
    "GGGGGGGGGGGG",
    "HHHHHHHHHHHH",
    "IIIIIIIIIIII",
    "JJJJJJJJJJJJ",
    "KKKKKKKKKKKK",
    "LLLLLLLLLLLL",
    "MMMMMMMMMMMM",
    "NNNNNNNNNNNN",
    "OOOOOOOOOOOO",
    "PPPPPPPPPPPP",
    "QQQQQQQQQQQQ",
    "RRRRRRRRRRRR",
    "SSSSSSSSSSSS",
    "TTTTTTTTTTTT",
    "UUUUUUUUUUUU",
    "VVVVVVVVVVVV",
    "WWWWWWWWWWWW",
    "XXXXXXXXXXXX",
    "YYYYYYYYYYYY",
    "ZZZZZZZZZZZZ",
]

TYPE_INVALID_MESSAGE = (
    'CNPJ generator option "type" accepts only the following values: '
    '"alphabetic", "alphanumeric", "numeric". Got "something".'
)


def _raises_message(exception_type, message: str):
    return pytest.raises(exception_type, match=re.escape(message))


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def describe_cnpj_generator_options():
    def describe_constructor():
        def describe_when_called_with_no_parameters():
            def it_sets_all_options_to_default_values():
                options = CnpjGeneratorOptions()

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters_with_null_values():
            def it_sets_all_options_to_default_values():
                options = CnpjGeneratorOptions(
                    {
                        "format": None,
                        "prefix": None,
                        "type": None,
                    }
                )

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters():
            def it_sets_all_options_to_the_provided_values():
                parameters = {
                    "format": True,
                    "prefix": "12345",
                    "type": "numeric",
                }

                options = CnpjGeneratorOptions(parameters)

                _assert_options_snapshots_match(options.all, parameters)

        def describe_when_called_with_some_parameters():
            def it_sets_only_the_provided_non_nullish_values():
                options = CnpjGeneratorOptions({"type": "numeric"})

                _assert_options_snapshots_match(
                    options.all,
                    {
                        **DEFAULT_PARAMETERS,
                        "type": "numeric",
                    },
                )

        def describe_when_called_with_a_cnpj_generator_options_instance():
            def it_sets_a_new_instance_with_the_same_values():
                original_options = CnpjGeneratorOptions(
                    {
                        "format": True,
                        "prefix": "12345",
                        "type": "numeric",
                    }
                )

                options = CnpjGeneratorOptions(original_options)

                assert options is not original_options
                _assert_options_snapshots_match(options.all, original_options.all)

        def describe_when_called_with_overrides_parameters():
            def it_uses_last_param_option_with_2_params():
                options = CnpjGeneratorOptions(
                    {"prefix": "12345"},
                    {"prefix": "11222333"},
                )

                assert options.prefix == "11222333"

            def it_uses_last_param_option_with_1_mapping_and_1_instance():
                options = CnpjGeneratorOptions(
                    {"prefix": "12345"},
                    CnpjGeneratorOptions({"prefix": "11222333"}),
                )

                assert options.prefix == "11222333"

            def it_uses_last_param_option_with_5_params():
                options = CnpjGeneratorOptions(
                    {"prefix": "123456780009"},
                    {"prefix": "11"},
                    {"prefix": "22333"},
                    {"prefix": "44555666"},
                    {"prefix": "77888999"},
                )

                assert options.prefix == "77888999"

    def describe_format_property():
        def describe_when_setting_to_a_boolean_value():
            def it_sets_format_to_true():
                options = CnpjGeneratorOptions({"format": False})

                options.format = True

                assert options.format is True

            def it_sets_format_to_false():
                options = CnpjGeneratorOptions({"format": True})

                options.format = False

                assert options.format is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjGeneratorOptions(
                    {"format": not CnpjGeneratorOptions.DEFAULT_FORMAT}
                )

                options.format = None

                assert options.format == DEFAULT_PARAMETERS["format"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CnpjGeneratorOptions({"format": False})

                options.format = {"not": "a boolean"}  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_truthy_string_value_to_true():
                options = CnpjGeneratorOptions({"format": False})

                options.format = "not a boolean"  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_truthy_number_value_to_true():
                options = CnpjGeneratorOptions({"format": False})

                options.format = 123  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_empty_string_value_to_false():
                options = CnpjGeneratorOptions({"format": False})

                options.format = ""  # type: ignore[assignment]

                assert options.format is False

            def it_coerces_zero_number_value_to_false():
                options = CnpjGeneratorOptions({"format": False})

                options.format = 0  # type: ignore[assignment]

                assert options.format is False

    def describe_prefix_property():
        def describe_when_setting_to_a_valid_string_value():
            def it_sets_prefix_to_the_provided_value():
                options = CnpjGeneratorOptions({"prefix": "12345"})

                options.prefix = "11222333"

                assert options.prefix == "11222333"

            def it_strips_non_alphanumeric_characters_from_the_provided_value():
                options = CnpjGeneratorOptions()

                options.prefix = "12.ABC.def/0001"

                assert options.prefix == "12ABCDEF0001"

            def it_uppercases_a_lowercase_only_prefix():
                options = CnpjGeneratorOptions()

                options.prefix = "abc123"

                assert options.prefix == "ABC123"

            def it_ignores_extra_characters_from_the_provided_value():
                options = CnpjGeneratorOptions()

                options.prefix = "12ABC345678910"

                assert options.prefix == "12ABC3456789"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjGeneratorOptions({"prefix": "12345"})

                options.prefix = None

                assert options.prefix == DEFAULT_PARAMETERS["prefix"]

        def describe_when_setting_to_a_non_string_value():
            def it_throws_cnpj_generator_options_type_error_with_an_object():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "prefix" must be of type string. Got object.',
                ):
                    options.prefix = {"not": "a string"}  # type: ignore[assignment]

            def it_throws_cnpj_generator_options_type_error_with_a_number():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "prefix" must be of type string. Got integer number.',
                ):
                    options.prefix = 123  # type: ignore[assignment]

            def it_throws_cnpj_generator_options_type_error_with_a_boolean():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "prefix" must be of type string. Got boolean.',
                ):
                    options.prefix = True  # type: ignore[assignment]

        def describe_when_setting_to_an_invalid_string():
            def it_throws_cnpj_generator_option_prefix_invalid_exception_with_base_id_all_zeros():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionPrefixInvalidException,
                    'CNPJ generator option "prefix" with value "00000000" is invalid. Zeroed base ID is not eligible.',
                ):
                    options.prefix = "00000000"

            def it_throws_cnpj_generator_option_prefix_invalid_exception_with_branch_id_all_zeros():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionPrefixInvalidException,
                    'CNPJ generator option "prefix" with value "123456780000" is invalid. Zeroed branch ID is not eligible.',
                ):
                    options.prefix = "123456780000"

            @pytest.mark.parametrize("prefix", REPEATED_DIGIT_PREFIXES)
            def it_throws_cnpj_generator_option_prefix_invalid_exception_with_repeated_digits(
                prefix,
            ):
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionPrefixInvalidException,
                    f'CNPJ generator option "prefix" with value "{prefix}" is invalid. Repeated digits are not considered valid.',
                ):
                    options.prefix = prefix

            @pytest.mark.parametrize("prefix", REPEATED_LETTER_PREFIXES)
            def it_does_not_throw_exception_with_repeated_letters(prefix):
                options = CnpjGeneratorOptions()

                options.prefix = prefix

                assert options.prefix == prefix

    def describe_type_property():
        def describe_when_setting_to_a_valid_option_value():
            @pytest.mark.parametrize(
                "type_value", ["alphabetic", "alphanumeric", "numeric"]
            )
            def it_sets_type_to_the_value(type_value):
                options = CnpjGeneratorOptions({"type": type_value})

                options.type = type_value

                assert options.type == type_value

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjGeneratorOptions({"type": "numeric"})

                options.type = None

                assert options.type == DEFAULT_PARAMETERS["type"]

        def describe_when_setting_to_a_non_string_value():
            def it_throws_cnpj_generator_options_type_error_with_an_object():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "type" must be of type str. Got object.',
                ):
                    options.type = {"not": "a string"}  # type: ignore[assignment]

            def it_throws_cnpj_generator_options_type_error_with_a_number():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "type" must be of type str. Got integer number.',
                ):
                    options.type = 123  # type: ignore[assignment]

            def it_throws_cnpj_generator_options_type_error_with_a_boolean():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionsTypeError,
                    'CNPJ generator option "type" must be of type str. Got boolean.',
                ):
                    options.type = True  # type: ignore[assignment]

        def describe_when_setting_to_an_invalid_option():
            def it_throws_cnpj_generator_option_type_invalid_exception_with_unexpected_value():
                options = CnpjGeneratorOptions()

                with _raises_message(
                    CnpjGeneratorOptionTypeInvalidException,
                    TYPE_INVALID_MESSAGE,
                ):
                    options.type = "something"  # type: ignore[assignment]

    def describe_all_getter():
        def it_returns_all_properties():
            options = CnpjGeneratorOptions()
            snapshot = options.all

            assert isinstance(snapshot["format"], bool)
            assert isinstance(snapshot["prefix"], str)
            assert isinstance(snapshot["type"], str)
