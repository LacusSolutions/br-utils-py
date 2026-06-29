from collections.abc import Callable

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions
from cnpj_gen import CnpjGenerator, CnpjGeneratorOptions
from cnpj_val import CnpjValidator


class CnpjUtils:
    """Class to manipulate CNPJ strings."""

    __slots__ = ("formatter", "generator", "validator")

    def __init__(
        self,
        formatter: CnpjFormatterOptions | None = None,
        generator: CnpjGeneratorOptions | None = None,
    ):
        self.formatter = CnpjFormatter(formatter)
        self.generator = CnpjGenerator(generator)
        self.validator = CnpjValidator()

    def format(
        self,
        cnpj_string: str,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> str:
        return self.formatter.format(
            cnpj_string,
            hidden=hidden,
            hidden_key=hidden_key,
            hidden_start=hidden_start,
            hidden_end=hidden_end,
            dot_key=dot_key,
            slash_key=slash_key,
            dash_key=dash_key,
            escape=escape,
            on_fail=on_fail,
        )

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return self.generator.generate(format=format, prefix=prefix)

    def is_valid(self, cnpj_string: str) -> bool:
        return self.validator.is_valid(cnpj_string)
