import html
import re
from collections.abc import Callable

from .cnpj_formatter_options import CNPJ_LENGTH, CnpjFormatterOptions


class CnpjFormatter:
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
        self.__options = CnpjFormatterOptions(
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
        actual_options = self.__get_options().merge(
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

        cnpj_numbers_string = re.sub(r"[^0-9]", "", cnpj_string)
        cnpj_numbers_array = list(cnpj_numbers_string)

        if len(cnpj_numbers_array) != CNPJ_LENGTH:
            error = ValueError(
                f'Parameter "{cnpj_string}" does not contain {CNPJ_LENGTH} digits.'
            )

            on_fail_callback = actual_options.on_fail

            try:
                return on_fail_callback(cnpj_string, error)
            except TypeError:
                return on_fail_callback(cnpj_string)

        if actual_options.hidden:
            hidden_start = actual_options.hidden_start
            hidden_end = actual_options.hidden_end
            hidden_key = actual_options.hidden_key

            for i in range(hidden_start, hidden_end + 1):
                cnpj_numbers_array[i] = hidden_key

        dot_key = actual_options.dot_key
        dash_key = actual_options.dash_key
        slash_key = actual_options.slash_key

        cnpj_numbers_array.insert(12, dash_key)
        cnpj_numbers_array.insert(8, slash_key)
        cnpj_numbers_array.insert(5, dot_key)
        cnpj_numbers_array.insert(2, dot_key)

        pretty_cnpj = "".join(cnpj_numbers_array)

        if actual_options.escape:
            return html.escape(pretty_cnpj, quote=True)

        return pretty_cnpj

    def __get_options(self) -> CnpjFormatterOptions:
        return self.__options

    options = property(__get_options)
