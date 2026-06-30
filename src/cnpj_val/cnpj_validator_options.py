"""Options for the CNPJ validator."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from .exceptions import (
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
)

if TYPE_CHECKING:
    from .types import CnpjType, CnpjValidatorOptionsInput, CnpjValidatorOptionsType

CNPJ_LENGTH = 14
"""The standard length of a CNPJ (Cadastro Nacional da Pessoa
Jurídica) identifier (14 alphanumeric characters).
"""


_CNPJ_TYPE_OPTIONS = frozenset({"alphanumeric", "numeric"})
_CNPJ_TYPE_OPTIONS_ORDER = ("alphanumeric", "numeric")


class CnpjValidatorOptions:
    """Class to store the options for the CNPJ validator.

    Provides a centralized way to configure how CNPJs are validated,
    including case sensitivity and the type of format that should be
    considered valid (``"numeric"`` or ``"alphanumeric"``).
    """

    DEFAULT_CASE_SENSITIVE = True
    """Default value for the ``case_sensitive`` option.

    When ``False`` and alphanumeric CNPJ is being validated, lowercase
    characters are also considered valid. Example: for a valid CNPJ
    ``AB.123.CDE/FGHI-45``, if ``case_sensitive`` is ``False``,
    ``ab.123.cde/fghi-45`` is also considered valid.
    """

    DEFAULT_TYPE: CnpjType = "alphanumeric"
    """Default type of characters to validate for the CNPJ."""

    def __init__(
        self,
        options: CnpjValidatorOptionsInput = None,
        *extra_overrides: CnpjValidatorOptionsInput,
        case_sensitive: bool | None = None,
        type: CnpjType | None = None,
    ) -> None:
        """Create a new :class:`CnpjValidatorOptions` instance.

        Options can be provided in multiple ways:

        1. As a single options mapping or another
           :class:`CnpjValidatorOptions` instance.
        2. As multiple override objects that are merged in order (later
           overrides take precedence).

        All options are optional and will default to their predefined values
        if not provided.

        Raises:
            ``CnpjValidatorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        self._options: dict[str, Any] = {}

        self.case_sensitive = case_sensitive
        self.type = type

        to_merge: list[CnpjValidatorOptionsInput] = []

        if options is not None:
            to_merge.append(options)

        to_merge.extend(extra_overrides)

        for item in to_merge:
            self.set(item)

    @property
    def all(self) -> CnpjValidatorOptionsType:
        """Return a shallow copy of all current options.

        The snapshot is immutable. This is useful for creating immutable
        snapshots of the current configuration.
        """
        snapshot: CnpjValidatorOptionsType = {
            "case_sensitive": self._options["case_sensitive"],
            "type": self._options["type"],
        }

        return MappingProxyType(snapshot)  # type: ignore[return-value]

    @property
    def case_sensitive(self) -> bool:
        """Return whether the CNPJ is validated case-sensitively."""
        return self._options["case_sensitive"]

    @case_sensitive.setter
    def case_sensitive(self, value: object | None) -> None:
        """Set whether the CNPJ is validated case-sensitively."""
        actual_case_sensitive = (
            CnpjValidatorOptions.DEFAULT_CASE_SENSITIVE
            if value is None
            else bool(value)
        )

        self._options["case_sensitive"] = actual_case_sensitive

    @property
    def type(self) -> CnpjType:
        """Return the type of characters to validate for the CNPJ."""
        return self._options["type"]

    @type.setter
    def type(self, value: object | None) -> None:
        """Set the type of characters to validate for the CNPJ.

        The options are:

        - ``"alphanumeric"``: alphanumeric CNPJ format.
        - ``"numeric"``: numeric-only (legacy) CNPJ format.

        Raises:
            ``CnpjValidatorOptionsTypeError``: If the value is not a string.
            ``CnpjValidatorOptionTypeInvalidException``: If the value is not a
                valid type.
        """
        actual_type = CnpjValidatorOptions.DEFAULT_TYPE if value is None else value

        if not isinstance(actual_type, str):
            raise CnpjValidatorOptionsTypeError("type", actual_type, "string")

        if actual_type not in _CNPJ_TYPE_OPTIONS:
            raise CnpjValidatorOptionTypeInvalidException(
                actual_type,
                _CNPJ_TYPE_OPTIONS_ORDER,
            )

        self._options["type"] = actual_type

    def set(self, options: CnpjValidatorOptionsInput) -> CnpjValidatorOptions:
        """Set multiple options at once.

        Only the provided options are updated; options not included in
        the object retain their current values. You can pass either a
        partial options mapping or another
        :class:`CnpjValidatorOptions` instance.

        Raises:
            CnpjValidatorOptionsTypeError: If any option has an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        if options is None:
            return self

        if isinstance(options, CnpjValidatorOptions):
            source_case_sensitive = options.case_sensitive
            source_type = options.type
        else:
            source_case_sensitive = options.get("case_sensitive")
            source_type = options.get("type")

        if source_case_sensitive is not None:
            self.case_sensitive = source_case_sensitive
        if source_type is not None:
            self.type = source_type

        return self


__all__ = [
    "CNPJ_LENGTH",
    "CnpjValidatorOptions",
]
