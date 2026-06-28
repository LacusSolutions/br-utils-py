"""Behavioral spec for ``CnpjFormatterOptions``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-fmt/tests/cnpj-formatter-options.spec.ts``) and the PHP
reference suite
(``php/packages/cnpj-fmt/tests/specs/CnpjFormatterOptions.spec.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` nullish option values (JavaScript-only; Python uses ``None``).
"""

import re

import pytest
from cnpj_fmt import (
    CnpjFormatterOptions,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjFormatterOptionsTypeError,
)

DEFAULT_PARAMETERS = {
    "hidden": CnpjFormatterOptions.DEFAULT_HIDDEN,
    "hidden_key": CnpjFormatterOptions.DEFAULT_HIDDEN_KEY,
    "hidden_start": CnpjFormatterOptions.DEFAULT_HIDDEN_START,
    "hidden_end": CnpjFormatterOptions.DEFAULT_HIDDEN_END,
    "dot_key": CnpjFormatterOptions.DEFAULT_DOT_KEY,
    "slash_key": CnpjFormatterOptions.DEFAULT_SLASH_KEY,
    "dash_key": CnpjFormatterOptions.DEFAULT_DASH_KEY,
    "escape": CnpjFormatterOptions.DEFAULT_ESCAPE,
    "encode": CnpjFormatterOptions.DEFAULT_ENCODE,
    "on_fail": CnpjFormatterOptions.DEFAULT_ON_FAIL,
}


def _raises_message(exception_type, message: str):
    return pytest.raises(exception_type, match=re.escape(message))


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def describe_cnpj_formatter_options():
    def describe_constructor():
        def describe_when_called_with_no_parameters():
            def it_sets_all_options_to_default_values():
                options = CnpjFormatterOptions()

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters_with_null_values():
            def it_sets_all_options_to_default_values():
                options = CnpjFormatterOptions(
                    {
                        "hidden": None,
                        "hidden_key": None,
                        "hidden_start": None,
                        "hidden_end": None,
                        "dot_key": None,
                        "slash_key": None,
                        "dash_key": None,
                        "escape": None,
                        "encode": None,
                        "on_fail": None,
                    }
                )

                _assert_options_snapshots_match(options.all, DEFAULT_PARAMETERS)

        def describe_when_called_with_all_parameters():
            def it_sets_all_options_to_the_provided_values():
                def on_fail(value):
                    return f"ERROR: {value}"

                parameters = {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 1,
                    "hidden_end": 8,
                    "dot_key": "|",
                    "slash_key": "_",
                    "dash_key": "~",
                    "escape": True,
                    "encode": True,
                    "on_fail": on_fail,
                }

                options = CnpjFormatterOptions(parameters)

                _assert_options_snapshots_match(options.all, parameters)

        def describe_when_called_with_some_parameters():
            def it_sets_only_the_provided_non_nullish_values():
                parameters = {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": None,
                    "hidden_end": None,
                    "escape": True,
                    "encode": False,
                    "on_fail": None,
                }

                options = CnpjFormatterOptions(parameters)

                _assert_options_snapshots_match(
                    options.all,
                    {
                        **DEFAULT_PARAMETERS,
                        "hidden": True,
                        "hidden_key": "#",
                        "escape": True,
                        "encode": False,
                    },
                )

        def describe_when_called_with_a_cnpj_formatter_options_instance():
            def it_sets_a_new_instance_with_the_same_values():
                original_options = CnpjFormatterOptions(
                    {
                        "hidden": True,
                        "hidden_start": 1,
                        "hidden_end": 8,
                        "slash_key": "|",
                        "escape": True,
                        "on_fail": lambda value: f"ERROR: {value}",
                    }
                )

                options = CnpjFormatterOptions(original_options)

                assert options is not original_options
                _assert_options_snapshots_match(options.all, original_options.all)

        def describe_when_called_with_overrides_parameters():
            def it_uses_last_param_option_with_2_params():
                options = CnpjFormatterOptions({"hidden_key": "#"}, {"hidden_key": "X"})

                assert options.hidden_key == "X"

            def it_uses_last_param_option_with_1_mapping_and_1_instance():
                options = CnpjFormatterOptions(
                    {"hidden_key": "#"},
                    CnpjFormatterOptions({"hidden_key": "X"}),
                )

                assert options.hidden_key == "X"

            def it_uses_last_param_option_with_5_params():
                options = CnpjFormatterOptions(
                    {"hidden_key": "."},
                    {"hidden_key": "_"},
                    {"hidden_key": "#"},
                    {"hidden_key": "X"},
                    {"hidden_key": "@"},
                )

                assert options.hidden_key == "@"

    def describe_hidden_property():
        def describe_when_setting_to_a_boolean_value():
            def it_sets_hidden_to_true():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = True

                assert options.hidden is True

            def it_sets_hidden_to_false():
                options = CnpjFormatterOptions({"hidden": True})

                options.hidden = False

                assert options.hidden is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions(
                    {"hidden": not DEFAULT_PARAMETERS["hidden"]}
                )

                options.hidden = None

                assert options.hidden == DEFAULT_PARAMETERS["hidden"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = {"not": "a boolean"}

                assert options.hidden is True

            def it_coerces_truthy_string_value_to_true():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = "not a boolean"

                assert options.hidden is True

            def it_coerces_truthy_number_value_to_true():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = 123

                assert options.hidden is True

            def it_coerces_empty_string_value_to_false():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = ""

                assert options.hidden is False

            def it_coerces_zero_number_value_to_false():
                options = CnpjFormatterOptions({"hidden": False})

                options.hidden = 0

                assert options.hidden is False

    def describe_hidden_key_property():
        def describe_when_setting_to_a_string_value():
            def it_sets_hidden_key_to_the_provided_value():
                options = CnpjFormatterOptions({"hidden_key": "*"})

                options.hidden_key = "X"

                assert options.hidden_key == "X"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"hidden_key": "#"})

                options.hidden_key = None

                assert options.hidden_key == DEFAULT_PARAMETERS["hidden_key"]

        def describe_when_setting_to_a_non_string_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_key" must be of type string. Got dict.',
                ):
                    options.hidden_key = {"not": "a string"}

            def it_raises_cnpj_formatter_options_type_error_with_a_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_key" must be of type string. Got integer number.',
                ):
                    options.hidden_key = 123

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_key" must be of type string. Got boolean.',
                ):
                    options.hidden_key = True

        def describe_when_setting_to_a_string_containing_a_forbidden_key_character():
            @pytest.mark.parametrize(
                "forbidden_char",
                CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS,
            )
            def it_raises_cnpj_formatter_options_forbidden_key_character_exception(
                forbidden_char,
            ):
                options = CnpjFormatterOptions()
                quoted_chars = '", "'.join(
                    CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS
                )
                message = (
                    f'Value "{forbidden_char}" for CNPJ formatting option "hidden_key" '
                    f'contains disallowed characters ("{quoted_chars}").'
                )

                with pytest.raises(
                    CnpjFormatterOptionsForbiddenKeyCharacterException
                ) as exc_info:
                    options.hidden_key = forbidden_char

                assert str(exc_info.value) == message

    def describe_hidden_start_property():
        def describe_when_setting_to_a_number_value():
            def it_sets_hidden_start_to_the_provided_value():
                options = CnpjFormatterOptions({"hidden_start": 0})

                options.hidden_start = 1

                assert options.hidden_start == 1

        def describe_when_setting_to_an_invalid_number_value_range():
            def it_raises_hidden_range_invalid_exception_with_a_negative_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsHiddenRangeInvalidException,
                    'CNPJ formatting option "hidden_start" must be an integer between 0 and 13. Got -1.',
                ):
                    options.hidden_start = -1

            def it_raises_hidden_range_invalid_exception_with_a_number_greater_than_13():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsHiddenRangeInvalidException,
                    'CNPJ formatting option "hidden_start" must be an integer between 0 and 13. Got 14.',
                ):
                    options.hidden_start = 14

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"hidden_start": 0})

                options.hidden_start = None

                assert options.hidden_start == DEFAULT_PARAMETERS["hidden_start"]

        def describe_when_setting_to_a_non_integer_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_start" must be of type integer. Got dict.',
                ):
                    options.hidden_start = {"not": "a number"}

            def it_raises_cnpj_formatter_options_type_error_with_a_string():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_start" must be of type integer. Got string.',
                ):
                    options.hidden_start = "not a number"

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_start" must be of type integer. Got boolean.',
                ):
                    options.hidden_start = True

            def it_raises_cnpj_formatter_options_type_error_with_a_float_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_start" must be of type integer. Got float number.',
                ):
                    options.hidden_start = 1.5

    def describe_hidden_end_property():
        def describe_when_setting_to_a_number_value():
            def it_sets_hidden_end_to_the_provided_value():
                options = CnpjFormatterOptions({"hidden_end": 13})

                options.hidden_end = 12

                assert options.hidden_end == 12

        def describe_when_setting_to_an_invalid_number_value_range():
            def it_raises_hidden_range_invalid_exception_with_a_negative_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsHiddenRangeInvalidException,
                    'CNPJ formatting option "hidden_end" must be an integer between 0 and 13. Got -1.',
                ):
                    options.hidden_end = -1

            def it_raises_hidden_range_invalid_exception_with_a_number_greater_than_13():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsHiddenRangeInvalidException,
                    'CNPJ formatting option "hidden_end" must be an integer between 0 and 13. Got 14.',
                ):
                    options.hidden_end = 14

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"hidden_end": 0})

                options.hidden_end = None

                assert options.hidden_end == DEFAULT_PARAMETERS["hidden_end"]

        def describe_when_setting_to_a_non_integer_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_end" must be of type integer. Got dict.',
                ):
                    options.hidden_end = {"not": "a number"}

            def it_raises_cnpj_formatter_options_type_error_with_a_string():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_end" must be of type integer. Got string.',
                ):
                    options.hidden_end = "not a number"

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_end" must be of type integer. Got boolean.',
                ):
                    options.hidden_end = True

            def it_raises_cnpj_formatter_options_type_error_with_a_float_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "hidden_end" must be of type integer. Got float number.',
                ):
                    options.hidden_end = 1.5

    def describe_dot_key_property():
        def describe_when_setting_to_a_string_value():
            def it_sets_dot_key_to_the_provided_value():
                options = CnpjFormatterOptions({"dot_key": "."})

                options.dot_key = "_"

                assert options.dot_key == "_"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"dot_key": "_"})

                options.dot_key = None

                assert options.dot_key == DEFAULT_PARAMETERS["dot_key"]

        def describe_when_setting_to_a_non_string_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dot_key" must be of type string. Got dict.',
                ):
                    options.dot_key = {"not": "a string"}

            def it_raises_cnpj_formatter_options_type_error_with_a_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dot_key" must be of type string. Got integer number.',
                ):
                    options.dot_key = 123

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dot_key" must be of type string. Got boolean.',
                ):
                    options.dot_key = True

        def describe_when_setting_to_a_string_containing_a_forbidden_key_character():
            @pytest.mark.parametrize(
                "forbidden_char",
                CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS,
            )
            def it_raises_cnpj_formatter_options_forbidden_key_character_exception(
                forbidden_char,
            ):
                options = CnpjFormatterOptions()
                quoted_chars = '", "'.join(
                    CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS
                )
                message = (
                    f'Value "{forbidden_char}" for CNPJ formatting option "dot_key" '
                    f'contains disallowed characters ("{quoted_chars}").'
                )

                with pytest.raises(
                    CnpjFormatterOptionsForbiddenKeyCharacterException
                ) as exc_info:
                    options.dot_key = forbidden_char

                assert str(exc_info.value) == message

    def describe_slash_key_property():
        def describe_when_setting_to_a_string_value():
            def it_sets_slash_key_to_the_provided_value():
                options = CnpjFormatterOptions({"slash_key": "."})

                options.slash_key = "_"

                assert options.slash_key == "_"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"slash_key": "_"})

                options.slash_key = None

                assert options.slash_key == DEFAULT_PARAMETERS["slash_key"]

        def describe_when_setting_to_a_non_string_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "slash_key" must be of type string. Got dict.',
                ):
                    options.slash_key = {"not": "a string"}

            def it_raises_cnpj_formatter_options_type_error_with_a_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "slash_key" must be of type string. Got integer number.',
                ):
                    options.slash_key = 123

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "slash_key" must be of type string. Got boolean.',
                ):
                    options.slash_key = True

        def describe_when_setting_to_a_string_containing_a_forbidden_key_character():
            @pytest.mark.parametrize(
                "forbidden_char",
                CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS,
            )
            def it_raises_cnpj_formatter_options_forbidden_key_character_exception(
                forbidden_char,
            ):
                options = CnpjFormatterOptions()
                quoted_chars = '", "'.join(
                    CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS
                )
                message = (
                    f'Value "{forbidden_char}" for CNPJ formatting option "slash_key" '
                    f'contains disallowed characters ("{quoted_chars}").'
                )

                with pytest.raises(
                    CnpjFormatterOptionsForbiddenKeyCharacterException
                ) as exc_info:
                    options.slash_key = forbidden_char

                assert str(exc_info.value) == message

    def describe_dash_key_property():
        def describe_when_setting_to_a_string_value():
            def it_sets_dash_key_to_the_provided_value():
                options = CnpjFormatterOptions({"dash_key": "."})

                options.dash_key = "_"

                assert options.dash_key == "_"

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions({"dash_key": "_"})

                options.dash_key = None

                assert options.dash_key == DEFAULT_PARAMETERS["dash_key"]

        def describe_when_setting_to_a_non_string_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dash_key" must be of type string. Got dict.',
                ):
                    options.dash_key = {"not": "a string"}

            def it_raises_cnpj_formatter_options_type_error_with_a_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dash_key" must be of type string. Got integer number.',
                ):
                    options.dash_key = 123

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "dash_key" must be of type string. Got boolean.',
                ):
                    options.dash_key = True

        def describe_when_setting_to_a_string_containing_a_forbidden_key_character():
            @pytest.mark.parametrize(
                "forbidden_char",
                CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS,
            )
            def it_raises_cnpj_formatter_options_forbidden_key_character_exception(
                forbidden_char,
            ):
                options = CnpjFormatterOptions()
                quoted_chars = '", "'.join(
                    CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS
                )
                message = (
                    f'Value "{forbidden_char}" for CNPJ formatting option "dash_key" '
                    f'contains disallowed characters ("{quoted_chars}").'
                )

                with pytest.raises(
                    CnpjFormatterOptionsForbiddenKeyCharacterException
                ) as exc_info:
                    options.dash_key = forbidden_char

                assert str(exc_info.value) == message

    def describe_escape_property():
        def describe_when_setting_to_a_boolean_value():
            def it_sets_escape_to_true():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = True

                assert options.escape is True

            def it_sets_escape_to_false():
                options = CnpjFormatterOptions({"escape": True})

                options.escape = False

                assert options.escape is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions(
                    {"escape": not DEFAULT_PARAMETERS["escape"]}
                )

                options.escape = None

                assert options.escape == DEFAULT_PARAMETERS["escape"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = {"not": "a boolean"}

                assert options.escape is True

            def it_coerces_truthy_string_value_to_true():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = "not a boolean"

                assert options.escape is True

            def it_coerces_truthy_number_value_to_true():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = 123

                assert options.escape is True

            def it_coerces_empty_string_value_to_false():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = ""

                assert options.escape is False

            def it_coerces_zero_number_value_to_false():
                options = CnpjFormatterOptions({"escape": False})

                options.escape = 0

                assert options.escape is False

    def describe_encode_property():
        def describe_when_setting_to_a_boolean_value():
            def it_sets_encode_to_true():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = True

                assert options.encode is True

            def it_sets_encode_to_false():
                options = CnpjFormatterOptions({"encode": True})

                options.encode = False

                assert options.encode is False

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_value_for_none():
                options = CnpjFormatterOptions(
                    {"encode": not DEFAULT_PARAMETERS["encode"]}
                )

                options.encode = None

                assert options.encode == DEFAULT_PARAMETERS["encode"]

        def describe_when_setting_to_a_non_boolean_value():
            def it_coerces_object_value_to_true():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = {"not": "a boolean"}

                assert options.encode is True

            def it_coerces_truthy_string_value_to_true():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = "not a boolean"

                assert options.encode is True

            def it_coerces_truthy_number_value_to_true():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = 123

                assert options.encode is True

            def it_coerces_empty_string_value_to_false():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = ""

                assert options.encode is False

            def it_coerces_zero_number_value_to_false():
                options = CnpjFormatterOptions({"encode": False})

                options.encode = 0

                assert options.encode is False

    def describe_on_fail_property():
        def describe_when_using_the_default_callback_value():
            def it_returns_empty_string():
                result = CnpjFormatterOptions.DEFAULT_ON_FAIL("some value")

                assert result == ""

        def describe_when_setting_to_a_callable_value():
            def it_sets_on_fail_to_the_provided_callback():
                def callback(value):
                    return f"ERROR: {value}"

                options = CnpjFormatterOptions()

                options.on_fail = callback

                assert options.on_fail is callback

        def describe_when_setting_to_a_nullish_value():
            def it_sets_default_callback_for_none():
                def callback(value):
                    return f"ERROR: {value}"

                options = CnpjFormatterOptions({"on_fail": callback})

                options.on_fail = None

                assert options.on_fail is DEFAULT_PARAMETERS["on_fail"]
                assert options.on_fail.__name__ == "DEFAULT_ON_FAIL"

        def describe_when_setting_to_a_non_callable_value():
            def it_raises_cnpj_formatter_options_type_error_with_an_object():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "on_fail" must be of type function. Got dict.',
                ):
                    options.on_fail = {"not": "a function"}

            def it_raises_cnpj_formatter_options_type_error_with_a_string():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "on_fail" must be of type function. Got string.',
                ):
                    options.on_fail = "not a function"

            def it_raises_cnpj_formatter_options_type_error_with_a_number():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "on_fail" must be of type function. Got integer number.',
                ):
                    options.on_fail = 123

            def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                options = CnpjFormatterOptions()

                with _raises_message(
                    CnpjFormatterOptionsTypeError,
                    'CNPJ formatting option "on_fail" must be of type function. Got boolean.',
                ):
                    options.on_fail = True

    def describe_all_getter():
        def it_returns_all_properties_with_expected_types():
            all_options = CnpjFormatterOptions().all

            assert isinstance(all_options["hidden"], bool)
            assert isinstance(all_options["hidden_key"], str)
            assert isinstance(all_options["hidden_start"], int)
            assert isinstance(all_options["hidden_end"], int)
            assert isinstance(all_options["dot_key"], str)
            assert isinstance(all_options["slash_key"], str)
            assert isinstance(all_options["dash_key"], str)
            assert isinstance(all_options["escape"], bool)
            assert isinstance(all_options["encode"], bool)
            assert callable(all_options["on_fail"])

    def describe_set_hidden_range_method():
        def describe_when_called_with_valid_values():
            def it_sets_hidden_start_and_hidden_end_to_the_provided_values():
                options = CnpjFormatterOptions()

                options.set_hidden_range(0, 10)

                assert options.hidden_start == 0
                assert options.hidden_end == 10

            def describe_and_hidden_start_is_equal_to_hidden_end():
                def it_sets_hidden_start_and_hidden_end_with_0_accordingly():
                    options = CnpjFormatterOptions()

                    options.set_hidden_range(0, 0)

                    assert options.hidden_start == 0
                    assert options.hidden_end == 0

                def it_sets_hidden_start_and_hidden_end_with_13_accordingly():
                    options = CnpjFormatterOptions()

                    options.set_hidden_range(13, 13)

                    assert options.hidden_start == 13
                    assert options.hidden_end == 13

            def describe_and_hidden_start_is_greater_than_hidden_end():
                def it_automatically_swaps_start_and_end_values():
                    options = CnpjFormatterOptions()

                    options.set_hidden_range(8, 2)

                    assert options.hidden_start == 2
                    assert options.hidden_end == 8

        def describe_when_called_with_nullish_values():
            def it_sets_default_values_for_none_in_both_fields():
                options = CnpjFormatterOptions()

                options.set_hidden_range(None, None)

                assert options.hidden_start == DEFAULT_PARAMETERS["hidden_start"]
                assert options.hidden_end == DEFAULT_PARAMETERS["hidden_end"]

            def describe_when_setting_hidden_start_to_a_nullish_value():
                def it_sets_default_value_for_none():
                    options = CnpjFormatterOptions({"hidden_start": 0})

                    options.set_hidden_range(None, 13)

                    assert options.hidden_start == DEFAULT_PARAMETERS["hidden_start"]
                    assert options.hidden_end == 13

            def describe_when_setting_hidden_end_to_a_nullish_value():
                def it_sets_default_value_for_none():
                    options = CnpjFormatterOptions({"hidden_end": 13})

                    options.set_hidden_range(0, None)

                    assert options.hidden_start == 0
                    assert options.hidden_end == DEFAULT_PARAMETERS["hidden_end"]

        def describe_when_called_with_invalid_values():
            def describe_when_setting_hidden_start_to_an_invalid_number_value_range():
                def it_raises_hidden_range_invalid_exception_with_a_negative_number():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsHiddenRangeInvalidException,
                        'CNPJ formatting option "hidden_start" must be an integer between 0 and 13. Got -1.',
                    ):
                        options.set_hidden_range(-1, 13)

                def it_raises_hidden_range_invalid_exception_with_a_number_greater_than_13():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsHiddenRangeInvalidException,
                        'CNPJ formatting option "hidden_start" must be an integer between 0 and 13. Got 14.',
                    ):
                        options.set_hidden_range(14, 13)

            def describe_when_setting_hidden_end_to_an_invalid_number_value_range():
                def it_raises_hidden_range_invalid_exception_with_a_negative_number():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsHiddenRangeInvalidException,
                        'CNPJ formatting option "hidden_end" must be an integer between 0 and 13. Got -1.',
                    ):
                        options.set_hidden_range(0, -1)

                def it_raises_hidden_range_invalid_exception_with_a_number_greater_than_13():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsHiddenRangeInvalidException,
                        'CNPJ formatting option "hidden_end" must be an integer between 0 and 13. Got 14.',
                    ):
                        options.set_hidden_range(0, 14)

            def describe_when_setting_hidden_start_to_a_non_integer_value():
                def it_raises_cnpj_formatter_options_type_error_with_an_object():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_start" must be of type integer. Got dict.',
                    ):
                        options.set_hidden_range({"not": "a number"}, 13)

                def it_raises_cnpj_formatter_options_type_error_with_a_string():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_start" must be of type integer. Got string.',
                    ):
                        options.set_hidden_range("not a number", 13)

                def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_start" must be of type integer. Got boolean.',
                    ):
                        options.set_hidden_range(True, 13)

                def it_raises_cnpj_formatter_options_type_error_with_a_float_number():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_start" must be of type integer. Got float number.',
                    ):
                        options.set_hidden_range(1.5, 13)

            def describe_when_setting_hidden_end_to_a_non_integer_value():
                def it_raises_cnpj_formatter_options_type_error_with_an_object():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_end" must be of type integer. Got dict.',
                    ):
                        options.set_hidden_range(0, {"not": "a number"})

                def it_raises_cnpj_formatter_options_type_error_with_a_string():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_end" must be of type integer. Got string.',
                    ):
                        options.set_hidden_range(0, "not a number")

                def it_raises_cnpj_formatter_options_type_error_with_a_boolean():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_end" must be of type integer. Got boolean.',
                    ):
                        options.set_hidden_range(0, True)

                def it_raises_cnpj_formatter_options_type_error_with_a_float_number():
                    options = CnpjFormatterOptions()

                    with _raises_message(
                        CnpjFormatterOptionsTypeError,
                        'CNPJ formatting option "hidden_end" must be of type integer. Got float number.',
                    ):
                        options.set_hidden_range(0, 1.5)
