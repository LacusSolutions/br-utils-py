import html
from collections.abc import Callable

from .cnpj_formatter_options import CNPJ_LENGTH, CnpjFormatterOptions


class CnpjFormatter:
    __slots__ = ("_options",)

    def __init__(
        self,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> None:
        self._options = CnpjFormatterOptions(
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            slash_key,
            dash_key,
            escape,
            on_fail,
        )

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
        actual_options = self._options.merge(
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            slash_key,
            dash_key,
            escape,
            on_fail,
        )

        cnpj_numbers_string = "".join(filter(str.isdigit, cnpj_string))

        if len(cnpj_numbers_string) != CNPJ_LENGTH:
            on_fail_callback = actual_options.on_fail

            try:
                error = ValueError(
                    f'Parameter "{cnpj_string}" does not contain {CNPJ_LENGTH} digits.'
                )
                return on_fail_callback(cnpj_string, error)
            except TypeError:
                return on_fail_callback(cnpj_string)

        if actual_options.hidden:
            hidden_start = actual_options.hidden_start
            hidden_end = actual_options.hidden_end
            hidden_key = actual_options.hidden_key

            prefix = cnpj_numbers_string[:hidden_start]
            hidden_part_length = hidden_end - hidden_start + 1
            masked = hidden_key * hidden_part_length
            suffix = cnpj_numbers_string[hidden_end + 1 :]
            cnpj_numbers_string = prefix + masked + suffix

        pretty_cnpj = (
            cnpj_numbers_string[0:2]
            + actual_options.dot_key
            + cnpj_numbers_string[2:5]
            + actual_options.dot_key
            + cnpj_numbers_string[5:8]
            + actual_options.slash_key
            + cnpj_numbers_string[8:12]
            + actual_options.dash_key
            + cnpj_numbers_string[12:14]
        )

        if actual_options.escape:
            return html.escape(pretty_cnpj, quote=True)

        return pretty_cnpj

    @property
    def options(self) -> CnpjFormatterOptions:
        return self._options
