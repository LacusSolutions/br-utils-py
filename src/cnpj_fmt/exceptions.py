"""Custom exceptions for the cnpj-fmt package."""


class CnpjFormatterError(Exception):
    """Base exception for all cnpj-fmt related errors."""


class CnpjInvalidLengthError(CnpjFormatterError):
    """Raised when a CNPJ string does not contain the expected number of digits."""

    def __init__(
        self, cnpj_string: str, expected_length: int, actual_length: int
    ) -> None:
        self.cnpj_string = cnpj_string
        self.expected_length = expected_length
        self.actual_length = actual_length
        message = (
            f'Parameter "{cnpj_string}" does not contain {expected_length} digits. '
            f"Found {actual_length} digit(s)."
        )

        super().__init__(message)


class CnpjRangeError(CnpjFormatterError):
    """Raised when a range value (hidden_start or hidden_end) is out of bounds."""

    def __init__(
        self, option_name: str, value: int, min_val: int, max_val: int
    ) -> None:
        self.option_name = option_name
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        message = (
            f'Option "{option_name}" must be an integer between {min_val} and {max_val}. '
            f"Got {value}."
        )

        super().__init__(message)
