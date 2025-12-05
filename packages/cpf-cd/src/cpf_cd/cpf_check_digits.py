import re

from .exceptions import (
    CpfCheckDigitsCalculationError,
    CpfCheckDigitsInputLengthError,
    CpfCheckDigitsInputNotValidError,
    CpfCheckDigitsInputTypeError,
)

CPF_MIN_LENGTH = 9
CPF_MAX_LENGTH = 11


class CpfCheckDigits:
    """Class to calculate CPF check digits."""

    __slots__ = ("_cpf_digits", "_first_digit", "_second_digit")

    def __init__(self, cpf_input: str | list[str] | list[int]) -> None:
        """
        Initialize CpfCheckDigits by validating and normalizing the provided CPF input into the nine base digits.
        
        Parameters:
            cpf_input (str | list[str] | list[int]): A CPF provided as a raw string (may include non-digit characters),
                a list of numeric strings, or a list of integers. The input is converted to a flattened list of integer digits
                and truncated to the first nine digits for internal storage.
        
        Raises:
            CpfCheckDigitsInputTypeError: If cpf_input is not a str or list.
            CpfCheckDigitsInputLengthError: If the sanitized digit list length is less than 9 or greater than 11.
            CpfCheckDigitsInputNotValidError: If the first nine digits are all identical (invalid CPF).
        
        Side effects:
            Sets self._cpf_digits to the first nine digits and initializes self._first_digit and self._second_digit to None.
        """
        original_input = cpf_input

        if not isinstance(cpf_input, (str, list)):
            raise CpfCheckDigitsInputTypeError(original_input)

        if isinstance(cpf_input, str):
            cpf_input = self._handle_string_input(cpf_input)
        else:
            cpf_input = self._handle_list_input(cpf_input, original_input)

        self._validate_length(cpf_input, original_input)
        self._validate_non_repeated_digits(cpf_input, original_input)

        self._cpf_digits = cpf_input[:CPF_MIN_LENGTH]
        self._first_digit: int | None = None
        self._second_digit: int | None = None

    @property
    def first_digit(self) -> int:
        """Calculates and returns the first check digit.As it's immutable, it caches the calculation result."""
        if self._first_digit is None:
            base_digits_sequence = self._cpf_digits.copy()
            self._first_digit = self._calculate(base_digits_sequence)

        return self._first_digit

    @property
    def second_digit(self) -> int:
        """Calculates and returns the second check digit.As it's immutable, it caches the calculation result. And, as it depends on the first check digit, it's also calculated."""
        if self._second_digit is None:
            base_digits_sequence = [*self._cpf_digits, self.first_digit]
            self._second_digit = self._calculate(base_digits_sequence)

        return self._second_digit

    def to_list(self) -> list[int]:
        """Returns the complete CPF as a list of 11 integers (9 base digits + 2 check digits)."""
        return [*self._cpf_digits, self.first_digit, self.second_digit]

    def to_string(self) -> str:
        """
        Produce the full CPF value including its two check digits.
        
        Returns:
            cpf_string (str): The 11-digit CPF composed of the 9 base digits followed by the two check digits.
        """
        return "".join(str(digit) for digit in self.to_list())

    def _handle_string_input(self, cpf_string: str) -> list[int]:
        """
        Sanitize a CPF string by removing non-digit characters and produce its individual digits.
        
        Parameters:
            cpf_string (str): CPF input that may include formatting characters (e.g., dots, dashes, spaces).
        
        Returns:
            list[int]: The sequence of digits from the sanitized CPF, each element as an integer.
        """
        digits_only_string = re.sub(r"[^0-9]", "", cpf_string)

        return [int(digit_string) for digit_string in digits_only_string]

    def _handle_list_input(
        self,
        cpf_list: list[str] | list[int],
        original_input: list,
    ) -> list[int]:
        """
        Convert a list-form CPF into a flattened list of individual integer digits.
        
        Parameters:
            cpf_list (list[str] | list[int]): The input list representation of a CPF; must be either all strings or all integers.
            original_input (list): The original list provided by the caller, forwarded to the error when raised.
        
        Returns:
            digits (list[int]): A list of single-digit integers extracted from the input, suitable for further CPF validation and check-digit calculation.
        
        Raises:
            CpfCheckDigitsInputTypeError: If the list contains mixed or unsupported element types; `original_input` is supplied to the exception for context.
        """
        if all(isinstance(digit, str) for digit in cpf_list):
            return self._handle_string_list_input(cpf_list)

        if all(isinstance(digit, int) for digit in cpf_list):
            return self._flatten_digits(cpf_list)

        raise CpfCheckDigitsInputTypeError(original_input)

    def _handle_string_list_input(self, cpf_string_list: list[str]) -> list[int]:
        """
        Convert a list of CPF string fragments into a flattened list of integer digits.
        
        Each string in `cpf_string_list` may contain non-digit characters; those characters are removed and the remaining digits from all items are concatenated into a single list of integers.
        
        Parameters:
            cpf_string_list (list[str]): List of CPF string fragments (each fragment may contain digits and non-digit characters).
        
        Returns:
            list[int]: Flattened list of individual CPF digits extracted from the input strings.
        """
        final_cpf_int_list = []

        for list_item in cpf_string_list:
            cpf_int_list = self._handle_string_input(list_item)
            final_cpf_int_list.extend(cpf_int_list)

        return final_cpf_int_list

    def _flatten_digits(self, int_list: list[int]) -> list[int]:
        """
        Convert a list of integers into a flattened list of their decimal digits.
        
        Parameters:
            int_list (list[int]): Sequence of integers; each integer is treated by its absolute value and expanded into its decimal digits in original order.
        
        Returns:
            list[int]: A list containing each digit from the input integers, in the same order they appear.
        """
        final_cpf_int_list = []

        for number in int_list:
            abs_number = abs(number)
            final_cpf_int_list.extend(
                [int(digit_string) for digit_string in str(abs_number)]
            )

        return final_cpf_int_list

    def _validate_length(
        self,
        cpf_int_list: list[int],
        original_input: str | list[str] | list[int],
    ) -> None:
        """
        Ensure the list of CPF digits has length between 9 and 11 inclusive.
        
        Parameters:
            cpf_int_list (list[int]): Flattened list of digits derived from the provided input.
            original_input (str | list[str] | list[int]): The original input value used to construct `cpf_int_list`; included in the error for context.
        
        Raises:
            CpfCheckDigitsInputLengthError: If the number of digits is less than 9 or greater than 11.
        """
        digits_count = len(cpf_int_list)

        if digits_count < CPF_MIN_LENGTH or digits_count > CPF_MAX_LENGTH:
            raise CpfCheckDigitsInputLengthError(
                original_input,
                "".join(str(digit) for digit in cpf_int_list),
                CPF_MIN_LENGTH,
                CPF_MAX_LENGTH,
            )

    def _validate_non_repeated_digits(
        self,
        cpf_int_list: list[int],
        original_input: str | list[str] | list[int],
    ) -> None:
        """
        Ensure the first nine CPF digits are not all identical.
        
        Checks the first nine elements of `cpf_int_list` and raises CpfCheckDigitsInputNotValidError if they are the same digit.
        
        Parameters:
            cpf_int_list (list[int]): List of integer digits extracted from the input CPF.
            original_input (str | list[str] | list[int]): The original input provided to the constructor, included in the raised error for context.
        
        Raises:
            CpfCheckDigitsInputNotValidError: If the first nine digits are all the same.
        """
        eligible_cpf_int_list = cpf_int_list[:CPF_MIN_LENGTH]
        digits_set = set(eligible_cpf_int_list)

        if len(digits_set) == 1:
            raise CpfCheckDigitsInputNotValidError(
                original_input,
                "Repeated digits are not considered valid.",
            )

    def _calculate(self, cpf_sequence: list[int]) -> int:
        """
        Compute a CPF check digit from a 9- or 10-digit base sequence using the official Brazilian algorithm.
        
        Parameters:
            cpf_sequence (list[int]): Sequence of digits to use for the calculation — the first 9 digits to produce the first check digit, or the first 10 digits (including the first check digit) to produce the second check digit.
        
        Returns:
            int: The calculated check digit as an integer between 0 and 9.
        
        Raises:
            CpfCheckDigitsCalculationError: If `cpf_sequence` does not contain 9 or 10 digits.
        """
        min_length = CPF_MIN_LENGTH
        max_length = CPF_MAX_LENGTH - 1
        sequence_length = len(cpf_sequence)

        if sequence_length < min_length or sequence_length > max_length:
            raise CpfCheckDigitsCalculationError(cpf_sequence)

        factor = sequence_length + 1
        sum_result = 0

        for num in cpf_sequence:
            sum_result += num * factor
            factor -= 1

        remainder = 11 - (sum_result % 11)

        return 0 if remainder > 9 else remainder