"""Behavioral spec for the ``cpf-gen`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-gen/tests/exceptions.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-gen/tests/specs/Exceptions.spec.php`` — CPF has no
package-specific PHP exception tests), following the rules documented in
``AGENTS.md`` §6.

Python decisions (see ``AGENTS.md`` §8):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cpf_gen import (
    CpfGeneratorException,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptionsTypeError,
    CpfGeneratorTypeError,
)


def describe_cpf_generator_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CpfGeneratorTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_generator_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CpfGeneratorTypeError)

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


def describe_cpf_generator_options_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CpfGeneratorOptionsTypeError("format", 123, "boolean")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_generator_type_error():
            error = CpfGeneratorOptionsTypeError("format", 123, "boolean")

            assert isinstance(error, CpfGeneratorTypeError)

        def it_has_the_correct_name():
            error = CpfGeneratorOptionsTypeError("format", 123, "boolean")

            assert type(error).__name__ == "CpfGeneratorOptionsTypeError"

        def it_sets_the_option_name_property():
            error = CpfGeneratorOptionsTypeError("format", 123, "string")

            assert error.option_name == "format"

        def it_sets_the_actual_input_property():
            error = CpfGeneratorOptionsTypeError("format", 123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CpfGeneratorOptionsTypeError("format", 123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CpfGeneratorOptionsTypeError("format", 123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CpfGeneratorOptionsTypeError("format", 123, "string")

            assert (
                str(error)
                == 'CPF generator option "format" must be of type string. Got integer number.'
            )


def describe_cpf_generator_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CpfGeneratorException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_generator_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CpfGeneratorException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cpf_generator_option_prefix_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_generator_exception():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert isinstance(exception, CpfGeneratorException)

        def it_has_the_correct_name():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert (
                type(exception).__name__ == "CpfGeneratorOptionPrefixInvalidException"
            )

        def it_sets_the_actual_input_property():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "77777777", "repeated digits"
            )

            assert exception.actual_input == "77777777"

        def it_sets_the_reason_property():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "000000000000", "repeated digits"
            )

            assert exception.reason == "repeated digits"

        def it_generates_a_message_describing_the_exception():
            exception = CpfGeneratorOptionPrefixInvalidException(
                "1.2.3.4.5", "repeated digits"
            )

            assert (
                str(exception)
                == 'CPF generator option "prefix" with value "1.2.3.4.5" is invalid. repeated digits'
            )
