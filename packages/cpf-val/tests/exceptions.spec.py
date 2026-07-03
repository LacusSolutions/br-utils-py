"""Behavioral spec for the ``cpf-val`` exception hierarchy.

Mirrors the JavaScript reference suite
(``js/packages/cpf-val/tests/exceptions.spec.ts``), following the rules
documented in ``AGENTS.md`` §6. PHP ``cpf-val`` defines no package-specific
exception classes (it relies on the native ``TypeError``), so there are no PHP
cases to combine here.

Kept parallel with the CNPJ mirror
(``python/packages/cnpj-val/tests/exceptions.spec.py``) for the shared classes;
the CNPJ ``*Options*`` exception specs are intentionally absent (CPF has no
options — see ``AGENTS.md`` §9.3).

Python decisions (see ``AGENTS.md`` §9):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cpf_val import (
    CpfValidatorException,
    CpfValidatorInputTypeError,
    CpfValidatorTypeError,
)


def describe_cpf_validator_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CpfValidatorTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_validator_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CpfValidatorTypeError)

        def it_has_the_correct_name():
            error = _TestTypeError(123, "number", "string", "some error")

            assert type(error).__name__ == "_TestTypeError"

        def it_sets_the_actual_input_property():
            error = _TestTypeError(123, "number", "string", "some error")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = _TestTypeError(123, "number", "string", "some error")

            assert error.actual_type == "number"

        def it_sets_the_expected_type_property():
            error = _TestTypeError(123, "number", "string", "some error")

            assert error.expected_type == "string"

        def it_has_the_correct_message():
            error = _TestTypeError(123, "number", "string", "some error")

            assert str(error) == "some error"


def describe_cpf_validator_input_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CpfValidatorInputTypeError(123, "string")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_validator_type_error():
            error = CpfValidatorInputTypeError(123, "string")

            assert isinstance(error, CpfValidatorTypeError)

        def it_has_the_correct_name():
            error = CpfValidatorInputTypeError(123, "string")

            assert type(error).__name__ == "CpfValidatorInputTypeError"

        def it_sets_the_actual_input_property():
            error = CpfValidatorInputTypeError(123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CpfValidatorInputTypeError(123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CpfValidatorInputTypeError(123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CpfValidatorInputTypeError(123, "string")

            assert str(error) == "CPF input must be of type string. Got integer number."


def describe_cpf_validator_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CpfValidatorException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_validator_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CpfValidatorException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"
