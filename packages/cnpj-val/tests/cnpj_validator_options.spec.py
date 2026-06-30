"""Behavioral spec for ``CnpjValidatorOptions``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-val/tests/cnpj-validator-options.spec.ts``) and the PHP
reference suite
(``php/packages/cnpj-val/tests/specs/CnpjValidatorOptions.spec.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` nullish option values (JavaScript-only; Python uses ``None``).
- PHP ``CnpjValidationType`` enum assignment (PHP-only representation; Python
  uses ``"alphanumeric"`` / ``"numeric"`` string literals).
- PHP ``overrides`` array entries that flip ``case_sensitive`` (same merge
  semantics as the JS ``type`` override chain; covered via JS cases).
"""

import re

import pytest
from cnpj_val import (
    CnpjValidatorOptions,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
)

DEFAULT_PARAMETERS = {
    "case_sensitive": CnpjValidatorOptions.DEFAULT_CASE_SENSITIVE,
    "type": CnpjValidatorOptions.DEFAULT_TYPE,
}


def _raises_message(exception_type, message: str):
    return pytest.raises(exception_type, match=re.escape(message))


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def describe_cnpj_validator_options():
    def describe_constructor():
        def describe_when_called_with_no_parameters():
            def it_sets_all_options_to_default_values():
                options = CnpjValidatorOptions()

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters_with_null_values():
            def it_sets_all_options_to_default_values():
                options = CnpjValidatorOptions(
                    {
                        "case_sensitive": None,
                        "type": None,
                    }
                )

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters():
            def it_sets_all_options_to_the_provided_values():
                parameters = {
                    "case_sensitive": True,
                    "type": "numeric",
                }

                options = CnpjValidatorOptions(parameters)

                _assert_options_snapshots_match(options.all, parameters)

        def describe_when_called_with_some_parameters():
            def it_sets_only_the_provided_non_nullish_values():
                options = CnpjValidatorOptions({"type": "numeric"})

                _assert_options_snapshots_match(
                    options.all,
                    {
                        **DEFAULT_PARAMETERS,
                        "type": "numeric",
                    },
                )

        def describe_when_called_with_a_cnpj_validator_options_instance():
            def it_sets_a_new_instance_with_the_same_values():
                original_options = CnpjValidatorOptions(
                    {
                        "case_sensitive": True,
                        "type": "numeric",
                    }
                )

                options = CnpjValidatorOptions(original_options)

                assert options is not original_options
                _assert_options_snapshots_match(options.all, original_options.all)

        def describe_when_called_with_overrides_parameters():
            def it_uses_last_param_option_with_2_params():
                options = CnpjValidatorOptions(
                    {"type": "numeric"},
                    {"type": "alphanumeric"},
                )

                assert options.type == "alphanumeric"

            def it_uses_last_param_option_with_5_params():
                options = CnpjValidatorOptions(
                    {"type": "numeric"},
                    {"type": "alphanumeric"},
                    {"type": "numeric"},
                    {"type": "alphanumeric"},
                    {"type": "numeric"},
                )

                assert options.type == "numeric"

    def describe_case_sensitive_property():
        def describe_when_setting_to_a_boolean_value():
            def it_sets_case_sensitive_to_true():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = True

                assert options.case_sensitive is True

            def it_sets_case_sensitive_to_false():
                options = CnpjValidatorOptions({"case_sensitive": True})

                options.case_sensitive = False

                assert options.case_sensitive is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjValidatorOptions(
                    {
                        "case_sensitive": not DEFAULT_PARAMETERS["case_sensitive"],
                    }
                )

                options.case_sensitive = None

                assert options.case_sensitive == DEFAULT_PARAMETERS["case_sensitive"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = {"not": "a boolean"}  # type: ignore[assignment]

                assert options.case_sensitive is True

            def it_coerces_truthy_string_value_to_true():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = "not a boolean"  # type: ignore[assignment]

                assert options.case_sensitive is True

            def it_coerces_truthy_number_value_to_true():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = 123  # type: ignore[assignment]

                assert options.case_sensitive is True

            def it_coerces_empty_string_value_to_false():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = ""  # type: ignore[assignment]

                assert options.case_sensitive is False

            def it_coerces_zero_number_value_to_false():
                options = CnpjValidatorOptions({"case_sensitive": False})

                options.case_sensitive = 0  # type: ignore[assignment]

                assert options.case_sensitive is False

    def describe_type_property():
        def describe_when_setting_to_a_valid_option_value():
            @pytest.mark.parametrize("type_value", ["alphanumeric", "numeric"])
            def it_sets_type_to_the_value(type_value):
                options = CnpjValidatorOptions({"type": type_value})

                options.type = type_value

                assert options.type == type_value

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjValidatorOptions({"type": "numeric"})

                options.type = None

                assert options.type == DEFAULT_PARAMETERS["type"]

        def describe_when_setting_to_a_non_string_value():
            def it_throws_cnpj_validator_options_type_error_with_an_object():
                options = CnpjValidatorOptions()

                with _raises_message(
                    CnpjValidatorOptionsTypeError,
                    'CNPJ validator option "type" must be of type string. Got object.',
                ):
                    options.type = {"not": "a string"}  # type: ignore[assignment]

            def it_throws_cnpj_validator_options_type_error_with_a_number():
                options = CnpjValidatorOptions()

                with _raises_message(
                    CnpjValidatorOptionsTypeError,
                    'CNPJ validator option "type" must be of type string. Got integer number.',
                ):
                    options.type = 123  # type: ignore[assignment]

            def it_throws_cnpj_validator_options_type_error_with_a_boolean():
                options = CnpjValidatorOptions()

                with _raises_message(
                    CnpjValidatorOptionsTypeError,
                    'CNPJ validator option "type" must be of type string. Got boolean.',
                ):
                    options.type = True  # type: ignore[assignment]

        def describe_when_setting_to_an_invalid_option():
            def it_throws_cnpj_validator_option_type_invalid_exception_with_unexpected_value():
                options = CnpjValidatorOptions()

                with _raises_message(
                    CnpjValidatorOptionTypeInvalidException,
                    'CNPJ validator option "type" accepts only the following values: '
                    '"alphanumeric", "numeric". Got "something".',
                ):
                    options.type = "something"  # type: ignore[assignment]

    def describe_all_getter():
        def it_returns_all_properties():
            options = CnpjValidatorOptions()

            assert isinstance(options.all["case_sensitive"], bool)
            assert isinstance(options.all["type"], str)
