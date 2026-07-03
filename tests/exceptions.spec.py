"""Behavioral spec for the ``cpf-fmt`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-fmt/tests/exceptions.spec.ts``) and the PHP reference suite
formatting-error expectations documented in ``AGENTS.md``.

Python decisions (see ``AGENTS.md`` §8):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cpf_fmt import (
    CpfFormatterException,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
    CpfFormatterOptionsForbiddenKeyCharacterException,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfFormatterOptionsTypeError,
    CpfFormatterTypeError,
)


def describe_cpf_formatter_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CpfFormatterTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_formatter_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CpfFormatterTypeError)

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


def describe_cpf_formatter_input_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CpfFormatterInputTypeError(123, "string")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_formatter_type_error():
            error = CpfFormatterInputTypeError(123, "string")

            assert isinstance(error, CpfFormatterTypeError)

        def it_has_the_correct_name():
            error = CpfFormatterInputTypeError(123, "string")

            assert type(error).__name__ == "CpfFormatterInputTypeError"

        def it_sets_the_actual_input_property():
            error = CpfFormatterInputTypeError(123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CpfFormatterInputTypeError(123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CpfFormatterInputTypeError(123, "string or string[]")

            assert error.expected_type == "string or string[]"

        def it_generates_a_message_describing_the_error():
            error = CpfFormatterInputTypeError(123, "string[]")

            assert (
                str(error) == "CPF input must be of type string[]. Got integer number."
            )


def describe_cpf_formatter_options_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CpfFormatterOptionsTypeError("hidden", 123, "boolean")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cpf_formatter_type_error():
            error = CpfFormatterOptionsTypeError("hidden", 123, "boolean")

            assert isinstance(error, CpfFormatterTypeError)

        def it_has_the_correct_name():
            error = CpfFormatterOptionsTypeError("hidden", 123, "boolean")

            assert type(error).__name__ == "CpfFormatterOptionsTypeError"

        def it_sets_the_option_name_property():
            error = CpfFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.option_name == "hidden_key"

        def it_sets_the_actual_input_property():
            error = CpfFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CpfFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CpfFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CpfFormatterOptionsTypeError("hidden_key", 123, "string")

            assert (
                str(error)
                == 'CPF formatting option "hidden_key" must be of type string. Got integer number.'
            )


def describe_cpf_formatter_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CpfFormatterException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_formatter_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CpfFormatterException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cpf_formatter_input_length_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_formatter_exception():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert isinstance(exception, CpfFormatterException)

        def it_has_the_correct_name():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert type(exception).__name__ == "CpfFormatterInputLengthException"

        def it_sets_the_actual_input_property():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert exception.actual_input == "1.2.3.4.5"

        def it_sets_the_evaluated_input_property():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert exception.evaluated_input == "12345"

        def it_sets_the_expected_length_property():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert exception.expected_length == 11

        def it_generates_a_message_describing_the_exception():
            exception = CpfFormatterInputLengthException("1.2.3.4.5", "12345", 11)

            assert (
                str(exception)
                == 'CPF input "1.2.3.4.5" does not contain 11 digits. Got 5 in "12345".'
            )

        def it_summarizes_sequence_input_without_serializing_its_contents():
            exception = CpfFormatterInputLengthException(
                ["123", "45"],
                "12345",
                11,
            )

            assert exception.actual_input == ["123", "45"]
            assert (
                str(exception)
                == 'CPF input sequence[2] does not contain 11 digits. Got 5 in "12345".'
            )


def describe_cpf_formatter_options_hidden_range_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_formatter_exception():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert isinstance(exception, CpfFormatterException)

        def it_has_the_correct_name():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert (
                type(exception).__name__
                == "CpfFormatterOptionsHiddenRangeInvalidException"
            )

        def it_sets_the_option_name_property():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert exception.option_name == "hidden_start"

        def it_sets_the_actual_input_property():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert exception.actual_input == 20

        def it_sets_the_min_expected_value_property():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert exception.min_expected_value == 0

        def it_sets_the_max_expected_value_property():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert exception.max_expected_value == 10

        def it_generates_a_message_describing_the_exception():
            exception = CpfFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 0, 10
            )

            assert (
                str(exception)
                == 'CPF formatting option "hidden_start" must be an integer between 0 and 10. Got 20.'
            )


def describe_cpf_formatter_options_forbidden_key_character_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cpf_formatter_exception():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert isinstance(exception, CpfFormatterException)

        def it_has_the_correct_name():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert (
                type(exception).__name__
                == "CpfFormatterOptionsForbiddenKeyCharacterException"
            )

        def it_sets_the_option_name_property():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "hidden_key", "x", ["x"]
            )

            assert exception.option_name == "hidden_key"

        def it_sets_the_actual_input_property():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "/", ["/"]
            )

            assert exception.actual_input == "/"

        def it_sets_the_forbidden_characters_property():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dash_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert exception.forbidden_characters == ["å", "ë", "ï", "ð"]

        def it_generates_a_message_describing_the_exception():
            exception = CpfFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert (
                str(exception)
                == 'Value "å" for CPF formatting option "dot_key" contains disallowed characters ("å", "ë", "ï", "ð").'
            )
