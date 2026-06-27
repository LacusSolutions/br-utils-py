"""Calculates and exposes CNPJ check digits from a valid base input.

Validates length, base ID, branch ID and rejects repeated-character
sequences.
"""

from .exceptions import (
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
    CnpjInput,
)

CNPJ_MIN_LENGTH = 12
"""Minimum number of characters required for the CNPJ check digits
calculation.
"""

CNPJ_MAX_LENGTH = 14
"""Maximum number of characters accepted as input for the CNPJ check
digits calculation.
"""

_CNPJ_BASE_ID_LENGTH = 8
_CNPJ_INVALID_BASE_ID = "0" * _CNPJ_BASE_ID_LENGTH
_CNPJ_BRANCH_ID_LENGTH = 4
_CNPJ_INVALID_BRANCH_ID = "0" * _CNPJ_BRANCH_ID_LENGTH

_DELTA_FACTOR = ord("0")
_WEIGHTS = (2, 3, 4, 5, 6, 7, 8, 9)
_DIGIT_CHARS = "0123456789"


class CnpjCheckDigits:
    """Calculates and exposes CNPJ check digits from a valid base input.

    Validates length, base ID, branch ID and rejects repeated-character
    sequences.
    """

    def __init__(self, cnpj_input: CnpjInput) -> None:
        """Create a calculator for the given CNPJ base (12 to 14 chars).

        Args:
            cnpj_input: Alphanumeric CNPJ with or without formatting, or
                a list of strings.

        Raises:
            CnpjCheckDigitsInputTypeError: When input is not a ``str`` or
                ``list[str]``.
            CnpjCheckDigitsInputLengthException: When character count is
                not between 12 and 14.
            CnpjCheckDigitsInputInvalidException: When base ID is all zero
                (``00.000.000``), branch ID is all zero (``0000``) or all
                digits are numeric the same (repeated digits, e.g.
                ``77.777.777/7777-...``).
        """
        parsed_input = self._parse_input(cnpj_input)

        self._validate_length(parsed_input, cnpj_input)
        self._validate_base_id(parsed_input, cnpj_input)
        self._validate_branch_id(parsed_input, cnpj_input)
        self._validate_non_repeated_digits(parsed_input, cnpj_input)

        self._cnpj_chars: tuple[str, ...] = tuple(parsed_input[:CNPJ_MIN_LENGTH])
        self._cached_first_digit: int | None = None
        self._cached_second_digit: int | None = None

    @property
    def first(self) -> str:
        """First check digit (13th character of the full CNPJ)."""
        if self._cached_first_digit is None:
            self._cached_first_digit = self._calculate(self._cnpj_chars)

        return _DIGIT_CHARS[self._cached_first_digit]

    @property
    def second(self) -> str:
        """Second check digit (14th character of the full CNPJ)."""
        if self._cached_second_digit is None:
            self._cached_second_digit = self._calculate((*self._cnpj_chars, self.first))

        return _DIGIT_CHARS[self._cached_second_digit]

    @property
    def both(self) -> str:
        """Both check digits concatenated (13th and 14th characters)."""
        return self.first + self.second

    @property
    def cnpj(self) -> str:
        """Full 14-character CNPJ (base 12 characters concatenated with
        the 2 check digits).
        """
        return "".join(self._cnpj_chars) + self.both

    def _parse_input(self, cnpj_input: object) -> list[str]:
        """Parse a string or list of strings into alphanumeric characters.

        Raises:
            CnpjCheckDigitsInputTypeError: When input is not a ``str`` or
                ``list[str]``.
        """
        if isinstance(cnpj_input, str):
            return self._parse_string_input(cnpj_input)

        if isinstance(cnpj_input, list):
            return self._parse_list_input(cnpj_input)

        raise CnpjCheckDigitsInputTypeError(cnpj_input, "string or string[]")

    def _parse_string_input(self, cnpj_string: str) -> list[str]:
        """Strip non-alphanumeric characters and uppercase the remainder."""
        result: list[str] = []
        append = result.append

        for char in cnpj_string:
            code = ord(char)
            if 48 <= code <= 57 or 65 <= code <= 90:
                append(char)
            elif 97 <= code <= 122:
                append(chr(code - 32))

        return result

    def _parse_list_input(self, cnpj_list: list[object]) -> list[str]:
        """Concatenate a list of strings and normalize the result.

        Raises:
            CnpjCheckDigitsInputTypeError: When input is not a ``str`` or
                ``list[str]``.
        """
        if not cnpj_list:
            return []

        is_string_list = all(isinstance(item, str) for item in cnpj_list)

        if not is_string_list:
            raise CnpjCheckDigitsInputTypeError(cnpj_list, "string or string[]")

        return self._parse_string_input("".join(cnpj_list))

    def _validate_length(
        self, cnpj_chars: list[str], original_input: CnpjInput
    ) -> None:
        """Ensure character count is between ``CNPJ_MIN_LENGTH`` and
        ``CNPJ_MAX_LENGTH``.

        Raises:
            CnpjCheckDigitsInputLengthException: When character count is
                not between 12 and 14.
        """
        chars_count = len(cnpj_chars)

        if chars_count < CNPJ_MIN_LENGTH or chars_count > CNPJ_MAX_LENGTH:
            raise CnpjCheckDigitsInputLengthException(
                original_input,
                "".join(cnpj_chars),
                CNPJ_MIN_LENGTH,
                CNPJ_MAX_LENGTH,
            )

    def _validate_base_id(
        self, cnpj_chars: list[str], original_input: CnpjInput
    ) -> None:
        """Reject base ID (first 8 digits) when it is all zeros.

        Raises:
            CnpjCheckDigitsInputInvalidException: When base ID is all
                zeros (``00.000.000``).
        """
        if all(char == "0" for char in cnpj_chars[:_CNPJ_BASE_ID_LENGTH]):
            raise CnpjCheckDigitsInputInvalidException(
                original_input,
                f'Base ID "{_CNPJ_INVALID_BASE_ID}" is not eligible.',
            )

    def _validate_branch_id(
        self, cnpj_chars: list[str], original_input: CnpjInput
    ) -> None:
        """Reject branch ID (digits 9-12) when it is all zeros.

        Raises:
            CnpjCheckDigitsInputInvalidException: When branch ID is all
                zeros (``0000``).
        """
        branch_start = _CNPJ_BASE_ID_LENGTH
        branch_end = branch_start + _CNPJ_BRANCH_ID_LENGTH

        if all(char == "0" for char in cnpj_chars[branch_start:branch_end]):
            raise CnpjCheckDigitsInputInvalidException(
                original_input,
                f'Branch ID "{_CNPJ_INVALID_BRANCH_ID}" is not eligible.',
            )

    def _validate_non_repeated_digits(
        self, cnpj_chars: list[str], original_input: CnpjInput
    ) -> None:
        """Reject inputs where all first 12 characters are the same.

        Raises:
            CnpjCheckDigitsInputInvalidException: When all digits are
                numeric the same (repeated digits, e.g.
                ``77.777.777/7777-...``).
        """
        first_char = cnpj_chars[0]

        if first_char.isdigit() and all(
            char == first_char for char in cnpj_chars[1:CNPJ_MIN_LENGTH]
        ):
            raise CnpjCheckDigitsInputInvalidException(
                original_input,
                "Repeated digits are not considered valid.",
            )

    def _calculate(self, cnpj_sequence: tuple[str, ...] | list[str]) -> int:
        """Compute a single check digit using the standard CNPJ modulo-11
        algorithm.
        """
        length = len(cnpj_sequence)
        sum_result = 0

        for index in range(length - 1, -1, -1):
            char_value = ord(cnpj_sequence[index]) - _DELTA_FACTOR
            sum_result += char_value * _WEIGHTS[(length - 1 - index) % 8]

        remainder = sum_result % 11

        return 0 if remainder < 2 else 11 - remainder
