from collections.abc import Callable

CNPJ_LENGTH = 14


class CnpjFormatterOptions:
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
        self.__set_hidden(hidden if hidden is not None else False)
        self.__set_hidden_key(hidden_key if hidden_key is not None else "*")
        self.set_hidden_range(
            hidden_start if hidden_start is not None else 5,
            hidden_end if hidden_end is not None else 13,
        )
        self.__set_dot_key(dot_key if dot_key is not None else ".")
        self.__set_slash_key(slash_key if slash_key is not None else "/")
        self.__set_dash_key(dash_key if dash_key is not None else "-")
        self.__set_escape(escape if escape is not None else False)
        self.__set_on_fail(
            on_fail if on_fail is not None else (lambda value, error=None: value)
        )

    def merge(
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
    ) -> "CnpjFormatterOptions":
        return CnpjFormatterOptions(
            hidden if hidden is not None else self.hidden,
            hidden_key if hidden_key is not None else self.hidden_key,
            hidden_start if hidden_start is not None else self.hidden_start,
            hidden_end if hidden_end is not None else self.hidden_end,
            dot_key if dot_key is not None else self.dot_key,
            slash_key if slash_key is not None else self.slash_key,
            dash_key if dash_key is not None else self.dash_key,
            escape if escape is not None else self.escape,
            on_fail if on_fail is not None else self.on_fail,
        )

    def set_hidden_range(self, start: int, end: int) -> None:
        min_val = 0
        max_val = CNPJ_LENGTH - 1

        if start < min_val or start > max_val:
            raise ValueError(
                f'Option "hiddenStart" must be an integer between {min_val} and {max_val}.'
            )

        if end < min_val or end > max_val:
            raise ValueError(
                f'Option "hiddenRange.end" must be an integer between {min_val} and {max_val}.'
            )

        if start > end:
            aux = start
            start = end
            end = aux

        self.__hidden_start = start
        self.__hidden_end = end

    def __set_escape(self, value: bool) -> None:
        self.__escape = value

    def __is_escape(self) -> bool:
        return self.__escape

    def __set_hidden(self, value: bool) -> None:
        self.__hidden = value

    def __is_hidden(self) -> bool:
        return self.__hidden

    def __set_hidden_key(self, value: str) -> None:
        self.__hidden_key = value

    def __get_hidden_key(self) -> str:
        return self.__hidden_key

    def __set_hidden_start(self, value: int) -> None:
        self.set_hidden_range(value, self.__hidden_end)

    def __get_hidden_start(self) -> int:
        return self.__hidden_start

    def __set_hidden_end(self, value: int) -> None:
        self.set_hidden_range(self.__hidden_start, value)

    def __get_hidden_end(self) -> int:
        return self.__hidden_end

    def __set_dot_key(self, value: str) -> None:
        self.__dot_key = value

    def __get_dot_key(self) -> str:
        return self.__dot_key

    def __set_slash_key(self, value: str) -> None:
        self.__slash_key = value

    def __get_slash_key(self) -> str:
        return self.__slash_key

    def __set_dash_key(self, value: str) -> None:
        self.__dash_key = value

    def __get_dash_key(self) -> str:
        return self.__dash_key

    def __set_on_fail(self, callback: Callable) -> None:
        if not callable(callback):
            raise TypeError(
                f"must be of type Callable, {type(callback).__name__} given"
            )

        self.__on_fail = callback

    def __get_on_fail(self) -> Callable:
        return self.__on_fail

    hidden = property(__is_hidden, __set_hidden)
    hidden_key = property(__get_hidden_key, __set_hidden_key)
    hidden_start = property(__get_hidden_start, __set_hidden_start)
    hidden_end = property(__get_hidden_end, __set_hidden_end)
    dot_key = property(__get_dot_key, __set_dot_key)
    slash_key = property(__get_slash_key, __set_slash_key)
    dash_key = property(__get_dash_key, __set_dash_key)
    escape = property(__is_escape, __set_escape)
    on_fail = property(__get_on_fail, __set_on_fail)
