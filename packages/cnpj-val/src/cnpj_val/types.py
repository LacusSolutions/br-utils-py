"""Type aliases for the ``cnpj_val`` package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, TypeAlias, TypedDict

CnpjType = Literal["alphanumeric", "numeric"]
"""Character set for CNPJ values (generation or validation).

- ``"alphanumeric"`` (default): digits and letters (``0-9A-Z``)
- ``"numeric"``: digits only (``0-9``)
"""


class CnpjValidatorOptionsType(TypedDict):
    """Resolved CNPJ validator options used internally.

    All properties have defaults when creating a
    :class:`~cnpj_val.cnpj_validator_options.CnpjValidatorOptions`
    instance.

    Attributes:
        ``case_sensitive``: Whether validation is case-sensitive. Example: for
            a valid CNPJ ``AB.123.CDE/FGHI-45``, if ``case_sensitive`` is
            ``False``, ``ab.123.cde/fghi-45`` is also considered valid.
            Defaults to ``True``.
        ``type``: Character set used to determine valid CNPJ characters.
            ``"alphanumeric"`` for alphanumeric CNPJ format; ``"numeric"`` for
            numeric-only (legacy) CNPJ format. Defaults to ``"alphanumeric"``.
    """

    case_sensitive: bool
    type: CnpjType


CnpjInput: TypeAlias = str | Sequence[str]
"""Valid input types for CNPJ validation.

A CNPJ may be given as:

- A string of alphanumeric characters (with or without formatting).
- A sequence of strings, each representing one or more alphanumeric characters.
"""

from .cnpj_validator_options import CnpjValidatorOptions  # noqa: E402

CnpjValidatorOptionsInput: TypeAlias = CnpjValidatorOptions | Mapping[str, Any] | None
"""Options input accepted by constructors and merge helpers.

May be a :class:`~cnpj_val.cnpj_validator_options.CnpjValidatorOptions`
instance, a partial options ``Mapping[str, Any]``, or ``None``.
"""

__all__ = [
    "CnpjInput",
    "CnpjType",
    "CnpjValidatorOptionsInput",
    "CnpjValidatorOptionsType",
]
