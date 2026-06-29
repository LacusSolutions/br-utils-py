"""Behavioral spec for the ``cnpj-gen`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-gen/tests/exceptions.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-gen/tests/specs/Exceptions.spec.php``), following the
rules documented in ``AGENTS.md`` §6.

Python decisions (see ``AGENTS.md`` §8):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cnpj_gen import (
    CnpjGeneratorException,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjGeneratorTypeError,
)

TYPE_INVALID_EXPECTED_VALUES = ["alphabetic", "alphanumeric", "numeric"]


def describe_cnpj_generator_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CnpjGeneratorTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_generator_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CnpjGeneratorTypeError)

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


def describe_cnpj_generator_options_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjGeneratorOptionsTypeError("format", 123, "boolean")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_generator_type_error():
            error = CnpjGeneratorOptionsTypeError("format", 123, "boolean")

            assert isinstance(error, CnpjGeneratorTypeError)

        def it_has_the_correct_name():
            error = CnpjGeneratorOptionsTypeError("format", 123, "boolean")

            assert type(error).__name__ == "CnpjGeneratorOptionsTypeError"

        def it_sets_the_option_name_property():
            error = CnpjGeneratorOptionsTypeError("format", 123, "string")

            assert error.option_name == "format"

        def it_sets_the_actual_input_property():
            error = CnpjGeneratorOptionsTypeError("format", 123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjGeneratorOptionsTypeError("format", 123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjGeneratorOptionsTypeError("format", 123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CnpjGeneratorOptionsTypeError("format", 123, "string")

            assert (
                str(error)
                == 'CNPJ generator option "format" must be of type string. Got integer number.'
            )


def describe_cnpj_generator_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CnpjGeneratorException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_generator_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CnpjGeneratorException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cnpj_generator_option_prefix_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_generator_exception():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert isinstance(exception, CnpjGeneratorException)

        def it_has_the_correct_name():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert (
                type(exception).__name__ == "CnpjGeneratorOptionPrefixInvalidException"
            )

        def it_sets_the_actual_input_property():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "77777777", "repeated digits"
            )

            assert exception.actual_input == "77777777"

        def it_sets_the_reason_property():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert exception.reason == "repeated digits"

        def it_generates_a_message_describing_the_exception():
            exception = CnpjGeneratorOptionPrefixInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert (
                str(exception)
                == 'CNPJ generator option "prefix" with value "1.2.3.4.5" is invalid. repeated digits'
            )


def describe_cnpj_generator_option_type_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjGeneratorOptionTypeInvalidException(
                "boolean", TYPE_INVALID_EXPECTED_VALUES
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_generator_exception():
            exception = CnpjGeneratorOptionTypeInvalidException(
                "boolean", TYPE_INVALID_EXPECTED_VALUES
            )

            assert isinstance(exception, CnpjGeneratorException)

        def it_has_the_correct_name():
            exception = CnpjGeneratorOptionTypeInvalidException(
                "boolean", TYPE_INVALID_EXPECTED_VALUES
            )

            assert type(exception).__name__ == "CnpjGeneratorOptionTypeInvalidException"

        def it_sets_the_actual_input_property():
            exception = CnpjGeneratorOptionTypeInvalidException(
                "boolean", TYPE_INVALID_EXPECTED_VALUES
            )

            assert exception.actual_input == "boolean"

        def it_sets_the_expected_values_property():
            exception = CnpjGeneratorOptionTypeInvalidException(
                "boolean", TYPE_INVALID_EXPECTED_VALUES
            )

            assert exception.expected_values == TYPE_INVALID_EXPECTED_VALUES

        def it_generates_a_message_describing_the_exception():
            actual_input = "boolean"
            expected_values_string = '", "'.join(TYPE_INVALID_EXPECTED_VALUES)
            message = (
                f'CNPJ generator option "type" accepts only the following values: '
                f'"{expected_values_string}". Got "{actual_input}".'
            )

            exception = CnpjGeneratorOptionTypeInvalidException(
                actual_input, TYPE_INVALID_EXPECTED_VALUES
            )

            assert str(exception) == message
