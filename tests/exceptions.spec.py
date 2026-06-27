"""Behavioral spec for the ``cnpj-dv`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-dv/tests/exceptions.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-dv/tests/specs/Exceptions.spec.php``), following the rules
documented in ``AGENTS.md`` §2.3.

Python decisions (see ``AGENTS.md`` §9):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method (divergence #4).
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the existing Python codebase.
"""

from cnpj_dv import (
    CnpjCheckDigitsException,
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
    CnpjCheckDigitsTypeError,
)


def describe_cnpj_check_digits_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CnpjCheckDigitsTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_check_digits_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CnpjCheckDigitsTypeError)

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


def describe_cnpj_check_digits_input_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjCheckDigitsInputTypeError(123, "string")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_check_digits_type_error():
            error = CnpjCheckDigitsInputTypeError(123, "string")

            assert isinstance(error, CnpjCheckDigitsTypeError)

        def it_has_the_correct_name():
            error = CnpjCheckDigitsInputTypeError(123, "string")

            assert type(error).__name__ == "CnpjCheckDigitsInputTypeError"

        def it_sets_the_actual_input_property():
            error = CnpjCheckDigitsInputTypeError(123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjCheckDigitsInputTypeError(123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjCheckDigitsInputTypeError(123, "string or string[]")

            assert error.expected_type == "string or string[]"

        def it_generates_a_message_describing_the_error():
            error = CnpjCheckDigitsInputTypeError(123, "string[]")

            assert (
                str(error) == "CNPJ input must be of type string[]. Got integer number."
            )


def describe_cnpj_check_digits_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CnpjCheckDigitsException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_check_digits_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CnpjCheckDigitsException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cnpj_check_digits_input_length_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_check_digits_exception():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert isinstance(exception, CnpjCheckDigitsException)

        def it_has_the_correct_name():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert type(exception).__name__ == "CnpjCheckDigitsInputLengthException"

        def it_sets_the_actual_input_property():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert exception.actual_input == "1.2.3.4.5"

        def it_sets_the_evaluated_input_property():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert exception.evaluated_input == "12345"

        def it_sets_the_min_expected_length_property():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert exception.min_expected_length == 12

        def it_sets_the_max_expected_length_property():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert exception.max_expected_length == 14

        def it_generates_a_message_describing_the_exception():
            exception = CnpjCheckDigitsInputLengthException(
                "1.2.3.4.5", "12345", 12, 14
            )

            assert (
                str(exception)
                == 'CNPJ input "1.2.3.4.5" does not contain 12 to 14 digits. Got 5 in "12345".'
            )


def describe_cnpj_check_digits_input_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_check_digits_exception():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert isinstance(exception, CnpjCheckDigitsException)

        def it_has_the_correct_name():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert type(exception).__name__ == "CnpjCheckDigitsInputInvalidException"

        def it_sets_the_actual_input_property():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert exception.actual_input == "1.2.3.4.5"

        def it_sets_the_reason_property():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert exception.reason == "repeated digits"

        def it_generates_a_message_describing_the_exception():
            exception = CnpjCheckDigitsInputInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert (
                str(exception) == 'CNPJ input "1.2.3.4.5" is invalid. repeated digits'
            )
