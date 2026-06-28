"""Behavioral spec for the ``cnpj-fmt`` exception hierarchy.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-fmt/tests/exceptions.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-fmt/tests/specs/Exceptions.spec.php``), following the
rules documented in ``AGENTS.md`` §6.

Python decisions (see ``AGENTS.md`` §9):
- Concrete class names are read through ``type(err).__name__`` instead of the
  JS ``name`` instance property / PHP ``getName()`` method.
- Exception messages are read through ``str(err)`` (the idiomatic Python way).
- Public attributes use ``snake_case`` to match the target Python API.
"""

from cnpj_fmt import (
    CnpjFormatterException,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjFormatterOptionsTypeError,
    CnpjFormatterTypeError,
)


def describe_cnpj_formatter_type_error():
    def describe_when_instantiated_through_a_subclass():
        class _TestTypeError(CnpjFormatterTypeError):
            pass

        def it_is_an_instance_of_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_formatter_type_error():
            error = _TestTypeError(123, "number", "string", "some error")

            assert isinstance(error, CnpjFormatterTypeError)

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


def describe_cnpj_formatter_input_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjFormatterInputTypeError(123, "string")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_formatter_type_error():
            error = CnpjFormatterInputTypeError(123, "string")

            assert isinstance(error, CnpjFormatterTypeError)

        def it_has_the_correct_name():
            error = CnpjFormatterInputTypeError(123, "string")

            assert type(error).__name__ == "CnpjFormatterInputTypeError"

        def it_sets_the_actual_input_property():
            error = CnpjFormatterInputTypeError(123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjFormatterInputTypeError(123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjFormatterInputTypeError(123, "string or string[]")

            assert error.expected_type == "string or string[]"

        def it_generates_a_message_describing_the_error():
            error = CnpjFormatterInputTypeError(123, "string[]")

            assert (
                str(error) == "CNPJ input must be of type string[]. Got integer number."
            )


def describe_cnpj_formatter_options_type_error():
    def describe_when_instantiated():
        def it_is_an_instance_of_type_error():
            error = CnpjFormatterOptionsTypeError("hidden", 123, "boolean")

            assert isinstance(error, TypeError)

        def it_is_an_instance_of_cnpj_formatter_type_error():
            error = CnpjFormatterOptionsTypeError("hidden", 123, "boolean")

            assert isinstance(error, CnpjFormatterTypeError)

        def it_has_the_correct_name():
            error = CnpjFormatterOptionsTypeError("hidden", 123, "boolean")

            assert type(error).__name__ == "CnpjFormatterOptionsTypeError"

        def it_sets_the_option_name_property():
            error = CnpjFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.option_name == "hidden_key"

        def it_sets_the_actual_input_property():
            error = CnpjFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.actual_input == 123

        def it_sets_the_actual_type_property():
            error = CnpjFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.actual_type == "integer number"

        def it_sets_the_expected_type_property():
            error = CnpjFormatterOptionsTypeError("hidden_key", 123, "string")

            assert error.expected_type == "string"

        def it_generates_a_message_describing_the_error():
            error = CnpjFormatterOptionsTypeError("hidden_key", 123, "string")

            assert (
                str(error)
                == 'CNPJ formatting option "hidden_key" must be of type string. Got integer number.'
            )


def describe_cnpj_formatter_exception():
    def describe_when_instantiated_through_a_subclass():
        class _TestException(CnpjFormatterException):
            pass

        def it_is_an_instance_of_exception():
            exception = _TestException("some error")

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_formatter_exception():
            exception = _TestException("some error")

            assert isinstance(exception, CnpjFormatterException)

        def it_has_the_correct_name():
            exception = _TestException("some error")

            assert type(exception).__name__ == "_TestException"

        def it_has_the_correct_message():
            exception = _TestException("some error")

            assert str(exception) == "some error"


def describe_cnpj_formatter_input_length_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_formatter_exception():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert isinstance(exception, CnpjFormatterException)

        def it_has_the_correct_name():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert type(exception).__name__ == "CnpjFormatterInputLengthException"

        def it_sets_the_actual_input_property():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert exception.actual_input == "1.2.3.4.5"

        def it_sets_the_evaluated_input_property():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert exception.evaluated_input == "12345"

        def it_sets_the_expected_length_property():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert exception.expected_length == 14

        def it_generates_a_message_describing_the_exception():
            exception = CnpjFormatterInputLengthException("1.2.3.4.5", "12345", 14)

            assert (
                str(exception)
                == 'CNPJ input "1.2.3.4.5" does not contain 14 characters. Got 5 in "12345".'
            )

        def it_summarizes_sequence_input_without_serializing_its_contents():
            exception = CnpjFormatterInputLengthException(
                ["12", "345"],
                "12345",
                14,
            )

            assert exception.actual_input == ["12", "345"]
            assert (
                str(exception)
                == 'CNPJ input sequence[2] does not contain 14 characters. Got 5 in "12345".'
            )


def describe_cnpj_formatter_options_hidden_range_invalid_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_formatter_exception():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert isinstance(exception, CnpjFormatterException)

        def it_has_the_correct_name():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert (
                type(exception).__name__
                == "CnpjFormatterOptionsHiddenRangeInvalidException"
            )

        def it_sets_the_option_name_property():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert exception.option_name == "hidden_start"

        def it_sets_the_actual_input_property():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert exception.actual_input == 20

        def it_sets_the_min_expected_value_property():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert exception.min_expected_value == 5

        def it_sets_the_max_expected_value_property():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert exception.max_expected_value == 13

        def it_generates_a_message_describing_the_exception():
            exception = CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start", 20, 5, 13
            )

            assert (
                str(exception)
                == 'CNPJ formatting option "hidden_start" must be an integer between 5 and 13. Got 20.'
            )


def describe_cnpj_formatter_options_forbidden_key_character_exception():
    def describe_when_instantiated():
        def it_is_an_instance_of_exception():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert isinstance(exception, Exception)

        def it_is_an_instance_of_cnpj_formatter_exception():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert isinstance(exception, CnpjFormatterException)

        def it_has_the_correct_name():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert (
                type(exception).__name__
                == "CnpjFormatterOptionsForbiddenKeyCharacterException"
            )

        def it_sets_the_option_name_property():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "hidden_key", "x", ["x"]
            )

            assert exception.option_name == "hidden_key"

        def it_sets_the_actual_input_property():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "slash_key", "/", ["/"]
            )

            assert exception.actual_input == "/"

        def it_sets_the_forbidden_characters_property():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dash_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert exception.forbidden_characters == ["å", "ë", "ï", "ð"]

        def it_generates_a_message_describing_the_exception():
            exception = CnpjFormatterOptionsForbiddenKeyCharacterException(
                "dot_key", "å", ["å", "ë", "ï", "ð"]
            )

            assert (
                str(exception)
                == 'Value "å" for CNPJ formatting option "dot_key" contains disallowed characters ("å", "ë", "ï", "ð").'
            )
