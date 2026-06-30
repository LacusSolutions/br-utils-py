"""Exception hierarchy for the ``cnpj_val`` package."""

from __future__ import annotations

from abc import ABC
from typing import Any

from lacus.utils import describe_type


def _describe_actual_type(value: Any) -> str:
    """Return a basic type label for option type-error messages."""
    actual_type = describe_type(value)

    if actual_type == "dict":
        return "object"

    return actual_type


class CnpjValidatorTypeError(TypeError, ABC):
    """Base error class for all ``cnpj-val`` type-related errors.

    This abstract class extends the native :class:`TypeError` and serves as the
    base for all type validation errors in the CNPJ validator.
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


class CnpjValidatorInputTypeError(CnpjValidatorTypeError):
    """Error raised when the CNPJ validator input has an invalid type.

    The input must match :data:`~cnpj_val.types.CnpjInput`. The error message
    includes both the actual input type and the expected type.
    """

    def __init__(self, actual_input: Any, expected_type: str) -> None:
        actual_type = describe_type(actual_input)
        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f"CNPJ input must be of type {expected_type}. Got {actual_type}.",
        )


class CnpjValidatorOptionsTypeError(CnpjValidatorTypeError):
    """Error raised when a validator option has an invalid type.

    The error message includes the option name, the actual input type, and the
    expected type.
    """

    def __init__(
        self,
        option_name: str,
        actual_input: Any,
        expected_type: str,
    ) -> None:
        actual_type = _describe_actual_type(actual_input)
        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f'CNPJ validator option "{option_name}" must be of type '
            f"{expected_type}. Got {actual_type}.",
        )
        self.option_name = option_name


class CnpjValidatorException(Exception, ABC):
    """Base exception for all ``cnpj-val`` rules-related errors.

    This abstract class extends the native :class:`Exception` and serves
    as the base for all non-type-related errors in
    :class:`~cnpj_val.cnpj_validator.CnpjValidator` and its
    dependencies. It is suitable for validation errors, range errors, and other
    business logic exceptions that are not strictly type-related.
    """


class CnpjValidatorOptionTypeInvalidException(CnpjValidatorException):
    """Exception raised when the ``type`` option value is not allowed.

    The option must be one of the enumerated values of
    :data:`~cnpj_val.types.CnpjType`. This is a business logic exception; it is
    highly recommended that users of the library catch it and handle it
    appropriately.
    """

    def __init__(
        self,
        actual_input: str,
        expected_values: list[str] | tuple[str, ...],
    ) -> None:
        quoted = '", "'.join(expected_values)
        super().__init__(
            f'CNPJ validator option "type" accepts only the following values: '
            f'"{quoted}". Got "{actual_input}".'
        )
        self.actual_input = actual_input
        self.expected_values = list(expected_values)


__all__ = [
    "CnpjValidatorException",
    "CnpjValidatorInputTypeError",
    "CnpjValidatorOptionTypeInvalidException",
    "CnpjValidatorOptionsTypeError",
    "CnpjValidatorTypeError",
]
