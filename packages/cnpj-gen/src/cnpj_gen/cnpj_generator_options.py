"""Options for the CNPJ generator."""

from __future__ import annotations

import re
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from .exceptions import (
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
)

if TYPE_CHECKING:
    from .types import CnpjGeneratorOptionsInput, CnpjGeneratorOptionsType, CnpjType

CNPJ_LENGTH = 14
"""The standard length of a CNPJ (Cadastro Nacional da Pessoa
Jurídica) identifier (14 alphanumeric characters).
"""

CNPJ_PREFIX_MAX_LENGTH = CNPJ_LENGTH - 2
"""Maximum length of the ``prefix`` (base ID and branch ID) of a CNPJ.
"""

_CNPJ_BASE_ID_LENGTH = 8
_CNPJ_BASE_ID_LAST_INDEX = _CNPJ_BASE_ID_LENGTH - 1
_ZEROED_CNPJ_BASE_ID = "0" * _CNPJ_BASE_ID_LENGTH

_CNPJ_BRANCH_ID_LENGTH = 4
_CNPJ_BRANCH_ID_LAST_INDEX = _CNPJ_BASE_ID_LAST_INDEX + _CNPJ_BRANCH_ID_LENGTH
_ZEROED_CNPJ_BRANCH_ID = "0" * _CNPJ_BRANCH_ID_LENGTH

_CNPJ_TYPE_OPTIONS = frozenset({"alphabetic", "alphanumeric", "numeric"})
_CNPJ_TYPE_OPTIONS_ORDER = ("alphabetic", "alphanumeric", "numeric")

_PREFIX_SANITIZE_PATTERN = re.compile(r"[^0-9A-Za-z]")


class CnpjGeneratorOptions:
    """Stores configuration for the CNPJ generator.

    Provides a centralized way to configure how CNPJ characters are
    generated, including partial start string (``prefix``), formatting
    (``format``), and the type of characters to be generated
    (``"numeric"``, ``"alphabetic"``, or ``"alphanumeric"``).
    """

    DEFAULT_FORMAT = False
    """Default value for the ``format`` option.

    When ``True``, the generated CNPJ string will have the standard
    formatting (``00.000.000/0000-00``).
    """

    DEFAULT_PREFIX = ""
    """Default value for the ``prefix`` option."""

    DEFAULT_TYPE = "alphanumeric"
    """Default value for the ``type`` option."""

    def __init__(
        self,
        options: CnpjGeneratorOptionsInput = None,
        *extra_overrides: CnpjGeneratorOptionsInput,
        format: bool | None = None,
        prefix: str | None = None,
        type: CnpjType | None = None,
    ) -> None:
        """Create a new :class:`CnpjGeneratorOptions` instance.

        Options can be provided in multiple ways:

        1. As a single options mapping or another
           :class:`CnpjGeneratorOptions` instance.
        2. As multiple override objects that are merged in order (later
           overrides take precedence).

        All options are optional and default to ``DEFAULT_FORMAT``,
        ``DEFAULT_PREFIX``, and ``DEFAULT_TYPE`` if not provided.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of characters.
            ``CnpjGeneratorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        self._options: dict[str, Any] = {}

        if isinstance(options, CnpjGeneratorOptions):
            self.format = options.format
            self.prefix = options.prefix
            self.type = options.type
        elif isinstance(options, dict):
            self.format = options.get("format")  # type: ignore[assignment]
            self.prefix = options.get("prefix")  # type: ignore[assignment]
            self.type = options.get("type")  # type: ignore[assignment]
        else:
            self.format = format
            self.prefix = prefix
            self.type = type

        for override in extra_overrides:
            self.set(override)

    @property
    def all(self) -> CnpjGeneratorOptionsType:
        """Return a shallow, immutable snapshot of the current options.

        Exposes resolved ``format``, ``prefix``, and ``type`` values.
        Useful for creating snapshots of the current configuration.
        """
        snapshot: CnpjGeneratorOptionsType = {
            "format": self._options["format"],
            "prefix": self._options["prefix"],
            "type": self._options["type"],
        }

        return MappingProxyType(snapshot)  # type: ignore[return-value]

    @property
    def format(self) -> bool:
        """Return whether the generated CNPJ will use standard formatting.

        When ``True``, the result is formatted as ``00.000.000/0000-00``.
        """
        return self._options["format"]

    @format.setter
    def format(self, value: object | None) -> None:
        """Set whether the generated CNPJ will use standard formatting.

        When ``True``, the result is formatted as ``00.000.000/0000-00``.
        The value is converted to ``bool``, so truthy/falsy values are handled
        appropriately.
        """
        actual_format = (
            CnpjGeneratorOptions.DEFAULT_FORMAT if value is None else bool(value)
        )

        self._options["format"] = actual_format

    @property
    def prefix(self) -> str:
        """Return the initial string (``prefix``) of the generated CNPJ.

        Note: If the evaluated ``prefix`` (after stripping non-alphanumeric
        characters) is longer than 12 characters, the extra characters are
        ignored, because a CNPJ has 12 base characters followed by 2 calculated
        check digits.
        """
        return self._options["prefix"]

    @prefix.setter
    def prefix(self, value: object | None) -> None:
        """Set the initial string (``prefix``) of the generated CNPJ.

        Only alphanumeric characters are kept and the rest is stripped.
        If provided, only the missing characters are generated randomly.
        For example, if the ``prefix`` ``AAABBB`` (6 characters) is given,
        only the next 8 characters are randomly generated and
        concatenated to the ``prefix``.

        Note: If the evaluated ``prefix`` (after stripping non-alphanumeric
        characters) is longer than 12 characters, the extra characters are
        ignored, because a CNPJ has 12 base characters followed by 2 calculated
        check digits.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If the value is not a ``str``.
            ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of characters.
        """
        actual_prefix = CnpjGeneratorOptions.DEFAULT_PREFIX if value is None else value

        if not isinstance(actual_prefix, str):
            raise CnpjGeneratorOptionsTypeError("prefix", actual_prefix, "string")

        actual_prefix = _PREFIX_SANITIZE_PATTERN.sub("", actual_prefix)
        actual_prefix = actual_prefix.upper()
        actual_prefix = actual_prefix[:CNPJ_PREFIX_MAX_LENGTH]

        self._validate_prefix_base_id(actual_prefix)
        self._validate_prefix_branch_id(actual_prefix)
        self._validate_prefix_non_repeated_digits(actual_prefix)

        self._options["prefix"] = actual_prefix

    @property
    def type(self) -> CnpjType:
        """Return the character ``type`` used for random CNPJ segments."""
        return self._options["type"]

    @type.setter
    def type(self, value: object | None) -> None:
        """Set the character ``type`` used for random CNPJ segments.

        The options are:

        - ``"alphabetic"``: Generates a sequence of alphabetic characters
          (``A-Z``).
        - ``"alphanumeric"``: Generates a sequence of alphanumeric characters
          (``0-9A-Z``).
        - ``"numeric"``: Generates a sequence of numbers-only characters
          (``0-9``).

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If the value is not a ``str``.
            ``CnpjGeneratorOptionTypeInvalidException``: If the value is not a
                valid type.
        """
        actual_type = CnpjGeneratorOptions.DEFAULT_TYPE if value is None else value

        if not isinstance(actual_type, str):
            raise CnpjGeneratorOptionsTypeError("type", actual_type, "str")

        if actual_type not in _CNPJ_TYPE_OPTIONS:
            raise CnpjGeneratorOptionTypeInvalidException(
                actual_type,
                _CNPJ_TYPE_OPTIONS_ORDER,
            )

        self._options["type"] = actual_type

    def set(
        self, options: CnpjGeneratorOptionsInput | None = None
    ) -> CnpjGeneratorOptions:
        """Update multiple options at once, preserving omitted fields.

        Only the provided options are updated; options not included in
        the object retain their current values. You can pass either a
        partial options mapping or another
        :class:`CnpjGeneratorOptions` instance.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of characters.
            ``CnpjGeneratorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        if options is None:
            return self

        if isinstance(options, CnpjGeneratorOptions):
            source_format = options.format
            source_prefix = options.prefix
            source_type = options.type
        else:
            source_format = options.get("format")
            source_prefix = options.get("prefix")
            source_type = options.get("type")

        if source_format is not None:
            self.format = source_format
        if source_prefix is not None:
            self.prefix = source_prefix
        if source_type is not None:
            self.type = source_type

        return self

    def _validate_prefix_base_id(self, partial_cnpj: str) -> None:
        """Raise if the first 8 characters of ``prefix`` are zeros.

        Raises:
            ``CnpjGeneratorOptionPrefixInvalidException``: If the first
                8 characters of ``prefix`` are all zeros.
        """
        if len(partial_cnpj) < _CNPJ_BASE_ID_LENGTH:
            return

        cnpj_base_id = partial_cnpj[: _CNPJ_BASE_ID_LAST_INDEX + 1]

        if cnpj_base_id == _ZEROED_CNPJ_BASE_ID:
            raise CnpjGeneratorOptionPrefixInvalidException(
                partial_cnpj,
                "Zeroed base ID is not eligible.",
            )

    def _validate_prefix_branch_id(self, partial_cnpj: str) -> None:
        """Raise if ``prefix`` characters at positions 9-12 are zeros.

        Raises:
            ``CnpjGeneratorOptionPrefixInvalidException``: If ``prefix``
                characters at positions 9-12 are all zeros.
        """
        if len(partial_cnpj) < _CNPJ_BASE_ID_LENGTH + _CNPJ_BRANCH_ID_LENGTH:
            return

        cnpj_branch_id = partial_cnpj[
            _CNPJ_BASE_ID_LENGTH : _CNPJ_BRANCH_ID_LAST_INDEX + 1
        ]

        if cnpj_branch_id == _ZEROED_CNPJ_BRANCH_ID:
            raise CnpjGeneratorOptionPrefixInvalidException(
                partial_cnpj,
                "Zeroed branch ID is not eligible.",
            )

    def _validate_prefix_non_repeated_digits(self, cnpj_prefix: str) -> None:
        """Raise if ``prefix`` has 12 characters that are one digit.

        Raises:
            ``CnpjGeneratorOptionPrefixInvalidException``: If ``prefix`` has
                12 characters that are all the same digit.
        """
        if len(cnpj_prefix) < CNPJ_PREFIX_MAX_LENGTH:
            return

        first_character = cnpj_prefix[0]

        if (
            first_character.isdigit()
            and cnpj_prefix == first_character * CNPJ_PREFIX_MAX_LENGTH
        ):
            raise CnpjGeneratorOptionPrefixInvalidException(
                cnpj_prefix,
                "Repeated digits are not considered valid.",
            )


__all__ = [
    "CNPJ_LENGTH",
    "CNPJ_PREFIX_MAX_LENGTH",
    "CnpjGeneratorOptions",
]
