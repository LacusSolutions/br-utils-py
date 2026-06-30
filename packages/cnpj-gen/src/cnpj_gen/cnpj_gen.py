"""Convenience wrapper around
:class:`~cnpj_gen.cnpj_generator.CnpjGenerator`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cnpj_generator import CnpjGenerator

if TYPE_CHECKING:
    from .types import CnpjGeneratorOptionsInput, CnpjType


def cnpj_gen(
    options: CnpjGeneratorOptionsInput | None = None,
    *,
    format: bool | None = None,
    prefix: str | None = None,
    type: CnpjType | None = None,
) -> str:
    """Helper function to simplify the usage of :class:`CnpjGenerator`.

    If no options are provided, it generates a 14-character unformatted
    alphanumeric CNPJ (e.g. ``"AB123CDE000155"``) using default settings.
    If options are provided, they control ``prefix``, ``type``, and
    whether the result is formatted.

    Generates a valid 14-character CNPJ (``prefix``, random body for the
    chosen :data:`~cnpj_gen.types.CnpjType`, and computed check digits).
    With default options the result is unformatted alphanumeric; pass
    ``format=True`` for ``00.000.000/0000-00`` style output.

    Raises:
        ``CnpjGeneratorOptionsTypeError``: If any option has an invalid type.
        ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix`` option
            contains an invalid combination of characters.
        ``CnpjGeneratorOptionTypeInvalidException``: If the ``type`` option is
            not one of the allowed values.

    See Also:
        :class:`CnpjGenerator` for detailed option descriptions.
    """
    return CnpjGenerator(
        options,
        format=format,
        prefix=prefix,
        type=type,
    ).generate()


__all__ = ["cnpj_gen"]
