"""Validator for CPF (Cadastro de Pessoa Física) identifiers."""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from cpf_dv import CpfCheckDigits

from .exceptions import CpfValidatorInputTypeError

if TYPE_CHECKING:
    from .types import CpfInput

CPF_LENGTH = 11
"""The standard length of a CPF (Cadastro de Pessoa Física) identifier (11
digits).
"""


_NON_DIGIT_PATTERN = re.compile(r"[^0-9]")


class CpfValidator:
    """Validator for CPF (Cadastro de Pessoa Física).

    Validates CPF strings according to the Brazilian CPF validation
    algorithm.
    """

    def is_valid(self, cpf_input: CpfInput) -> bool:
        """Validate a CPF input.

        A CPF is considered valid when, after stripping every non-digit
        character, it has exactly :data:`CPF_LENGTH` digits, its base is not an
        all-identical-digit sequence, and both check digits match the ones
        computed via the standard modulo-11 algorithm. Invalid values return
        ``False`` instead of raising.

        Raises:
            ``CpfValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
        """
        actual_input = self._to_string_input(cpf_input)
        sanitized_cpf = _NON_DIGIT_PATTERN.sub("", actual_input)

        if len(sanitized_cpf) != CPF_LENGTH:
            return False

        try:
            cpf_check_digits = CpfCheckDigits(sanitized_cpf)
        except Exception:
            return False

        return sanitized_cpf == cpf_check_digits.cpf

    def _to_string_input(self, cpf_input: Any) -> str:
        """Normalize the input to a string.

        Raises:
            ``CpfValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
        """
        if isinstance(cpf_input, str):
            return cpf_input

        if isinstance(cpf_input, Sequence) and not isinstance(cpf_input, str):
            for item in cpf_input:
                if not isinstance(item, str):
                    raise CpfValidatorInputTypeError(
                        cpf_input,
                        "string or string[]",
                    )

            return "".join(cpf_input)

        raise CpfValidatorInputTypeError(cpf_input, "string or string[]")


__all__ = ["CPF_LENGTH", "CpfValidator"]
