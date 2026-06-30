"""Helper function for CNPJ validation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cnpj_validator import CnpjValidator

if TYPE_CHECKING:
    from .types import CnpjInput, CnpjType, CnpjValidatorOptionsInput


def cnpj_val(
    cnpj_input: CnpjInput,
    options: CnpjValidatorOptionsInput = None,
    *,
    case_sensitive: bool | None = None,
    type: CnpjType | None = None,
) -> bool:
    """Helper function to simplify the usage of :class:`CnpjValidator`.

    If no options are provided, it validates a CNPJ string or sequence of
    strings using default settings. If options are provided, they control case
    sensitivity and the type of characters to be validated.

    Raises:
        ``CnpjValidatorInputTypeError``: If the input is not a string or
            sequence of strings.
        ``CnpjValidatorOptionsTypeError``: If any option has an invalid type.
        ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option is
            not one of the allowed values.

    See Also:
        :class:`CnpjValidator` for detailed option descriptions.
    """
    return CnpjValidator(
        options,
        case_sensitive=case_sensitive,
        type=type,
    ).is_valid(cnpj_input)


__all__ = ["cnpj_val"]
