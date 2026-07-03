"""Exception hierarchy for the ``cpf_dv`` package.

The package distinguishes between **errors** and **exceptions**:

- ``CpfCheckDigitsTypeError`` (extends the native :class:`TypeError`) signals
  incorrect API usage (the input is of the wrong *type*).
- ``CpfCheckDigitsException`` (extends the native :class:`Exception`) signals
  invalid or ineligible data (right type, bad value).
"""

import json
from typing import Any

from lacus.utils import describe_type

from .types import CpfInput


def _format_actual_input(actual_input: Any) -> str:
    """Format the original input for inclusion in an exception message."""
    if isinstance(actual_input, str):
        return f'"{actual_input}"'

    return json.dumps(actual_input, separators=(",", ":"), ensure_ascii=False)


class CpfCheckDigitsTypeError(TypeError):
    """Base error for all ``cpf_dv`` type-related errors.

    This class extends the native :class:`TypeError` and serves as the base for
    all type validation errors in the :class:`CpfCheckDigits`.
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


class CpfCheckDigitsInputTypeError(CpfCheckDigitsTypeError):
    """Error raised when the input provided to :class:`CpfCheckDigits` is not
    of the expected type (``str`` or ``list[str]``).

    The error message includes both the actual type of the input and the
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


class CpfCheckDigitsException(Exception):
    """Base exception for all ``cpf_dv`` rules-related errors.

    This class extends the native :class:`Exception` and serves as the base for
    all non-type-related errors in the :class:`CpfCheckDigits`. It is suitable
    for validation errors, range errors, and other business logic exceptions
    that are not strictly type-related.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CpfCheckDigitsInputLengthException(CpfCheckDigitsException):
    """Error raised when the input (after optional processing) does not have
    the required length to calculate the check digits.

    A valid CPF input must contain between 9 and 11 numeric characters. The
    error message distinguishes between the original input and the evaluated
    one (which strips punctuation characters).
    """

    def __init__(
        self,
        actual_input: CpfInput,
        evaluated_input: str,
        min_expected_length: int,
        max_expected_length: int,
    ) -> None:
        fmt_actual_input = _format_actual_input(actual_input)
        fmt_evaluated_input = (
            f"{len(evaluated_input)}"
            if actual_input == evaluated_input
            else f'{len(evaluated_input)} in "{evaluated_input}"'
        )

        super().__init__(
            f"CPF input {fmt_actual_input} does not contain "
            f"{min_expected_length} to {max_expected_length} digits. "
            f"Got {fmt_evaluated_input}."
        )
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length


class CpfCheckDigitsInputInvalidException(CpfCheckDigitsException):
    """Exception raised when the CPF input contains invalid character
    sequences, like all digits are repeated.

    This is a business logic exception and it is highly recommended that users
    of the library catch it and handle it appropriately.
    """

    def __init__(self, actual_input: CpfInput, reason: str) -> None:
        fmt_actual_input = _format_actual_input(actual_input)

        super().__init__(f"CPF input {fmt_actual_input} is invalid. {reason}")
        self.actual_input = actual_input
        self.reason = reason
