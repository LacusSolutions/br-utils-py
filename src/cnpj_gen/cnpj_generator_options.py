import re

from .exceptions import InvalidArgumentException

CNPJ_LENGTH = 14


class CnpjGeneratorOptions:
    def __init__(self, format: bool | None = None, prefix: str | None = None):
        self.set_format(format if format is not None else False)
        self.set_prefix(prefix if prefix is not None else "")

    def merge(
        self,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> "CnpjGeneratorOptions":
        return CnpjGeneratorOptions(
            format if format is not None else self.is_formatting(),
            prefix if prefix is not None else self.get_prefix(),
        )

    def set_format(self, value: bool) -> None:
        self._format = value

    def is_formatting(self) -> bool:
        return self._format

    def set_prefix(self, value: str) -> None:
        min_digits = 0
        max_digits = CNPJ_LENGTH - 2
        digits_only = re.sub(r"[^0-9]", "", value)
        prefix_length = len(digits_only)

        if prefix_length > CNPJ_LENGTH - 2:
            raise InvalidArgumentException(
                f'Option "prefix" must be a string containing between {min_digits} and {max_digits} digits.'
            )

        if prefix_length > 8 and digits_only[8:] == "0000":
            raise InvalidArgumentException(
                'The branch ID (characters 8 to 11) cannot be "0000".'
            )

        self._prefix = digits_only

    def get_prefix(self) -> str:
        return self._prefix
