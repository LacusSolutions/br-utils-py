"""Helper function for CPF validation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cpf_validator import CpfValidator

if TYPE_CHECKING:
    from .types import CpfInput


def cpf_val(cpf_input: CpfInput) -> bool:
    """Helper function to simplify the usage of :class:`CpfValidator`.

    Validates a CPF string or sequence of strings and returns whether it is a
    valid Brazilian CPF.

    Raises:
        ``CpfValidatorInputTypeError``: If the input is not a string or
            sequence of strings.

    See Also:
        :class:`CpfValidator` for the detailed validation contract.
    """
    return CpfValidator().is_valid(cpf_input)


__all__ = ["cpf_val"]
