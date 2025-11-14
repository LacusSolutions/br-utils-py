from collections.abc import Callable


class CnpjFormatterOptions:
    def __init__(
        self,
        escape: bool | None = None,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        on_fail: Callable | None = None,
    ) -> None:
        pass

    def merge(
        self,
        escape: bool | None = None,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        on_fail: Callable | None = None,
    ) -> "CnpjFormatterOptions":
        pass

    def is_escaped(self) -> bool:
        pass

    def is_hidden(self) -> bool:
        pass

    def get_hidden_key(self) -> str:
        pass

    def get_hidden_start(self) -> int:
        pass

    def get_hidden_end(self) -> int:
        pass

    def get_dot_key(self) -> str:
        pass

    def get_slash_key(self) -> str:
        pass

    def get_dash_key(self) -> str:
        pass

    def get_on_fail(self) -> Callable:
        pass

    def set_escape(self, value: bool) -> None:
        pass

    def set_hide(self, value: bool) -> None:
        pass

    def set_hidden_key(self, value: str) -> None:
        pass

    def set_hidden_range(self, start: int, end: int) -> None:
        pass

    def set_dot_key(self, value: str) -> None:
        pass

    def set_slash_key(self, value: str) -> None:
        pass

    def set_dash_key(self, value: str) -> None:
        pass

    def set_on_fail(self, callback: Callable) -> None:
        pass
