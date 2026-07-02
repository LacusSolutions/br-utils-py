"""Calculates and exposes CPF check digits from a valid base input.

Validates length and rejects repeated-digit sequences.
"""

from .exceptions import (
    CpfCheckDigitsInputInvalidException,
    CpfCheckDigitsInputLengthException,
    CpfCheckDigitsInputTypeError,
)
from .types import CpfInput

CPF_MIN_LENGTH = 9
"""Minimum number of digits required for the CPF check digits calculation."""

CPF_MAX_LENGTH = 11
"""Maximum number of digits accepted as input for the CPF check digits
calculation.
"""

_DELTA_FACTOR = ord("0")
_FIRST_WEIGHTS = (10, 9, 8, 7, 6, 5, 4, 3, 2)
_SECOND_WEIGHTS = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
_DIGIT_CHARS = "0123456789"


class CpfCheckDigits:
    """Calculates and exposes CPF check digits from a valid base input.

    Validates length and rejects repeated-digit sequences.
    """

    def __init__(self, cpf_input: CpfInput) -> None:
        """Create a calculator for the given CPF base (9 to 11 digits).

        Args:
            ``cpf_input``: Digits with or without formatting, or a list of
                strings.

        Raises:
            ``CpfCheckDigitsInputTypeError``: When input is not a ``str`` or
                ``list[str]``.
            ``CpfCheckDigitsInputLengthException``: When digit count is not
                between 9 and 11.
            ``CpfCheckDigitsInputInvalidException``: When all digits are the
                same (repeated digits, e.g. ``777.777.777-...``).
        """
        parsed_input = self._parse_input(cpf_input)

        self._validate_length(parsed_input, cpf_input)
        self._validate_non_repeated_digits(parsed_input, cpf_input)

        self._cpf_digits: tuple[str, ...] = tuple(parsed_input[:CPF_MIN_LENGTH])
        self._cached_first_digit: int | None = None
        self._cached_second_digit: int | None = None

    @property
    def first(self) -> str:
        """First check digit (10th digit of the full CPF)."""
        if self._cached_first_digit is None:
            self._cached_first_digit = self._calculate(self._cpf_digits)

        return _DIGIT_CHARS[self._cached_first_digit]

    @property
    def second(self) -> str:
        """Second check digit (11th digit of the full CPF)."""
        if self._cached_second_digit is None:
            self._cached_second_digit = self._calculate((*self._cpf_digits, self.first))

        return _DIGIT_CHARS[self._cached_second_digit]

    @property
    def both(self) -> str:
        """Both check digits concatenated (10th and 11th digits)."""
        return self.first + self.second

    @property
    def cpf(self) -> str:
        """Full 11-digit CPF (base 9 digits concatenated with the 2 check
        digits).
        """
        return "".join(self._cpf_digits) + self.both

    def _parse_input(self, cpf_input: object) -> list[str]:
        """Parse a string or list of strings into digit characters.

        Raises:
            ``CpfCheckDigitsInputTypeError``: When input is not a ``str`` or
                ``list[str]``.
        """
        if isinstance(cpf_input, str):
            return self._parse_string_input(cpf_input)

        if isinstance(cpf_input, list):
            return self._parse_list_input(cpf_input)

        raise CpfCheckDigitsInputTypeError(cpf_input, "string or string[]")

    def _parse_string_input(self, cpf_string: str) -> list[str]:
        """Strip non-digit characters and keep the remainder as characters."""
        result: list[str] = []
        append = result.append

        for char in cpf_string:
            code = ord(char)
            if 48 <= code <= 57:
                append(char)

        return result

    def _parse_list_input(self, cpf_list: list[object]) -> list[str]:
        """Concatenate a list of strings and parse the result.

        Raises:
            ``CpfCheckDigitsInputTypeError``: When input is not a ``str`` or
                ``list[str]``.
        """
        if not cpf_list:
            return []

        is_string_list = all(isinstance(item, str) for item in cpf_list)

        if not is_string_list:
            raise CpfCheckDigitsInputTypeError(cpf_list, "string or string[]")

        return self._parse_string_input("".join(cpf_list))

    def _validate_length(self, cpf_digits: list[str], original_input: CpfInput) -> None:
        """Ensure digit count is between ``CPF_MIN_LENGTH`` and
        ``CPF_MAX_LENGTH``.

        Raises:
            ``CpfCheckDigitsInputLengthException``: When digit count is not
                between 9 and 11.
        """
        digits_count = len(cpf_digits)

        if digits_count < CPF_MIN_LENGTH or digits_count > CPF_MAX_LENGTH:
            raise CpfCheckDigitsInputLengthException(
                original_input,
                "".join(cpf_digits),
                CPF_MIN_LENGTH,
                CPF_MAX_LENGTH,
            )

    def _validate_non_repeated_digits(
        self, cpf_digits: list[str], original_input: CpfInput
    ) -> None:
        """Reject inputs where all first 9 digits are the same.

        Raises:
            ``CpfCheckDigitsInputInvalidException``: When all digits are the
                same (repeated digits, e.g. ``777.777.777-...``).
        """
        first_char = cpf_digits[0]

        if all(char == first_char for char in cpf_digits[1:CPF_MIN_LENGTH]):
            raise CpfCheckDigitsInputInvalidException(
                original_input,
                "Repeated digits are not considered valid.",
            )

    def _calculate(self, cpf_sequence: tuple[str, ...] | list[str]) -> int:
        """Compute a single check digit using the standard CPF modulo-11
        algorithm.
        """
        length = len(cpf_sequence)
        weights = _FIRST_WEIGHTS if length == CPF_MIN_LENGTH else _SECOND_WEIGHTS
        sum_result = 0

        for index in range(length):
            char_value = ord(cpf_sequence[index]) - _DELTA_FACTOR
            sum_result += char_value * weights[index]

        remainder = 11 - (sum_result % 11)

        return 0 if remainder > 9 else remainder
