"""Exception hierarchy for the ``cnpj_gen`` package.

The package distinguishes between **errors** and **exceptions**:

- :class:`CnpjGeneratorTypeError` (extends the native
  :class:`TypeError`) signals incorrect API usage (the option is of the
  wrong *type*).
- :class:`CnpjGeneratorException` (extends the native
  :class:`Exception`) signals invalid or ineligible data (right type,
  bad value).
"""

from __future__ import annotations

from abc import ABC
from typing import Any

from lacus.utils import describe_type


def _describe_actual_type(value: Any) -> str:
    """Return a basic type label for ``describe_type`` error messages."""
    actual_type = describe_type(value)

    if actual_type == "dict":
        return "object"

    return actual_type


class CnpjGeneratorTypeError(TypeError, ABC):
    """Base error for all ``cnpj-gen`` type-related errors.

    This abstract class extends the native :class:`TypeError` and serves
    as the base for all type validation errors in the CNPJ generator. It
    stores ``actual_input``, ``actual_type``, and ``expected_type``.
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


class CnpjGeneratorOptionsTypeError(CnpjGeneratorTypeError):
    """Error raised when a generator option has an invalid type.

    The error message includes the ``option_name``, ``actual_type``,
    and ``expected_type``.
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
            f'CNPJ generator option "{option_name}" must be of type '
            f"{expected_type}. Got {actual_type}.",
        )
        self.option_name = option_name


class CnpjGeneratorException(Exception, ABC):
    """Base exception for all ``cnpj-gen`` rules-related errors.

    This abstract class extends the native :class:`Exception` and serves
    as the base for all non-type-related errors in
    :class:`~cnpj_gen.cnpj_generator.CnpjGenerator` and its
    dependencies. Suitable for validation errors, range errors, and
    other business logic exceptions that are not type-related.
    """


class CnpjGeneratorOptionPrefixInvalidException(CnpjGeneratorException):
    """Exception raised when the ``prefix`` option is invalid.

    Carries ``actual_input`` and ``reason``. This is a business logic
    exception; callers should catch it and handle it appropriately.
    """

    def __init__(self, actual_input: str, reason: str) -> None:
        super().__init__(
            f'CNPJ generator option "prefix" with value "{actual_input}" is invalid. {reason}'
        )
        self.actual_input = actual_input
        self.reason = reason


class CnpjGeneratorOptionTypeInvalidException(CnpjGeneratorException):
    """Exception raised when the ``type`` option is not allowed.

    The option must be one of the values in
    :data:`~cnpj_gen.types.CnpjType`. Carries ``actual_input`` and
    ``expected_values``. This is a business logic exception; callers
    should catch it and handle it appropriately.
    """

    def __init__(
        self,
        actual_input: str,
        expected_values: list[str] | tuple[str, ...],
    ) -> None:
        quoted = '", "'.join(expected_values)

        super().__init__(
            f'CNPJ generator option "type" accepts only the following values: '
            f'"{quoted}". Got "{actual_input}".'
        )
        self.actual_input = actual_input
        self.expected_values = list(expected_values)


__all__ = [
    "CnpjGeneratorException",
    "CnpjGeneratorOptionPrefixInvalidException",
    "CnpjGeneratorOptionTypeInvalidException",
    "CnpjGeneratorOptionsTypeError",
    "CnpjGeneratorTypeError",
]
