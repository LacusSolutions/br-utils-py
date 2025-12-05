class CpfCheckDigitsError(Exception):
    """Base exception for all cpf-cd related errors."""


class CpfCheckDigitsInputTypeError(CpfCheckDigitsError):
    """Raised when the class input does not match the expected type."""

    def __init__(self, actual_input) -> None:
        """
        Initialize the exception for an input with an unsupported type.
        
        Parameters:
        	actual_input: The value provided to the CPF check-digit routine; stored on the exception instance. The exception message indicates the expected types (str, list[str], or list[int]) and the actual type received.
        """
        self.actual_input = actual_input

        super().__init__(
            f"CPF input must be of type str, list[str] or list[int]. Got {type(actual_input).__name__}."
        )


class CpfCheckDigitsInputLengthError(CpfCheckDigitsError):
    """Raised when the class input does not contain the expected number of digits."""

    def __init__(
        self,
        actual_input: str | list[str] | list[int],
        evaluated_input: str,
        min_expected_length: int,
        max_expected_length: int,
    ) -> None:
        """
        Initialize an error indicating the CPF input does not contain the expected number of digits.
        
        Parameters:
        	actual_input (str | list[str] | list[int]): The original input provided by the caller; may be a raw string or a list of characters/integers. Stored on the instance as `actual_input`.
        	evaluated_input (str): The digits-only representation derived from `actual_input` that is used to evaluate length. Stored on the instance as `evaluated_input`.
        	min_expected_length (int): Minimum number of digits expected. Stored on the instance as `min_expected_length`.
        	max_expected_length (int): Maximum number of digits expected. Stored on the instance as `max_expected_length`.
        
        Notes:
        	The exception message includes the expected digit range and the evaluated input length, and formats the original input distinctly when it was supplied as a string.
        """
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length

        if isinstance(actual_input, str):
            fmt_actual_input = f'"{actual_input}"'
        else:
            fmt_actual_input = f"{actual_input}"

        if actual_input == evaluated_input:
            fmt_evaluated_input = f"{len(evaluated_input)}"
        else:
            fmt_evaluated_input = f'{len(evaluated_input)} in "{evaluated_input}"'

        super().__init__(
            f"CPF input {fmt_actual_input} does not contain "
            f"{min_expected_length} to {max_expected_length} digits. "
            f"Got {fmt_evaluated_input}."
        )


class CpfCheckDigitsInputNotValidError(CpfCheckDigitsError):
    """Raised when the class input contains non-invalid characters."""

    def __init__(self, actual_input: str | list[str] | list[int], reason: str) -> None:
        """
        Initialize the exception with the offending input and a human-readable reason.
        
        Parameters:
            actual_input (str | list[str] | list[int]): The original input that failed validation.
            reason (str): A brief explanation of why the input is considered invalid.
        
        Notes:
            The instance stores `actual_input` and `reason`, and the exception message includes a formatted representation of `actual_input` followed by `reason`.
        """
        self.actual_input = actual_input
        self.reason = reason

        if isinstance(actual_input, str):
            fmt_actual_input = f'"{actual_input}"'
        else:
            fmt_actual_input = f"{actual_input}"

        super().__init__(f"CPF input {fmt_actual_input} is invalid. {reason}")


class CpfCheckDigitsCalculationError(CpfCheckDigitsError):
    """Raised when the calculation of the CPF check digits fails."""

    def __init__(self, actual_input: list[int]) -> None:
        """
        Initialize the CpfCheckDigitsCalculationError for a failed check-digit calculation.
        
        Parameters:
        	actual_input (list[int]): The digit sequence that failed check-digit calculation; stored on the exception and included in the exception message.
        """
        self.actual_input = actual_input

        super().__init__(
            f"Failed to calculate CPF check digits for the sequence: {actual_input}."
        )