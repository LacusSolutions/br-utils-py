"""Exception hierarchy for the ``cpf_val`` package."""

from __future__ import annotations

from typing import Any

from lacus.utils import describe_type


class CpfValidatorTypeError(TypeError):
    """Base error class for all ``cpf-val`` type-related errors.

    This base class extends the native :class:`TypeError` and serves as the
    base for all type validation errors in the CPF validator.
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


class CpfValidatorInputTypeError(CpfValidatorTypeError):
    """Error raised when the CPF validator input has an invalid type.

    The input must match :data:`~cpf_val.types.CpfInput`. The error message
    includes both the actual input type and the expected type.
    """

    def __init__(self, actual_input: Any, expected_type: str) -> None:
        actual_type = describe_type(actual_input)
        super().__init__(
            actual_input,
            actual_type,
            expected_type,
            f"CPF input must be of type {expected_type}. Got {actual_type}.",
        )


class CpfValidatorException(Exception):
    """Base exception for all ``cpf-val`` rules-related errors.

    This base class extends the native :class:`Exception` and serves as the
    base for all non-type-related errors in
    :class:`~cpf_val.cpf_validator.CpfValidator` and its dependencies. It is
    suitable for validation errors, range errors, and other business logic
    exceptions that are not strictly type-related.
    """


__all__ = [
    "CpfValidatorException",
    "CpfValidatorInputTypeError",
    "CpfValidatorTypeError",
]
