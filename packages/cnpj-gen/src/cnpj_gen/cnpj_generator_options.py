import re
from dataclasses import dataclass, replace

from .exceptions import InvalidArgumentException

CNPJ_LENGTH = 14


@dataclass(slots=True, frozen=False)
class CnpjGeneratorOptions:
    format: bool | None = None
    prefix: str | None = None

    def __post_init__(self) -> None:
        if self.format is None:
            object.__setattr__(self, "format", False)
        if self.prefix is None:
            object.__setattr__(self, "prefix", "")

    def merge(
        self,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> "CnpjGeneratorOptions":
        kwargs = {}

        if format is not None:
            kwargs["format"] = format
        if prefix is not None:
            kwargs["prefix"] = prefix

        new_options = replace(self, **kwargs)

        return new_options

    def __setattr__(self, name: str, value: object) -> None:
        if name == "prefix" and value is not None:
            min_digits = 0
            max_digits = CNPJ_LENGTH - 2
            value = re.sub(r"[^0-9]", "", value)
            prefix_length = len(value)

            if prefix_length > CNPJ_LENGTH - 2:
                raise InvalidArgumentException(
                    f'Option "prefix" must be a string containing between {min_digits} and {max_digits} digits.'
                )

            if prefix_length > 8 and value[8:] == "0000":
                raise InvalidArgumentException(
                    'The branch ID (characters 8 to 11) cannot be "0000".'
                )

        object.__setattr__(self, name, value)
