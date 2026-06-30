"""Behavioral spec for the ``cnpj-val`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-val/tests/exceptions.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-val/tests/specs/Exceptions.spec.php``), following the
rules documented in ``AGENTS.md`` §6.

Python decisions (see ``AGENTS.md`` §9):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cnpj_val import (
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    CnpjValidatorTypeError,
)


def describe_cnpj_validator_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CnpjValidatorTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_validator_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CnpjValidatorTypeError)

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


def describe_cnpj_validator_input_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjValidatorInputTypeError(123, "string")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_validator_type_error():
            error = CnpjValidatorInputTypeError(123, "string")

            assert isinstance(error, CnpjValidatorTypeError)

        def it_has_the_correct_name():
            error = CnpjValidatorInputTypeError(123, "string")

            assert type(error).__name__ == "CnpjValidatorInputTypeError"

        def it_sets_the_actual_input_property():
            error = CnpjValidatorInputTypeError(123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjValidatorInputTypeError(123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjValidatorInputTypeError(123, "string or string[]")

            assert error.expected_type == "string or string[]"

        def it_generates_a_message_describing_the_error():
            error = CnpjValidatorInputTypeError(123, "string")

            assert (
                str(error) == "CNPJ input must be of type string. Got integer number."
            )


def describe_cnpj_validator_options_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjValidatorOptionsTypeError("type", 123, "boolean")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_validator_type_error():
            error = CnpjValidatorOptionsTypeError("type", 123, "boolean")

            assert isinstance(error, CnpjValidatorTypeError)

        def it_has_the_correct_name():
            error = CnpjValidatorOptionsTypeError("type", 123, "boolean")

            assert type(error).__name__ == "CnpjValidatorOptionsTypeError"

        def it_sets_the_option_name_property():
            error = CnpjValidatorOptionsTypeError("type", 123, "string")

            assert error.option_name == "type"

        def it_sets_the_actual_input_property():
            error = CnpjValidatorOptionsTypeError("type", 123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjValidatorOptionsTypeError("type", 123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjValidatorOptionsTypeError("type", 123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CnpjValidatorOptionsTypeError("type", 123, "string")

            assert (
                str(error)
                == 'CNPJ validator option "type" must be of type string. Got integer number.'
            )


def describe_cnpj_validator_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CnpjValidatorException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_validator_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CnpjValidatorException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cnpj_validator_option_type_invalid_exception():
    expected_values = ["alphabetic", "alphanumeric", "numeric"]

    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_validator_exception():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert isinstance(exception, CnpjValidatorException)

        def it_has_the_correct_name():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert type(exception).__name__ == "CnpjValidatorOptionTypeInvalidException"

        def it_sets_the_actual_input_property():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert exception.actual_input == "boolean"

        def it_sets_the_expected_values_property():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert exception.expected_values == expected_values

        def it_generates_a_message_describing_the_exception():
            exception = CnpjValidatorOptionTypeInvalidException(
                "boolean",
                expected_values,
            )

            assert (
                str(exception)
                == 'CNPJ validator option "type" accepts only the following values: '
                '"alphabetic", "alphanumeric", "numeric". Got "boolean".'
            )
