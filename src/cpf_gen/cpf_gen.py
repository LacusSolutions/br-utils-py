"""Convenience wrapper around :class:`~cpf_gen.cpf_generator.CpfGenerator`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cpf_generator import CpfGenerator

if TYPE_CHECKING:
    from .types import CpfGeneratorOptionsInput


def cpf_gen(
    options: CpfGeneratorOptionsInput = None,
    *,
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    """Helper function to simplify the usage of :class:`CpfGenerator`.

    If no options are provided, it generates an 11-digit unformatted numeric
    CPF (e.g. ``"12345678901"``) using default settings. If options are provided, they control
    ``prefix`` and whether the result is formatted.

    Generates a valid 11-digit CPF (``prefix``, random body, and computed check digits). With default options the result is unformatted numeric; pass ``format=True`` for ``000.000.000-00`` style output.

    Raises:
        ``CpfGeneratorOptionsTypeError``: If any option has an invalid type.
        ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix`` option
            contains an invalid combination of digits.

    See Also:
        :class:`CpfGenerator` for detailed option descriptions.
    """
    return CpfGenerator(
        options,
        format=format,
        prefix=prefix,
    ).generate()


__all__ = ["cpf_gen"]
