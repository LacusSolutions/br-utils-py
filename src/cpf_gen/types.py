"""Type aliases for the ``cpf_gen`` package."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias, TypedDict

from .cpf_generator_options import CpfGeneratorOptions


class CpfGeneratorOptionsType(TypedDict):
    """Configuration for CPF generation options.

    Defines the resolved options used internally: ``format`` (standard masking)
    and ``prefix`` (partial start string). All properties have default values
    when creating a :class:`~cpf_gen.cpf_generator_options.CpfGeneratorOptions`
    instance.

    Attributes:
        ``format``: Whether to format the generated CPF string as
            ``000.000.000-00``.
        ``prefix``: A partial string containing 0 to 9 digits to use as the
            start of the generated CPF. Only digits are kept; the rest is
            stripped. If provided, only the missing digits are generated
            randomly. For example, if the ``prefix`` ``123456`` (``6`` digits)
            is given, only the next 3 digits are randomly generated and
            concatenated to the ``prefix``.

            Note: If the evaluated ``prefix`` (after stripping non-digit
            characters) is longer than 9 digits, the extra digits are ignored,
            because a CPF has 9 base digits followed by 2 calculated check
            digits.
    """

    format: bool
    prefix: str


CpfGeneratorOptionsInput: TypeAlias = CpfGeneratorOptions | Mapping[str, Any] | None
"""Options input accepted by constructors and merge helpers.

May be a :class:`~cpf_gen.cpf_generator_options.CpfGeneratorOptions` instance,
a partial options ``Mapping[str, Any]``, or ``None``.
"""

__all__ = [
    "CpfGeneratorOptionsInput",
    "CpfGeneratorOptionsType",
]
