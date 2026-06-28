"""Options for the CNPJ formatter."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .exceptions import (
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjFormatterOptionsTypeError,
)

if TYPE_CHECKING:
    from .types import (
        CnpjFormatterOptionsInput,
        CnpjFormatterOptionsType,
        OnFailCallback,
    )

CNPJ_LENGTH = 14
"""The standard length of a CNPJ (Cadastro Nacional da Pessoa
Jurídica) identifier (14 alphanumeric characters).
"""

MIN_HIDDEN_RANGE = 0
"""Minimum valid index for the hidden range (inclusive).

Must be between 0 and ``CNPJ_LENGTH - 1``.
"""

MAX_HIDDEN_RANGE = CNPJ_LENGTH - 1
"""Maximum valid index for the hidden range (inclusive).

Must be between 0 and ``CNPJ_LENGTH - 1``.
"""

_default_on_fail_callback: OnFailCallback | None = None


def get_default_on_fail() -> OnFailCallback:
    """Return the shared default ``on_fail`` callback.

    Returns an empty string by default. The callback is created lazily
    on first use.
    """
    global _default_on_fail_callback

    if _default_on_fail_callback is None:

        def DEFAULT_ON_FAIL(_value: Any, _exception: Any = None) -> str:
            return ""

        _default_on_fail_callback = DEFAULT_ON_FAIL

    return _default_on_fail_callback


class CnpjFormatterOptions:
    """Stores configuration for the CNPJ formatter.

    Provides a centralized way to configure how CNPJ numbers are
    formatted, including delimiters, hidden character ranges, HTML
    escaping, URL encoding, and error handling callbacks.
    """

    CNPJ_LENGTH = CNPJ_LENGTH
    """The standard length of a CNPJ identifier (14 alphanumeric
    characters).
    """

    DEFAULT_HIDDEN = False
    """Default value for the ``hidden`` option.

    When ``False``, all CNPJ characters are displayed.
    """

    DEFAULT_HIDDEN_KEY = "*"
    """Default string used to replace hidden CNPJ characters."""

    DEFAULT_HIDDEN_START = 5
    """Default start index (inclusive) for hiding CNPJ characters.

    Characters from this index onwards will be replaced with the
    ``hidden_key`` value.
    """

    DEFAULT_HIDDEN_END = 13
    """Default end index (inclusive) for hiding CNPJ characters.

    Characters up to and including this index will be replaced with the
    ``hidden_key`` value.
    """

    DEFAULT_DOT_KEY = "."
    """Default string used as the dot delimiter in formatted CNPJ.

    Used to separate the first groups of characters (``XX.XXX.XXX``).
    """

    DEFAULT_SLASH_KEY = "/"
    """Default string used as the slash delimiter in formatted CNPJ.

    Used to separate the first group of characters from the branch
    identifier (``XXXXXXXX/XXXX``).
    """

    DEFAULT_DASH_KEY = "-"
    """Default string used as the dash delimiter in formatted CNPJ.

    Used to separate the branch identifier from the check digits at the
    end (``XXXX-XX``).
    """

    DEFAULT_ESCAPE = False
    """Default value for the ``escape`` option.

    When ``False``, HTML special characters are not escaped.
    """

    DEFAULT_ENCODE = False
    """Default value for the ``encode`` option.

    When ``False``, the CNPJ string is not URL-encoded.
    """

    DEFAULT_ON_FAIL = get_default_on_fail()
    """Default callback function executed when formatting fails.

    Returns an empty string by default.
    """

    DISALLOWED_KEY_CHARACTERS = ("\u00e5", "\u00eb", "\u00ef", "\u00f6")
    """Characters not allowed in key options (``hidden_key``, ``dot_key``,
    ``slash_key``, ``dash_key``).

    They are reserved for internal formatting logic. For now, the first
    character is only used to replace the hidden key placeholder in
    :class:`~cnpj_fmt.cnpj_formatter.CnpjFormatter`. However, this set
    of characters is reserved for future use already.
    """

    def __init__(
        self,
        options: CnpjFormatterOptionsInput = None,
        *extra_overrides: CnpjFormatterOptionsInput,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: OnFailCallback | None = None,
    ) -> None:
        """Create a new options instance.

        Options can be provided in multiple ways:

        1. As a single options mapping or another
           :class:`CnpjFormatterOptions` instance.
        2. As multiple override objects that are merged in order (later
           overrides take precedence).

        All options are optional and will default to their predefined
        values if not provided. The ``hidden_start`` and ``hidden_end``
        options are validated to ensure they are within the valid range
        ``[0, CNPJ_LENGTH - 1]`` and will be swapped if
        ``hidden_start > hidden_end``.

        Raises:
            CnpjFormatterOptionsTypeError: If any option has an invalid
                type.
            CnpjFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        self._options: CnpjFormatterOptionsType = {}  # type: ignore[typeddict-item]

        self.hidden = hidden
        self.hidden_key = hidden_key
        self.dot_key = dot_key
        self.slash_key = slash_key
        self.dash_key = dash_key
        self.escape = escape
        self.encode = encode
        self.on_fail = on_fail
        self.set_hidden_range(hidden_start, hidden_end)

        to_merge: list[CnpjFormatterOptionsInput] = []

        if options is not None:
            to_merge.append(options)

        to_merge.extend(extra_overrides)

        for item in to_merge:
            self.set(item)

    @property
    def all(self) -> CnpjFormatterOptionsType:
        """Return a shallow copy of all current options.

        This is useful for creating snapshots of the current
        configuration.
        """
        return {**self._options}

    @property
    def hidden(self) -> bool:
        """Return whether hidden character replacement is enabled.

        When ``True``, characters within the ``hidden_start`` to
        ``hidden_end`` range will be replaced with the ``hidden_key``
        character.
        """
        return self._options["hidden"]

    @hidden.setter
    def hidden(self, value: bool | None) -> None:
        """Set whether hidden character replacement is enabled.

        When set to ``True``, characters within the ``hidden_start`` to
        ``hidden_end`` range will be replaced with the ``hidden_key``
        character. The value is converted to a boolean, so truthy/falsy
        values are handled appropriately.
        """
        actual_hidden = self.DEFAULT_HIDDEN if value is None else bool(value)
        self._options["hidden"] = actual_hidden

    @property
    def hidden_key(self) -> str:
        """Return the string used to replace hidden CNPJ characters.

        This string is used when ``hidden`` is ``True`` to mask
        characters in the range from ``hidden_start`` to ``hidden_end``
        (inclusive).
        """
        return self._options["hidden_key"]

    @hidden_key.setter
    def hidden_key(self, value: str | None) -> None:
        """Set the string used to replace hidden CNPJ characters.

        This string is used when ``hidden`` is ``True`` to mask
        characters in the range from ``hidden_start`` to ``hidden_end``
        (inclusive).

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not a
                ``str``.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If the
                value contains any disallowed key character.
        """
        actual_hidden_key = self.DEFAULT_HIDDEN_KEY if value is None else value

        if not isinstance(actual_hidden_key, str):
            raise CnpjFormatterOptionsTypeError(
                "hidden_key", actual_hidden_key, "string"
            )

        self._assert_no_disallowed_key_characters("hidden_key", actual_hidden_key)
        self._options["hidden_key"] = actual_hidden_key

    @property
    def hidden_start(self) -> int:
        """Return the start index (inclusive) for hiding CNPJ characters.

        This is the first position in the CNPJ string where characters
        will be replaced with the ``hidden_key`` string when ``hidden``
        is ``True``. Must be between ``0`` and ``13``
        (``CNPJ_LENGTH - 1``).
        """
        return self._options["hidden_start"]

    @hidden_start.setter
    def hidden_start(self, value: int | None) -> None:
        """Set the start index (inclusive) for hiding CNPJ characters.

        This is the first position in the CNPJ string where characters
        will be replaced with the ``hidden_key`` when ``hidden`` is
        ``True``. The value is validated and will be swapped with
        ``hidden_end`` if necessary to ensure
        ``hidden_start <= hidden_end``.

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not an
                ``int``.
            CnpjFormatterOptionsHiddenRangeInvalidException: If the
                value is out of valid range ``[0, CNPJ_LENGTH - 1]``.
        """
        self.set_hidden_range(value, self._options["hidden_end"])

    @property
    def hidden_end(self) -> int:
        """Return the end index (inclusive) for hiding CNPJ characters.

        This is the last position in the CNPJ string where characters
        will be replaced with the ``hidden_key`` string when ``hidden``
        is ``True``. Must be between ``0`` and ``13``
        (``CNPJ_LENGTH - 1``).
        """
        return self._options["hidden_end"]

    @hidden_end.setter
    def hidden_end(self, value: int | None) -> None:
        """Set the end index (inclusive) for hiding CNPJ characters.

        This is the last position in the CNPJ string where characters
        will be replaced with the ``hidden_key`` when ``hidden`` is
        ``True``. The value is validated and will be swapped with
        ``hidden_start`` if necessary to ensure
        ``hidden_start <= hidden_end``.

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not an
                ``int``.
            CnpjFormatterOptionsHiddenRangeInvalidException: If the
                value is out of valid range ``[0, CNPJ_LENGTH - 1]``.
        """
        self.set_hidden_range(self._options["hidden_start"], value)

    @property
    def dot_key(self) -> str:
        """Return the string used as the dot delimiter.

        This string is used to separate the first groups of characters
        in the formatted CNPJ (e.g., ``"."`` in ``"12.345.678/0001-90"``).
        """
        return self._options["dot_key"]

    @dot_key.setter
    def dot_key(self, value: str | None) -> None:
        """Set the string used as the dot delimiter.

        This string is used to separate the first groups of characters
        in the formatted CNPJ (e.g., ``"."`` in
        ``"12.345.678/0001-90"``).

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not a
                ``str``.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If the
                value contains any disallowed key character.
        """
        actual_dot_key = self.DEFAULT_DOT_KEY if value is None else value

        if not isinstance(actual_dot_key, str):
            raise CnpjFormatterOptionsTypeError("dot_key", actual_dot_key, "string")

        self._assert_no_disallowed_key_characters("dot_key", actual_dot_key)
        self._options["dot_key"] = actual_dot_key

    @property
    def slash_key(self) -> str:
        """Return the string used as the slash delimiter.

        This string is used to separate the first group of characters
        from the branch identifier in the formatted CNPJ (e.g.,
        ``"/"`` in ``"12.345.678/0001-90"``).
        """
        return self._options["slash_key"]

    @slash_key.setter
    def slash_key(self, value: str | None) -> None:
        """Set the string used as the slash delimiter.

        This string is used to separate the first group of characters
        from the branch identifier in the formatted CNPJ (e.g.,
        ``"/"`` in ``"12.345.678/0001-90"``).

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not a
                ``str``.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If the
                value contains any disallowed key character.
        """
        actual_slash_key = self.DEFAULT_SLASH_KEY if value is None else value

        if not isinstance(actual_slash_key, str):
            raise CnpjFormatterOptionsTypeError("slash_key", actual_slash_key, "string")

        self._assert_no_disallowed_key_characters("slash_key", actual_slash_key)
        self._options["slash_key"] = actual_slash_key

    @property
    def dash_key(self) -> str:
        """Return the string used as the dash delimiter.

        This string is used to separate the check digits at the end in
        the formatted CNPJ (e.g., ``"-"`` in ``"12.345.678/0001-90"``).
        """
        return self._options["dash_key"]

    @dash_key.setter
    def dash_key(self, value: str | None) -> None:
        """Set the string used as the dash delimiter.

        This string is used to separate the check digits at the end in
        the formatted CNPJ (e.g., ``"-"`` in ``"12.345.678/0001-90"``).

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not a
                ``str``.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If the
                value contains any disallowed key character.
        """
        actual_dash_key = self.DEFAULT_DASH_KEY if value is None else value

        if not isinstance(actual_dash_key, str):
            raise CnpjFormatterOptionsTypeError("dash_key", actual_dash_key, "string")

        self._assert_no_disallowed_key_characters("dash_key", actual_dash_key)
        self._options["dash_key"] = actual_dash_key

    @property
    def escape(self) -> bool:
        """Return whether HTML escaping is enabled.

        When ``True``, HTML special characters (like ``<``, ``>``,
        ``&``, etc.) in the formatted CNPJ string will be escaped. This
        is useful when using custom delimiters that may contain HTML
        characters or when displaying CNPJ in HTML.
        """
        return self._options["escape"]

    @escape.setter
    def escape(self, value: bool | None) -> None:
        """Set whether HTML escaping is enabled.

        When set to ``True``, HTML special characters (like ``<``,
        ``>``, ``&``, etc.) in the formatted CNPJ string will be
        escaped. This is useful when using custom delimiters that may
        contain HTML characters or when displaying CNPJ in HTML. The
        value is converted to a boolean, so truthy/falsy values are
        handled appropriately.
        """
        actual_escape = self.DEFAULT_ESCAPE if value is None else bool(value)
        self._options["escape"] = actual_escape

    @property
    def encode(self) -> bool:
        """Return whether URL encoding is enabled.

        When ``True``, the formatted CNPJ string will be URL-encoded,
        making it safe to use in URL query parameters or path segments.
        """
        return self._options["encode"]

    @encode.setter
    def encode(self, value: bool | None) -> None:
        """Set whether URL encoding is enabled.

        When set to ``True``, the formatted CNPJ string will be
        URL-encoded, making it safe to use in URL query parameters or
        path segments. The value is converted to a boolean, so
        truthy/falsy values are handled appropriately.
        """
        actual_encode = self.DEFAULT_ENCODE if value is None else bool(value)
        self._options["encode"] = actual_encode

    @property
    def on_fail(self) -> OnFailCallback:
        """Return the callback executed when formatting fails.

        This function is called when the formatter encounters an error
        (e.g., invalid input length). It receives the input value and an
        exception object, and should return a string to use as the
        fallback output.
        """
        return self._options["on_fail"]

    @on_fail.setter
    def on_fail(self, value: OnFailCallback | None) -> None:
        """Set the callback executed when formatting fails.

        This function is called when the formatter encounters an error
        (e.g., invalid input length). It receives the input value and an
        exception object, and should return a string to use as the
        fallback output.

        Raises:
            CnpjFormatterOptionsTypeError: If the value is not
                callable.
        """
        actual_on_fail = get_default_on_fail() if value is None else value

        if not callable(actual_on_fail):
            raise CnpjFormatterOptionsTypeError("on_fail", value, "function")

        self._options["on_fail"] = actual_on_fail

    def set_hidden_range(
        self,
        hidden_start: int | None,
        hidden_end: int | None,
    ) -> CnpjFormatterOptions:
        """Set ``hidden_start`` and ``hidden_end`` with validation.

        Validates that both indices are integers within the valid range
        ``[0, CNPJ_LENGTH - 1]``. If ``hidden_start > hidden_end``,
        the values are automatically swapped to ensure a valid range.
        This method is used internally by the ``hidden_start`` and
        ``hidden_end`` setters to maintain consistency.

        Raises:
            CnpjFormatterOptionsTypeError: If either value is not an
                ``int``.
            CnpjFormatterOptionsHiddenRangeInvalidException: If either
                value is out of valid range ``[0, CNPJ_LENGTH - 1]``.
        """
        actual_hidden_start = (
            self.DEFAULT_HIDDEN_START if hidden_start is None else hidden_start
        )
        actual_hidden_end = (
            self.DEFAULT_HIDDEN_END if hidden_end is None else hidden_end
        )

        if not self._is_valid_integer(actual_hidden_start):
            raise CnpjFormatterOptionsTypeError(
                "hidden_start", actual_hidden_start, "integer"
            )

        if not self._is_valid_integer(actual_hidden_end):
            raise CnpjFormatterOptionsTypeError(
                "hidden_end", actual_hidden_end, "integer"
            )

        if (
            actual_hidden_start < MIN_HIDDEN_RANGE
            or actual_hidden_start > MAX_HIDDEN_RANGE
        ):
            raise CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_start",
                actual_hidden_start,
                MIN_HIDDEN_RANGE,
                MAX_HIDDEN_RANGE,
            )

        if actual_hidden_end < MIN_HIDDEN_RANGE or actual_hidden_end > MAX_HIDDEN_RANGE:
            raise CnpjFormatterOptionsHiddenRangeInvalidException(
                "hidden_end",
                actual_hidden_end,
                MIN_HIDDEN_RANGE,
                MAX_HIDDEN_RANGE,
            )

        if actual_hidden_start > actual_hidden_end:
            actual_hidden_start, actual_hidden_end = (
                actual_hidden_end,
                actual_hidden_start,
            )

        self._options["hidden_start"] = actual_hidden_start
        self._options["hidden_end"] = actual_hidden_end

        return self

    def copy(self) -> CnpjFormatterOptions:
        """Return a shallow copy of this options instance."""
        duplicate = object.__new__(type(self))

        object.__setattr__(duplicate, "_options", self._options.copy())

        return duplicate

    def set(self, options: CnpjFormatterOptionsInput) -> CnpjFormatterOptions:
        """Set multiple options at once.

        Only the provided options are updated; options not included in
        the object retain their current values. You can pass either a
        partial options mapping or another :class:`CnpjFormatterOptions`
        instance.

        Raises:
            CnpjFormatterOptionsTypeError: If any option has an invalid
                type.
            CnpjFormatterOptionsHiddenRangeInvalidException: If
                ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            CnpjFormatterOptionsForbiddenKeyCharacterException: If any
                key option contains a disallowed character.
        """
        if options is None:
            return self

        if isinstance(options, CnpjFormatterOptions):
            source = options.all
        elif isinstance(options, Mapping):
            source = options
        else:
            return self

        def coalesce(key: str, current: Any) -> Any:
            if key not in source:
                return current

            value = source[key]

            return current if value is None else value

        self.hidden = coalesce("hidden", self.hidden)
        self.hidden_key = coalesce("hidden_key", self.hidden_key)
        self.dot_key = coalesce("dot_key", self.dot_key)
        self.slash_key = coalesce("slash_key", self.slash_key)
        self.dash_key = coalesce("dash_key", self.dash_key)
        self.escape = coalesce("escape", self.escape)
        self.encode = coalesce("encode", self.encode)
        self.on_fail = coalesce("on_fail", self.on_fail)
        self.set_hidden_range(
            coalesce("hidden_start", self.hidden_start),
            coalesce("hidden_end", self.hidden_end),
        )

        return self

    @staticmethod
    def _is_valid_integer(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def _assert_no_disallowed_key_characters(
        self, option_name: str, value: str
    ) -> None:
        """Raise if ``value`` contains any disallowed key character.

        Raises:
            CnpjFormatterOptionsForbiddenKeyCharacterException: If
                ``value`` contains any character from
                ``DISALLOWED_KEY_CHARACTERS``.
        """
        forbidden_chars = self.DISALLOWED_KEY_CHARACTERS

        if any(character in value for character in forbidden_chars):
            raise CnpjFormatterOptionsForbiddenKeyCharacterException(
                option_name,
                value,
                forbidden_chars,
            )


__all__ = ["CNPJ_LENGTH", "CnpjFormatterOptions"]
