"""Spec for the public API surface of the ``cnpj_utils`` package.

Mirrors the API-surface and behavioral smoke tests of the JavaScript
``output.spec.ts`` suite following ``AGENTS.md`` §2 and §9.

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable wiring,
and export string parsing). Those concern JS packaging only and have no Python
equivalent.
"""

import cnpj_utils as cnpj_utils_module
from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterException,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
    CnpjFormatterOptions,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjFormatterOptionsTypeError,
    CnpjFormatterTypeError,
    cnpj_fmt,
)
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorException,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjGeneratorTypeError,
    cnpj_gen,
)
from cnpj_utils import CnpjUtils, cnpj_utils
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptions,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    CnpjValidatorTypeError,
    cnpj_val,
)


def describe_the_cnpj_utils_package_api():
    def describe_default_instance():
        def it_exports_an_instance_of_cnpj_utils_class():
            assert isinstance(cnpj_utils, CnpjUtils)

        def it_exposes_format_generate_and_is_valid_methods():
            assert callable(cnpj_utils.format)
            assert callable(cnpj_utils.generate)
            assert callable(cnpj_utils.is_valid)

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "cnpj_utils",
                "CnpjUtils",
                "cnpj_fmt",
                "CnpjFormatter",
                "CnpjFormatterOptions",
                "CnpjFormatterTypeError",
                "CnpjFormatterInputTypeError",
                "CnpjFormatterOptionsTypeError",
                "CnpjFormatterException",
                "CnpjFormatterInputLengthException",
                "CnpjFormatterOptionsHiddenRangeInvalidException",
                "CnpjFormatterOptionsForbiddenKeyCharacterException",
                "cnpj_gen",
                "CnpjGenerator",
                "CnpjGeneratorOptions",
                "CnpjGeneratorTypeError",
                "CnpjGeneratorOptionsTypeError",
                "CnpjGeneratorException",
                "CnpjGeneratorOptionPrefixInvalidException",
                "CnpjGeneratorOptionTypeInvalidException",
                "cnpj_val",
                "CnpjValidator",
                "CnpjValidatorOptions",
                "CnpjValidatorTypeError",
                "CnpjValidatorInputTypeError",
                "CnpjValidatorOptionsTypeError",
                "CnpjValidatorException",
                "CnpjValidatorOptionTypeInvalidException",
            }

            assert expected_names.issubset(set(dir(cnpj_utils_module)))

    def describe_on_formatting_module():
        def it_exposes_a_format_method():
            result = cnpj_utils.format("01ABC234000X56", slash_key="|")

            assert result == "01.ABC.234|000X-56"

        def it_exposes_cnpj_fmt_function():
            result = cnpj_fmt("01ABC234000X56", {"slash_key": "|"})

            assert result == "01.ABC.234|000X-56"

        def it_exposes_an_instantiable_cnpj_formatter_class():
            formatter = CnpjFormatter({"hidden": True})
            result = formatter.format("AB123XYZ000123")

            assert isinstance(formatter, CnpjFormatter)
            assert result == "AB.123.***/****-**"

        def it_exposes_an_instantiable_cnpj_formatter_options_class():
            options = CnpjFormatterOptions(
                {
                    "hidden": True,
                    "hidden_key": "X",
                    "dot_key": " ",
                    "slash_key": "|",
                    "dash_key": "_",
                },
            )

            assert options.hidden is True
            assert options.hidden_key == "X"
            assert options.dot_key == " "
            assert options.slash_key == "|"
            assert options.dash_key == "_"

        def it_exposes_cnpj_formatter_input_type_error_as_instantiable():
            error = CnpjFormatterInputTypeError(123, "string")

            assert error.actual_input == 123
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert (
                str(error) == "CNPJ input must be of type string. Got integer number."
            )

        def it_exposes_cnpj_formatter_options_type_error_as_instantiable():
            error = CnpjFormatterOptionsTypeError("hidden", 123, "boolean")

            assert error.actual_input == 123
            assert error.option_name == "hidden"
            assert error.actual_type == "integer number"
            assert error.expected_type == "boolean"
            assert (
                str(error)
                == 'CNPJ formatting option "hidden" must be of type boolean. Got integer number.'
            )

        def it_exposes_cnpj_formatter_options_hidden_range_invalid_exception_as_instantiable():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start",
                123,
                0,
                13,
            )

            assert exception.actual_input == 123
            assert exception.option_name == "hidden_start"
            assert exception.min_expected_value == 0
            assert exception.max_expected_value == 13
            assert (
                str(exception)
                == 'CNPJ formatting option "hidden_start" must be an integer between 0 and 13. Got 123.'
            )

        def it_exposes_cnpj_formatter_options_forbidden_key_character_exception_as_instantiable():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dot_key",
                "x",
                ["x"],
            )

            assert exception.actual_input == "x"
            assert exception.option_name == "dot_key"
            assert exception.forbidden_characters == ["x"]
            assert (
                str(exception)
                == 'Value "x" for CNPJ formatting option "dot_key" contains disallowed characters ("x").'
            )

        def it_exposes_cnpj_formatter_input_length_exception_as_instantiable():
            exception = CnpjFormatterInputLengthException("ABC.123", "ABC123", 14)

            assert exception.actual_input == "ABC.123"
            assert exception.evaluated_input == "ABC123"
            assert exception.expected_length == 14
            assert (
                str(exception)
                == 'CNPJ input "ABC.123" does not contain 14 characters. Got 6 in "ABC123".'
            )

        def it_exposes_cnpj_formatter_type_error_as_a_base_type():
            assert issubclass(CnpjFormatterTypeError, TypeError)

        def it_exposes_cnpj_formatter_exception_as_a_base_type():
            assert issubclass(CnpjFormatterException, Exception)

    def describe_on_generating_module():
        def it_exposes_a_generate_method():
            result = cnpj_utils.generate(type="numeric")

            assert len(result) == 14
            assert result.isdigit()

        def it_exposes_cnpj_gen_function():
            result = cnpj_gen({"type": "numeric"})

            assert len(result) == 14
            assert result.isdigit()

        def it_exposes_an_instantiable_cnpj_generator_class():
            generator = CnpjGenerator({"type": "alphabetic"})
            result = generator.generate({"prefix": "12345"})

            assert isinstance(generator, CnpjGenerator)
            assert len(result) == 14
            assert result.startswith("12345")
            assert result[5:12].isalpha()
            assert result[12:].isdigit()

        def it_exposes_an_instantiable_cnpj_generator_options_class():
            options = CnpjGeneratorOptions(
                {
                    "prefix": "AB123XYZ",
                    "type": "numeric",
                    "format": True,
                },
            )

            assert options.prefix == "AB123XYZ"
            assert options.type == "numeric"
            assert options.format is True

        def it_exposes_cnpj_generator_options_type_error_as_instantiable():
            error = CnpjGeneratorOptionsTypeError("prefix", 123, "string")

            assert error.actual_input == 123
            assert error.option_name == "prefix"
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert (
                str(error)
                == 'CNPJ generator option "prefix" must be of type string. Got integer number.'
            )

        def it_exposes_cnpj_generator_option_prefix_invalid_exception_as_instantiable():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "AB123XYZ", "some reason"
            )

            assert exception.actual_input == "AB123XYZ"
            assert exception.reason == "some reason"
            assert (
                str(exception)
                == 'CNPJ generator option "prefix" with value "AB123XYZ" is invalid. some reason'
            )

        def it_exposes_cnpj_generator_option_type_invalid_exception_as_instantiable():
            exception = CnpjGeneratorOptionTypeInvalidException("string", ["numeric"])

            assert exception.actual_input == "string"
            assert exception.expected_values == ["numeric"]
            assert (
                str(exception)
                == 'CNPJ generator option "type" accepts only the following values: "numeric". Got "string".'
            )

        def it_exposes_cnpj_generator_type_error_as_a_base_type():
            assert issubclass(CnpjGeneratorTypeError, TypeError)

        def it_exposes_cnpj_generator_exception_as_a_base_type():
            assert issubclass(CnpjGeneratorException, Exception)

    def describe_on_validating_module():
        def it_exposes_an_is_valid_method():
            assert cnpj_utils.is_valid("9JN7MGLJZXIO50") is True
            assert cnpj_utils.is_valid("9JN7MGLJZXIO51") is False

        def it_exposes_cnpj_val_function():
            assert cnpj_val("9JN7MGLJZXIO50") is True
            assert cnpj_val("9JN7MGLJZXIO51") is False

        def it_exposes_an_instantiable_cnpj_validator_class():
            validator = CnpjValidator({"type": "numeric"})
            result = validator.is_valid("12651319934215")

            assert isinstance(validator, CnpjValidator)
            assert result is True

        def it_exposes_an_instantiable_cnpj_validator_options_class():
            options = CnpjValidatorOptions(
                {
                    "case_sensitive": False,
                    "type": "numeric",
                },
            )

            assert options.case_sensitive is False
            assert options.type == "numeric"

        def it_exposes_cnpj_validator_input_type_error_as_instantiable():
            error = CnpjValidatorInputTypeError(123, "string")

            assert error.actual_input == 123
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert (
                str(error) == "CNPJ input must be of type string. Got integer number."
            )

        def it_exposes_cnpj_validator_options_type_error_as_instantiable():
            error = CnpjValidatorOptionsTypeError("prefix", 123, "string")

            assert error.actual_input == 123
            assert error.option_name == "prefix"
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert (
                str(error)
                == 'CNPJ validator option "prefix" must be of type string. Got integer number.'
            )

        def it_exposes_cnpj_validator_option_type_invalid_exception_as_instantiable():
            exception = CnpjValidatorOptionTypeInvalidException("string", ["numeric"])

            assert exception.actual_input == "string"
            assert exception.expected_values == ["numeric"]

        def it_exposes_cnpj_validator_type_error_as_a_base_type():
            assert issubclass(CnpjValidatorTypeError, TypeError)

        def it_exposes_cnpj_validator_exception_as_a_base_type():
            assert issubclass(CnpjValidatorException, Exception)
