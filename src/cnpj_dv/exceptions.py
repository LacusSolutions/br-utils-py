"""Exception hierarchy for the ``cnpj_dv`` package.

The package distinguishes between **errors** and **exceptions**:

- ``CnpjCheckDigitsTypeError`` (extends the native :class:`TypeError`)
  signals incorrect API usage (the input is of the wrong *type*).
- ``CnpjCheckDigitsException`` (extends the native :class:`Exception`)
  signals invalid or ineligible data (right type, bad value).
"""

import json
from typing import Any

from lacus.utils import describe_type

CnpjInput = str | list[str]


def _format_actual_input(actual_input: Any) -> str:
    """Format the original input for inclusion in an exception message."""
    if isinstance(actual_input, str):
        return f'"{actual_input}"'

    return json.dumps(actual_input, separators=(",", ":"), ensure_ascii=False)


class CnpjCheckDigitsTypeError(TypeError):
    """Base error for all ``cnpj_dv`` type-related errors.

    This class extends the native :class:`TypeError` and serves as the
    base for all type validation errors in the :class:`CnpjCheckDigits`.
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


class CnpjCheckDigitsInputTypeError(CnpjCheckDigitsTypeError):
    """Error raised when the input provided to :class:`CnpjCheckDigits` is
    not of the expected type (``str`` or ``list[str]``).

    The error message includes both the actual type of the input and the
    expected type.
    """

    def __init__(self, actual_input: Any, expected_type: str) -> None:
        actual_type = describe_type(actual_input)

        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f"CNPJ input must be of type {expected_type}. Got {actual_type}.",
        )


class CnpjCheckDigitsException(Exception):
    """Base exception for all ``cnpj_dv`` rules-related errors.

    This class extends the native :class:`Exception` and serves as the
    base for all non-type-related errors in the :class:`CnpjCheckDigits`.
    It is suitable for validation errors, range errors, and other business
    logic exceptions that are not strictly type-related.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CnpjCheckDigitsInputLengthException(CnpjCheckDigitsException):
    """Error raised when the input (after optional processing) does not
    have the required length to calculate the check digits.

    A valid CNPJ input must contain between 12 and 14 alphanumeric
    characters. The error message distinguishes between the original
    input and the evaluated one (which strips punctuation characters).
    """

    def __init__(
        self,
        actual_input: CnpjInput,
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
            f"CNPJ input {fmt_actual_input} does not contain "
            f"{min_expected_length} to {max_expected_length} digits. "
            f"Got {fmt_evaluated_input}."
        )
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length


class CnpjCheckDigitsInputInvalidException(CnpjCheckDigitsException):
    """Exception raised when the CNPJ input contains invalid character
    sequences, like all digits are repeated.

    This is a business logic exception and it is highly recommended that
    users of the library catch it and handle it appropriately.
    """

    def __init__(self, actual_input: CnpjInput, reason: str) -> None:
        fmt_actual_input = _format_actual_input(actual_input)

        super().__init__(f"CNPJ input {fmt_actual_input} is invalid. {reason}")
        self.actual_input = actual_input
        self.reason = reason
