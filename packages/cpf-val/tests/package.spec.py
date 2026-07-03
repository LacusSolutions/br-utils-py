"""Spec for the public API surface of the ``cpf_val`` package.

Mirrors the API-surface assertions of the JS ``output.spec.ts`` suite
(``js/packages/cpf-val/tests/output.spec.ts``) following ``AGENTS.md`` §3 and §9,
and stays parallel with the CNPJ mirror
(``python/packages/cnpj-val/tests/package.spec.py``).

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable, default
export). Those concern JS packaging only and have no Python equivalent. The
CNPJ ``*Options*`` public symbols are intentionally absent (CPF has no
options — see ``AGENTS.md`` §9.3).
"""

import cpf_val as cpf_val_module
from cpf_val import (
    CPF_LENGTH,
    CpfValidator,
    CpfValidatorException,
    CpfValidatorInputTypeError,
    CpfValidatorTypeError,
    cpf_val,
)


def describe_the_cpf_val_package_api():
    def describe_when_inspecting_constants():
        def it_exposes_cpf_length():
            assert CPF_LENGTH == 11

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "cpf_val",
                "CpfValidator",
                "CpfValidatorTypeError",
                "CpfValidatorInputTypeError",
                "CpfValidatorException",
                "CPF_LENGTH",
            }

            assert expected_names.issubset(set(dir(cpf_val_module)))

    def describe_when_inspecting_public_types():
        def it_exposes_cpf_val_as_a_callable_helper():
            assert callable(cpf_val)

            assert cpf_val("33528612690") is True
            assert cpf_val("33528612691") is False

        def it_exposes_cpf_validator_as_an_instantiable_class():
            validator = CpfValidator()
            result = validator.is_valid("33528612690")

            assert isinstance(validator, CpfValidator)
            assert result is True

        def it_exposes_cpf_validator_type_error_as_a_base_type():
            assert issubclass(CpfValidatorTypeError, TypeError)

        def it_exposes_cpf_validator_input_type_error_as_instantiable():
            error = CpfValidatorInputTypeError(123, "string")

            assert error.actual_input == 123
            assert error.actual_type == "integer number"
            assert error.expected_type == "string"
            assert str(error) == "CPF input must be of type string. Got integer number."

        def it_exposes_cpf_validator_exception_as_a_base_type():
            assert issubclass(CpfValidatorException, Exception)
