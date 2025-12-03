class CpfGeneratorError(Exception):
    """Base exception for all cpf-gen related errors."""


class CpfGeneratorInvalidPrefixLengthError(CpfGeneratorError):
    """Raised when the prefix length is too long."""

    def __init__(self, prefix_length: int, max_length: int) -> None:
        self.prefix_length = prefix_length
        self.max_length = max_length

        super().__init__(
            f"The prefix length must be less than or equal to {max_length}. Got {prefix_length}."
        )
