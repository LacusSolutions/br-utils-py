"""Exception hierarchy for the ``cpf_gen`` package.

The package distinguishes between **errors** and **exceptions**:

- :class:`CpfGeneratorTypeError` (extends the native :class:`TypeError`)
signals incorrect API usage (the option is of the wrong *type*).
- :class:`CpfGeneratorException` (extends the native :class:`Exception`)
  signals invalid or ineligible data (right type, bad value).
"""

from __future__ import annotations

from typing import Any

from lacus.utils import describe_type


def _describe_actual_type(value: Any) -> str:
    """Return a basic type label for ``describe_type`` error messages."""
    actual_type = describe_type(value)

    if actual_type == "dict":
        return "object"

    return actual_type


class CpfGeneratorTypeError(TypeError):
    """Base error for all ``cpf-gen`` type-related errors.

    This base class extends the native :class:`TypeError` and serves as the
    base for all type validation errors in the CPF generator. It stores
    ``actual_input``, ``actual_type``, and ``expected_type``.
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


class CpfGeneratorOptionsTypeError(CpfGeneratorTypeError):
    """Error raised when a generator option has an invalid type.

    The error message includes the ``option_name``, ``actual_type``, and
    ``expected_type``.
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
            f'CPF generator option "{option_name}" must be of type '
            f"{expected_type}. Got {actual_type}.",
        )
        self.option_name = option_name


class CpfGeneratorException(Exception):
    """Base exception for all ``cpf-gen`` rules-related errors.

    This base class extends the native :class:`Exception` and serves as the
    base for all non-type-related errors in
    :class:`~cpf_gen.cpf_generator.CpfGenerator` and its dependencies. Suitable
    for validation errors, range errors, and other business logic exceptions
    that are not type-related.
    """


class CpfGeneratorOptionPrefixInvalidException(CpfGeneratorException):
    """Exception raised when the ``prefix`` option is invalid.

    Carries ``actual_input`` and ``reason``. This is a business logic
    exception; callers should catch it and handle it appropriately.
    """

    def __init__(self, actual_input: str, reason: str) -> None:
        super().__init__(
            f'CPF generator option "prefix" with value "{actual_input}" is invalid. {reason}'
        )
        self.actual_input = actual_input
        self.reason = reason


__all__ = [
    "CpfGeneratorException",
    "CpfGeneratorOptionPrefixInvalidException",
    "CpfGeneratorOptionsTypeError",
    "CpfGeneratorTypeError",
]
