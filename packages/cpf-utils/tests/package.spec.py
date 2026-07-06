"""Spec for the public API surface of the ``cpf_utils`` package.

Mirrors the API-surface and behavioral smoke tests of the JavaScript
``output.spec.ts`` suite following ``AGENTS.md`` §2 and §9.

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable wiring,
and export string parsing). Those concern JS packaging only.

Dropped CNPJ-only exports: ``CpfValidatorOptions``, ``CpfValidatorOptionsTypeError``,
``CpfValidatorOptionTypeInvalidException``, ``CpfGeneratorOptionTypeInvalidException``,
and formatter ``slash_key`` scenarios.
"""

import re

import cpf_utils as cpf_utils_module
from cpf_fmt import (
    CpfFormatter,
    CpfFormatterException,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
    CpfFormatterOptions,
    CpfFormatterOptionsForbiddenKeyCharacterException,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfFormatterOptionsTypeError,
    CpfFormatterTypeError,
    cpf_fmt,
)
from cpf_gen import (
    CpfGenerator,
    CpfGeneratorException,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
    CpfGeneratorOptionsTypeError,
    CpfGeneratorTypeError,
    cpf_gen,
)
from cpf_utils import CpfUtils, cpf_utils
from cpf_val import (
    CpfValidator,
    CpfValidatorException,
    CpfValidatorInputTypeError,
    CpfValidatorTypeError,
    cpf_val,
)


def describe_the_cpf_utils_package_api():
    def describe_default_instance():
        def it_exports_an_instance_of_cpf_utils_class():
            assert isinstance(cpf_utils, CpfUtils)

        def it_exposes_format_generate_and_is_valid_methods():
            assert callable(cpf_utils.format)
            assert callable(cpf_utils.generate)
            assert callable(cpf_utils.is_valid)

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "cpf_utils",
                "CpfUtils",
                "cpf_fmt",
                "CpfFormatter",
                "CpfFormatterOptions",
                "CpfFormatterTypeError",
                "CpfFormatterInputTypeError",
                "CpfFormatterOptionsTypeError",
                "CpfFormatterException",
                "CpfFormatterInputLengthException",
                "CpfFormatterOptionsHiddenRangeInvalidException",
                "CpfFormatterOptionsForbiddenKeyCharacterException",
                "cpf_gen",
                "CpfGenerator",
                "CpfGeneratorOptions",
                "CpfGeneratorTypeError",
                "CpfGeneratorOptionsTypeError",
                "CpfGeneratorException",
                "CpfGeneratorOptionPrefixInvalidException",
                "cpf_val",
                "CpfValidator",
                "CpfValidatorTypeError",
                "CpfValidatorInputTypeError",
                "CpfValidatorException",
            }

            assert expected_names.issubset(set(dir(cpf_utils_module)))

    def describe_on_formatting_module():
        def it_exposes_a_format_method():
            result = cpf_utils.format("12345678909", dot_key="_", dash_key=" dv ")

            assert result == "123_456_789 dv 09"

        def it_exposes_cpf_fmt_function():
            result = cpf_fmt("12345678909", {"dot_key": "_", "dash_key": " dv "})

            assert result == "123_456_789 dv 09"

        def it_exposes_an_instantiable_cpf_formatter_class():
            formatter = CpfFormatter({"hidden": True})
            result = formatter.format("12345678909")

            assert isinstance(formatter, CpfFormatter)
            assert result == "123.***.***-**"

        def it_exposes_an_instantiable_cpf_formatter_options_class():
            options = CpfFormatterOptions(
                {
                    "hidden": True,
                    "hidden_key": "X",
                    "dot_key": " ",
                    "dash_key": "_",
                },
            )

            assert options.hidden is True
            assert options.hidden_key == "X"
            assert options.dot_key == " "
            assert options.dash_key == "_"

        def it_exposes_cpf_formatter_input_type_error_as_instantiable():
            error = CpfFormatterInputTypeError(123, "string")

            assert error.actual_input == 123
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert str(error) == "CPF input must be of type string. Got integer number."

        def it_exposes_cpf_formatter_options_type_error_as_instantiable():
            error = CpfFormatterOptionsTypeError("hidden", 123, "boolean")

            assert error.actual_input == 123
            assert error.option_name == "hidden"
            assert error.actual_type == "integer number"
            assert error.expected_type == "boolean"
            assert (
                str(error)
                == 'CPF formatting option "hidden" must be of type boolean. Got integer number.'
            )

        def it_exposes_cpf_formatter_options_hidden_range_invalid_exception_as_instantiable():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start",
                123,
                0,
                10,
            )

            assert exception.actual_input == 123
            assert exception.option_name == "hidden_start"
            assert exception.min_expected_value == 0
            assert exception.max_expected_value == 10
            assert (
                str(exception)
                == 'CPF formatting option "hidden_start" must be an integer between 0 and 10. Got 123.'
            )

        def it_exposes_cpf_formatter_options_forbidden_key_character_exception_as_instantiable():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key",
                "x",
                ["x"],
            )

            assert exception.actual_input == "x"
            assert exception.option_name == "dot_key"
            assert exception.forbidden_characters == ["x"]
            assert (
                str(exception)
                == 'Value "x" for CPF formatting option "dot_key" contains disallowed characters ("x").'
            )

        def it_exposes_cpf_formatter_input_length_exception_as_instantiable():
            exception = CpfFormatterInputLengthException("ABC.123", "ABC123", 11)

            assert exception.actual_input == "ABC.123"
            assert exception.evaluated_input == "ABC123"
            assert exception.expected_length == 11
            assert (
                str(exception)
                == 'CPF input "ABC.123" does not contain 11 digits. Got 6 in "ABC123".'
            )

        def it_exposes_cpf_formatter_type_error_as_a_base_type():
            assert issubclass(CpfFormatterTypeError, TypeError)

        def it_exposes_cpf_formatter_exception_as_a_base_type():
            assert issubclass(CpfFormatterException, Exception)

    def describe_on_generating_module():
        def it_exposes_a_generate_method():
            result = cpf_utils.generate()

            assert len(result) == 11
            assert result.isdigit()

        def it_exposes_cpf_gen_function():
            result = cpf_gen()

            assert len(result) == 11
            assert result.isdigit()

        def it_exposes_an_instantiable_cpf_generator_class():
            generator = CpfGenerator()
            result = generator.generate({"prefix": "12345"})

            assert isinstance(generator, CpfGenerator)
            assert re.fullmatch(r"^12345\d{6}$", result)

        def it_exposes_an_instantiable_cpf_generator_options_class():
            options = CpfGeneratorOptions(
                {
                    "prefix": "12345678",
                    "format": True,
                },
            )

            assert options.prefix == "12345678"
            assert options.format is True

        def it_exposes_cpf_generator_options_type_error_as_instantiable():
            error = CpfGeneratorOptionsTypeError("prefix", 123, "string")

            assert error.actual_input == 123
            assert error.option_name == "prefix"
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert (
                str(error)
                == 'CPF generator option "prefix" must be of type string. Got integer number.'
            )

        def it_exposes_cpf_generator_option_prefix_invalid_exception_as_instantiable():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "AB123XYZ", "some reason"
            )

            assert exception.actual_input == "AB123XYZ"
            assert exception.reason == "some reason"
            assert (
                str(exception)
                == 'CPF generator option "prefix" with value "AB123XYZ" is invalid. some reason'
            )

        def it_exposes_cpf_generator_type_error_as_a_base_type():
            assert issubclass(CpfGeneratorTypeError, TypeError)

        def it_exposes_cpf_generator_exception_as_a_base_type():
            assert issubclass(CpfGeneratorException, Exception)

    def describe_on_validating_module():
        def it_exposes_an_is_valid_method():
            assert cpf_utils.is_valid("12345678909") is True
            assert cpf_utils.is_valid("12345678900") is False

        def it_exposes_cpf_val_function():
            assert cpf_val("12345678909") is True
            assert cpf_val("12345678900") is False

        def it_exposes_an_instantiable_cpf_validator_class():
            validator = CpfValidator()
            result = validator.is_valid("12345678909")

            assert isinstance(validator, CpfValidator)
            assert result is True

        def it_exposes_cpf_validator_input_type_error_as_instantiable():
            error = CpfValidatorInputTypeError(123, "string")

            assert error.actual_input == 123
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert str(error) == "CPF input must be of type string. Got integer number."

        def it_exposes_cpf_validator_type_error_as_a_base_type():
            assert issubclass(CpfValidatorTypeError, TypeError)

        def it_exposes_cpf_validator_exception_as_a_base_type():
            assert issubclass(CpfValidatorException, Exception)
