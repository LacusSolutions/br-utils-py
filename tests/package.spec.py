"""Spec for the public API surface of the ``cnpj_dv`` package.

Mirrors the PHP ``Package.spec.php`` suite (and the API-surface assertions of
the JS ``output.spec.ts`` suite) following ``AGENTS.md`` §2 and §9.

Dropped from the JS suite: every assertion about distribution bundles
(UMD/CJS/ESM build artifacts, ``.d.ts`` declarations, global variable, default
export). Those concern JS packaging only and have no Python equivalent.
"""

import cnpj_dv
from cnpj_dv import (
    CNPJ_MAX_LENGTH,
    CNPJ_MIN_LENGTH,
    CnpjCheckDigits,
    CnpjCheckDigitsException,
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
    CnpjCheckDigitsTypeError,
)


def describe_the_cnpj_dv_package_api():
    def describe_when_inspecting_constants():
        def it_exposes_cnpj_min_length():
            assert CNPJ_MIN_LENGTH == 12

        def it_exposes_cnpj_max_length():
            assert CNPJ_MAX_LENGTH == 14

    def describe_when_inspecting_public_names():
        def it_exports_all_public_resources():
            expected_names = {
                "CnpjCheckDigits",
                "CnpjCheckDigitsTypeError",
                "CnpjCheckDigitsInputTypeError",
                "CnpjCheckDigitsException",
                "CnpjCheckDigitsInputInvalidException",
                "CnpjCheckDigitsInputLengthException",
                "CNPJ_MIN_LENGTH",
                "CNPJ_MAX_LENGTH",
            }

            assert expected_names.issubset(set(dir(cnpj_dv)))

    def describe_when_inspecting_public_types():
        def it_exposes_cnpj_check_digits_as_an_instantiable_class():
            instance = CnpjCheckDigits("914157320007")

            assert isinstance(instance, CnpjCheckDigits)
            assert instance.first == "9"
            assert instance.second == "3"
            assert instance.cnpj == "91415732000793"

        def it_exposes_cnpj_check_digits_type_error_as_a_base_type():
            assert issubclass(CnpjCheckDigitsTypeError, TypeError)

        def it_exposes_cnpj_check_digits_input_type_error_as_instantiable():
            instance = CnpjCheckDigitsInputTypeError(123, "string")

            assert instance.actual_input == 123
            assert (
                str(instance)
                == "CNPJ input must be of type string. Got integer number."
            )

        def it_exposes_cnpj_check_digits_exception_as_a_base_type():
            assert issubclass(CnpjCheckDigitsException, Exception)

        def it_exposes_cnpj_check_digits_input_invalid_exception_as_instantiable():
            instance = CnpjCheckDigitsInputInvalidException("123", "some reason")

            assert instance.actual_input == "123"
            assert instance.reason == "some reason"
            assert str(instance) == 'CNPJ input "123" is invalid. some reason'

        def it_exposes_cnpj_check_digits_input_length_exception_as_instantiable():
            instance = CnpjCheckDigitsInputLengthException("x", "1", 12, 14)

            assert instance.min_expected_length == 12
            assert instance.max_expected_length == 14
