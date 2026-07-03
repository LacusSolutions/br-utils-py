"""Behavioral spec for ``CpfGeneratorOptions``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-gen/tests/cpf-generator-options.spec.ts``) and the PHP
reference suite (``php/packages/cpf-gen/tests/CpfGeneratorOptionsTest.php``),
following the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` nullish option values (JavaScript-only; Python uses ``None``).
- PHP ``merge()`` API cases (legacy positional API; target uses constructor
  spread and property setters per JS/TS v3).
- PHP prefix-length ``InvalidArgumentException`` on >9 digits (JS truncates
  silently; canonical behavior per ``AGENTS.md`` §8 #6).
"""

import re

import pytest
from cpf_gen import (
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
    CpfGeneratorOptionsTypeError,
)

DEFAULT_PARAMETERS = {
    "format": CpfGeneratorOptions.DEFAULT_FORMAT,
    "prefix": CpfGeneratorOptions.DEFAULT_PREFIX,
}

REPEATED_DIGIT_PREFIXES = [
    "111111111",
    "222222222",
    "333333333",
    "444444444",
    "555555555",
    "666666666",
    "777777777",
    "888888888",
    "999999999",
]


def _raises_message(exception_type, message: str):
    return pytest.raises(exception_type, match=re.escape(message))


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def describe_cpf_generator_options():
    def describe_constructor():
        def describe_when_called_with_no_parameters():
            def it_sets_all_options_to_default_values():
                options = CpfGeneratorOptions()

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters_with_null_values():
            def it_sets_all_options_to_default_values():
                options = CpfGeneratorOptions(
                    {
                        "format": None,
                        "prefix": None,
                    }
                )

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters():
            def it_sets_all_options_to_the_provided_values():
                parameters = {
                    "format": True,
                    "prefix": "12345",
                }

                options = CpfGeneratorOptions(parameters)

                _assert_options_snapshots_match(options.all, parameters)

        def describe_when_called_with_a_cpf_generator_options_instance():
            def it_sets_a_new_instance_with_the_same_values():
                original_options = CpfGeneratorOptions(
                    {
                        "format": True,
                        "prefix": "12345",
                    }
                )

                options = CpfGeneratorOptions(original_options)

                assert options is not original_options
                _assert_options_snapshots_match(options.all, original_options.all)

        def describe_when_called_with_overrides_parameters():
            def it_uses_last_param_option_with_2_params():
                options = CpfGeneratorOptions(
                    {"prefix": "12345"},
                    {"prefix": "11222333"},
                )

                assert options.prefix == "11222333"

            def it_uses_last_param_option_with_5_params():
                options = CpfGeneratorOptions(
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
                options = CpfGeneratorOptions({"format": False})

                options.format = True

                assert options.format is True

            def it_sets_format_to_false():
                options = CpfGeneratorOptions({"format": True})

                options.format = False

                assert options.format is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CpfGeneratorOptions(
                    {"format": not CpfGeneratorOptions.DEFAULT_FORMAT}
                )

                options.format = None

                assert options.format == DEFAULT_PARAMETERS["format"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CpfGeneratorOptions({"format": False})

                options.format = {"not": "a boolean"}  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_truthy_string_value_to_true():
                options = CpfGeneratorOptions({"format": False})

                options.format = "not a boolean"  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_truthy_number_value_to_true():
                options = CpfGeneratorOptions({"format": False})

                options.format = 123  # type: ignore[assignment]

                assert options.format is True

            def it_coerces_empty_string_value_to_false():
                options = CpfGeneratorOptions({"format": False})

                options.format = ""  # type: ignore[assignment]

                assert options.format is False

            def it_coerces_zero_number_value_to_false():
                options = CpfGeneratorOptions({"format": False})

                options.format = 0  # type: ignore[assignment]

                assert options.format is False

    def describe_prefix_property():
        def describe_when_setting_to_a_valid_string_value():
            def it_sets_prefix_to_the_provided_value():
                options = CpfGeneratorOptions({"prefix": "12345"})

                options.prefix = "11222333"

                assert options.prefix == "11222333"

            def it_strips_non_numeric_characters_from_the_provided_value():
                options = CpfGeneratorOptions()

                options.prefix = "123.ABC.def"

                assert options.prefix == "123"

            def it_ignores_extra_characters_from_the_provided_value():
                options = CpfGeneratorOptions()

                options.prefix = "12345678910"

                assert options.prefix == "123456789"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CpfGeneratorOptions({"prefix": "12345"})

                options.prefix = None

                assert options.prefix == DEFAULT_PARAMETERS["prefix"]

        def describe_when_setting_to_a_non_string_value():
            def it_throws_cpf_generator_options_type_error_with_an_object():
                options = CpfGeneratorOptions()

                with _raises_message(
                    CpfGeneratorOptionsTypeError,
                    'CPF generator option "prefix" must be of type string. Got object.',
                ):
                    options.prefix = {"not": "a string"}  # type: ignore[assignment]

            def it_throws_cpf_generator_options_type_error_with_a_number():
                options = CpfGeneratorOptions()

                with _raises_message(
                    CpfGeneratorOptionsTypeError,
                    'CPF generator option "prefix" must be of type string. Got integer number.',
                ):
                    options.prefix = 123  # type: ignore[assignment]

            def it_throws_cpf_generator_options_type_error_with_a_boolean():
                options = CpfGeneratorOptions()

                with _raises_message(
                    CpfGeneratorOptionsTypeError,
                    'CPF generator option "prefix" must be of type string. Got boolean.',
                ):
                    options.prefix = True  # type: ignore[assignment]

        def describe_when_setting_to_an_invalid_string():
            def it_throws_cpf_generator_option_prefix_invalid_exception_with_base_id_all_zeros():
                options = CpfGeneratorOptions()

                with _raises_message(
                    CpfGeneratorOptionPrefixInvalidException,
                    'CPF generator option "prefix" with value "000000000" is invalid. Zeroed base ID is not eligible.',
                ):
                    options.prefix = "000000000"

            @pytest.mark.parametrize("prefix", REPEATED_DIGIT_PREFIXES)
            def it_throws_cpf_generator_option_prefix_invalid_exception_with_repeated_digits(
                prefix,
            ):
                options = CpfGeneratorOptions()

                with _raises_message(
                    CpfGeneratorOptionPrefixInvalidException,
                    f'CPF generator option "prefix" with value "{prefix}" is invalid. Repeated digits are not considered valid.',
                ):
                    options.prefix = prefix

    def describe_all_getter():
        def it_returns_all_properties():
            options = CpfGeneratorOptions()
            snapshot = options.all

            assert isinstance(snapshot["format"], bool)
            assert isinstance(snapshot["prefix"], str)
