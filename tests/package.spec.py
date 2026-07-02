"""Spec for the public API surface of the ``cpf_dv`` package.

Mirrors the PHP ``Package.spec.php`` suite (and the API-surface assertions of
the JS ``output.spec.ts`` suite) following ``AGENTS.md`` §2 and §8.4.

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable, default
export). Those concern JS packaging only and have no Python equivalent.

Dropped from the PHP suite: class-level ``CpfCheckDigits.CPF_*`` constants.
Python ``cpf_dv`` exposes length constants at module scope only, mirroring
``cnpj_dv``.
"""

import cpf_dv
from cpf_dv import (
    CPF_MAX_LENGTH,
    CPF_MIN_LENGTH,
    CpfCheckDigits,
    CpfCheckDigitsException,
    CpfCheckDigitsInputInvalidException,
    CpfCheckDigitsInputLengthException,
    CpfCheckDigitsInputTypeError,
    CpfCheckDigitsTypeError,
)


def describe_the_cpf_dv_package_api():
    def describe_when_inspecting_constants():
        def it_exposes_cpf_min_length():
            assert CPF_MIN_LENGTH == 9

        def it_exposes_cpf_max_length():
            assert CPF_MAX_LENGTH == 11

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "CpfCheckDigits",
                "CpfCheckDigitsTypeError",
                "CpfCheckDigitsInputTypeError",
                "CpfCheckDigitsException",
                "CpfCheckDigitsInputInvalidException",
                "CpfCheckDigitsInputLengthException",
                "CpfInput",
                "CPF_MIN_LENGTH",
                "CPF_MAX_LENGTH",
            }

            assert expected_names.issubset(set(dir(cpf_dv)))

    def describe_when_inspecting_public_types():
        def it_exposes_cpf_check_digits_as_an_instantiable_class():
            instance = CpfCheckDigits("123456789")

            assert isinstance(instance, CpfCheckDigits)
            assert instance.first == "0"
            assert instance.second == "9"
            assert instance.cpf == "12345678909"

        def it_exposes_cpf_check_digits_type_error_as_a_base_type():
            assert issubclass(CpfCheckDigitsTypeError, TypeError)

        def it_exposes_cpf_check_digits_input_type_error_as_instantiable():
            instance = CpfCheckDigitsInputTypeError(123, "string")

            assert instance.actual_input == 123
            assert (
                str(instance) == "CPF input must be of type string. Got integer number."
            )

        def it_exposes_cpf_check_digits_exception_as_a_base_type():
            assert issubclass(CpfCheckDigitsException, Exception)

        def it_exposes_cpf_check_digits_input_invalid_exception_as_instantiable():
            instance = CpfCheckDigitsInputInvalidException("123", "some reason")

            assert instance.actual_input == "123"
            assert instance.reason == "some reason"
            assert str(instance) == 'CPF input "123" is invalid. some reason'

        def it_exposes_cpf_check_digits_input_length_exception_as_instantiable():
            instance = CpfCheckDigitsInputLengthException("x", "1", 9, 11)

            assert instance.min_expected_length == 9
            assert instance.max_expected_length == 11
