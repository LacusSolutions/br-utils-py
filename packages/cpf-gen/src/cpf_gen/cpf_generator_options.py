"""Options for the CPF generator."""

from __future__ import annotations

import re
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from .exceptions import (
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptionsTypeError,
)

if TYPE_CHECKING:
    from .types import CpfGeneratorOptionsInput, CpfGeneratorOptionsType

CPF_LENGTH = 11
"""The standard length of a CPF (Cadastro de Pessoa Física) identifier (11
digits).
"""

CPF_PREFIX_MAX_LENGTH = CPF_LENGTH - 2
"""Maximum length of the ``prefix`` of a CPF."""

_CPF_BASE_ID_LENGTH = 9
_CPF_BASE_ID_LAST_INDEX = _CPF_BASE_ID_LENGTH - 1
_ZEROED_CPF_BASE_ID = "0" * _CPF_BASE_ID_LENGTH

_PREFIX_SANITIZE_PATTERN = re.compile(r"\D")


class CpfGeneratorOptions:
    """Stores configuration for the CPF generator.

    Provides a centralized way to configure how CPF digits are generated,
    including partial start string (``prefix``) and formatting (``format``).
    """

    DEFAULT_FORMAT = False
    """Default value for the ``format`` option.

    When ``True``, the generated CPF string will have the standard formatting
    (``000.000.000-00``).
    """

    DEFAULT_PREFIX = ""
    """Default value for the ``prefix`` option."""

    def __init__(
        self,
        options: CpfGeneratorOptionsInput = None,
        *extra_overrides: CpfGeneratorOptionsInput,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> None:
        """Create a new :class:`CpfGeneratorOptions` instance.

        Options can be provided in multiple ways:

        1. As a single options mapping or another :class:`CpfGeneratorOptions`
           instance.
        2. As multiple override objects that are merged in order (later
           overrides take precedence).

        All options are optional and default to ``DEFAULT_FORMAT`` and
        ``DEFAULT_PREFIX`` if not provided.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If any option has an invalid type
            ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of digits.
        """
        self._options: dict[str, Any] = {}

        if isinstance(options, CpfGeneratorOptions):
            self.format = options.format
            self.prefix = options.prefix
        elif isinstance(options, dict):
            self.format = options.get("format")  # type: ignore[assignment]
            self.prefix = options.get("prefix")  # type: ignore[assignment]
        else:
            self.format = format
            self.prefix = prefix

        for override in extra_overrides:
            self.set(override)

    @property
    def all(self) -> CpfGeneratorOptionsType:
        """Return a shallow copy of all current options, frozen to prevent
        modification.

        Exposes resolved ``format`` and ``prefix`` values. Useful for creating
        immutable snapshots of the current configuration.
        """
        snapshot: CpfGeneratorOptionsType = {
            "format": self._options["format"],
            "prefix": self._options["prefix"],
        }

        return MappingProxyType(snapshot)  # type: ignore[return-value]

    @property
    def format(self) -> bool:
        """Return whether the generated CPF will use standard formatting.

        When ``True``, the result is formatted as ``000.000.000-00``.
        """
        return self._options["format"]

    @format.setter
    def format(self, value: object | None) -> None:
        """Set whether the generated CPF will use standard formatting.

        When ``True``, the result is formatted as ``000.000.000-00``. The value
        is converted to ``bool``, so truthy/falsy values are handled
        appropriately.
        """
        actual_format = (
            CpfGeneratorOptions.DEFAULT_FORMAT if value is None else bool(value)
        )

        self._options["format"] = actual_format

    @property
    def prefix(self) -> str:
        """Return the initial string (``prefix``) of the generated CPF.

        Note: If the evaluated ``prefix`` (after stripping non-digit
        characters) is longer than 9 digits, the extra digits are ignored,
        because a CPF has 9 base digits followed by 2 calculated check digits.
        """
        return self._options["prefix"]

    @prefix.setter
    def prefix(self, value: object | None) -> None:
        """Set the initial string (``prefix``) of the generated CPF.

        Only digits are kept and the rest is stripped. If provided, only the
        missing digits are generated randomly. For example, if the ``prefix``
        ``123456`` (6 digits) is given, only the next 3 digits are randomly
        generated and concatenated to the ``prefix``.

        Note: If the evaluated ``prefix`` (after stripping non-digit
        characters) is longer than 9 digits, the extra digits are ignored,
        because a CPF has 9 base digits followed by 2 calculated check digits.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If the value is not a ``str``.
            ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of digits.
        """
        actual_prefix = CpfGeneratorOptions.DEFAULT_PREFIX if value is None else value

        if not isinstance(actual_prefix, str):
            raise CpfGeneratorOptionsTypeError("prefix", actual_prefix, "string")

        actual_prefix = _PREFIX_SANITIZE_PATTERN.sub("", actual_prefix)
        actual_prefix = actual_prefix[:CPF_PREFIX_MAX_LENGTH]

        self._validate_prefix_base_id(actual_prefix)
        self._validate_prefix_non_repeated_digits(actual_prefix)

        self._options["prefix"] = actual_prefix

    def set(self, options: CpfGeneratorOptionsInput) -> CpfGeneratorOptions:
        """Update multiple options at once, preserving omitted fields.

        Only the provided options are updated; options not included in the
        object retain their current values. You can pass either a partial
        options mapping or another :class:`CpfGeneratorOptions` instance.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If any option has an invalid
            type.
            ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of digits.
        """
        if options is None:
            return self

        if isinstance(options, CpfGeneratorOptions):
            source_format = options.format
            source_prefix = options.prefix
        else:
            source_format = options.get("format")
            source_prefix = options.get("prefix")

        if source_format is not None:
            self.format = source_format
        if source_prefix is not None:
            self.prefix = source_prefix

        return self

    def _validate_prefix_base_id(self, partial_cpf: str) -> None:
        """Raise if the first 9 characters of ``prefix`` are zeros.

        Raises:
            ``CpfGeneratorOptionPrefixInvalidException``: If the first 9
                characters of ``prefix`` are all zeros.
        """
        if len(partial_cpf) < _CPF_BASE_ID_LENGTH:
            return

        cpf_base_id = partial_cpf[: _CPF_BASE_ID_LAST_INDEX + 1]

        if cpf_base_id == _ZEROED_CPF_BASE_ID:
            raise CpfGeneratorOptionPrefixInvalidException(
                partial_cpf,
                "Zeroed base ID is not eligible.",
            )

    def _validate_prefix_non_repeated_digits(self, cpf_prefix: str) -> None:
        """Raise if ``prefix`` has 9 characters that are one digit.

        Raises:
            ``CpfGeneratorOptionPrefixInvalidException``: If ``prefix`` has 9
                characters that are all the same digit.
        """
        if len(cpf_prefix) < CPF_PREFIX_MAX_LENGTH:
            return

        first_character = cpf_prefix[0]

        if cpf_prefix == first_character * CPF_PREFIX_MAX_LENGTH:
            raise CpfGeneratorOptionPrefixInvalidException(
                cpf_prefix,
                "Repeated digits are not considered valid.",
            )


__all__ = [
    "CPF_LENGTH",
    "CPF_PREFIX_MAX_LENGTH",
    "CpfGeneratorOptions",
]
