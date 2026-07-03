"""Exception hierarchy for the ``cpf_fmt`` package.

The package distinguishes between **errors** and **exceptions**:

- :class:`CpfFormatterTypeError` (extends the native
  :class:`TypeError`) signals incorrect API usage (the input or option
  is of the wrong *type*).
- :class:`CpfFormatterException` (extends the native
  :class:`Exception`) signals invalid or ineligible data (right type,
  bad value).
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from lacus.utils import describe_type

if TYPE_CHECKING:
    from .types import CpfInput


class CpfFormatterTypeError(TypeError, ABC):
    """Base error for all ``cpf-fmt`` type-related errors.

    This abstract class extends the native :class:`TypeError` and serves
    as the base for all type validation errors in the CPF formatter. It
    ensures proper inheritance and stores the actual input, actual type,
    and expected type.
    """

    def __init__(
        self,
        actual_input: Any,
        actual_type: str,
        expected_type: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.actual_input = actual_input
        self.actual_type = actual_type
        self.expected_type = expected_type


class CpfFormatterInputTypeError(CpfFormatterTypeError):
    """Error raised when the input provided to the CPF formatter is not
    of the expected type :data:`~cpf_fmt.types.CpfInput`.

    The error message includes both the actual input type and the
    expected type.
    """

    def __init__(self, actual_input: Any, expected_type: str) -> None:
        actual_type = describe_type(actual_input)
        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f"CPF input must be of type {expected_type}. Got {actual_type}.",
        )


class CpfFormatterOptionsTypeError(CpfFormatterTypeError):
    """Error raised when a specific option in the formatter configuration
    has an invalid type.

    The error message includes the option name, the actual input type
    and the expected type.
    """

    def __init__(
        self,
        option_name: str,
        actual_input: Any,
        expected_type: str,
    ) -> None:
        actual_type = describe_type(actual_input)
        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f'CPF formatting option "{option_name}" must be of type '
            f"{expected_type}. Got {actual_type}.",
        )
        self.option_name = option_name


class CpfFormatterException(Exception, ABC):
    """Base exception for all ``cpf-fmt`` rules-related errors.

    This abstract class extends the native :class:`Exception` and serves
    as the base for all non-type-related errors in the
    :class:`~cpf_fmt.cpf_formatter.CpfFormatter` and its dependencies. It
    is suitable for validation errors, range errors, and other business
    logic exceptions that are not strictly type-related.
    """


def _format_length_exception_input(actual_input: CpfInput) -> str:
    if isinstance(actual_input, str):
        return f'"{actual_input}"'

    if isinstance(actual_input, Sequence):
        return f"sequence[{len(actual_input)}]"

    return repr(actual_input)


class CpfFormatterInputLengthException(CpfFormatterException):
    """Exception raised when the CPF string input (after optional
    processing) does not have the required length.

    A valid CPF must contain exactly 11 digits. The error message
    distinguishes between the original input and the evaluated one (which
    strips punctuation characters).
    """

    def __init__(
        self,
        actual_input: CpfInput,
        evaluated_input: str,
        expected_length: int,
    ) -> None:
        fmt_actual_input = _format_length_exception_input(actual_input)
        fmt_evaluated_input = (
            f"{len(evaluated_input)}"
            if actual_input == evaluated_input
            else f'{len(evaluated_input)} in "{evaluated_input}"'
        )
        super().__init__(
            f"CPF input {fmt_actual_input} does not contain "
            f"{expected_length} digits. Got {fmt_evaluated_input}."
        )
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.expected_length = expected_length


class CpfFormatterOptionsHiddenRangeInvalidException(CpfFormatterException):
    """Exception raised when ``hidden_start`` or ``hidden_end`` option
    values are outside the valid range for CPF formatting.

    The valid range bounds are between 0 and 10 (inclusive), representing
    the indices of the 11-digit CPF string. The error message includes the
    option name, the actual input value, and the expected range bounds.
    """

    def __init__(
        self,
        option_name: str,
        actual_input: int,
        min_expected_value: int,
        max_expected_value: int,
    ) -> None:
        super().__init__(
            f'CPF formatting option "{option_name}" must be an integer '
            f"between {min_expected_value} and {max_expected_value}. "
            f"Got {actual_input}."
        )
        self.option_name = option_name
        self.actual_input = actual_input
        self.min_expected_value = min_expected_value
        self.max_expected_value = max_expected_value


class CpfFormatterOptionsForbiddenKeyCharacterException(CpfFormatterException):
    """Exception raised when a character is not allowed to be used as a
    key character on options.
    """

    def __init__(
        self,
        option_name: str,
        actual_input: str,
        forbidden_characters: Sequence[str],
    ) -> None:
        quoted = '", "'.join(forbidden_characters)
        super().__init__(
            f'Value "{actual_input}" for CPF formatting option '
            f'"{option_name}" contains disallowed characters '
            f'("{quoted}").'
        )
        self.option_name = option_name
        self.actual_input = actual_input
        self.forbidden_characters = list(forbidden_characters)


__all__ = [
    "CpfFormatterException",
    "CpfFormatterInputLengthException",
    "CpfFormatterInputTypeError",
    "CpfFormatterOptionsForbiddenKeyCharacterException",
    "CpfFormatterOptionsHiddenRangeInvalidException",
    "CpfFormatterOptionsTypeError",
    "CpfFormatterTypeError",
]
