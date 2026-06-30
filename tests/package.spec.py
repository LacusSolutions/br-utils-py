"""Spec for the public API surface of the ``cnpj_val`` package.

Mirrors the API-surface assertions of the JS ``output.spec.ts`` suite following
``AGENTS.md`` §2 and §9.

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable, default
export). Those concern JS packaging only and have no Python equivalent.
"""

import cnpj_val as cnpj_val_module
from cnpj_val import (
    CNPJ_LENGTH,
    CnpjValidator,
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptions,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    CnpjValidatorTypeError,
    cnpj_val,
)


def describe_the_cnpj_val_package_api():
    def describe_when_inspecting_constants():
        def it_exposes_cnpj_length():
            assert CNPJ_LENGTH == 14

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "cnpj_val",
                "CnpjValidator",
                "CnpjValidatorOptions",
                "CnpjValidatorTypeError",
                "CnpjValidatorInputTypeError",
                "CnpjValidatorOptionsTypeError",
                "CnpjValidatorException",
                "CnpjValidatorOptionTypeInvalidException",
                "CNPJ_LENGTH",
            }

            assert expected_names.issubset(set(dir(cnpj_val_module)))

    def describe_when_inspecting_public_types():
        def it_exposes_cnpj_val_as_a_callable_helper():
            assert callable(cnpj_val)

            assert cnpj_val("9JN7MGLJZXIO50") is True
            assert cnpj_val("9JN7MGLJZXIO51") is False

        def it_exposes_cnpj_validator_as_an_instantiable_class():
            validator = CnpjValidator({"type": "numeric"})
            result = validator.is_valid("12651319934215")

            assert isinstance(validator, CnpjValidator)
            assert result is True

        def it_exposes_cnpj_validator_options_as_an_instantiable_class():
            options = CnpjValidatorOptions(
                {
                    "case_sensitive": False,
                    "type": "numeric",
                }
            )

            assert options.case_sensitive is False
            assert options.type == "numeric"

        def it_exposes_cnpj_validator_type_error_as_a_base_type():
            assert issubclass(CnpjValidatorTypeError, TypeError)

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

        def it_exposes_cnpj_validator_exception_as_a_base_type():
            assert issubclass(CnpjValidatorException, Exception)

        def it_exposes_cnpj_validator_option_type_invalid_exception_as_instantiable():
            exception = CnpjValidatorOptionTypeInvalidException("string", ["numeric"])

            assert exception.actual_input == "string"
            assert exception.expected_values == ["numeric"]
