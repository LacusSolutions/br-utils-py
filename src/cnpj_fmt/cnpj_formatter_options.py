from collections.abc import Callable
from dataclasses import dataclass, replace

from .exceptions import CnpjRangeError

CNPJ_LENGTH = 14


def _default_on_fail(value: str, _error: Exception | None = None) -> str:
    """Default callback for invalid CNPJ input."""
    return value


@dataclass(slots=True, frozen=False)
class CnpjFormatterOptions:
    """Class to manage and store the options for the CNPJ formatter."""

    hidden: bool | None = None
    hidden_key: str | None = None
    hidden_start: int | None = None
    hidden_end: int | None = None
    dot_key: str | None = None
    slash_key: str | None = None
    dash_key: str | None = None
    escape: bool | None = None
    on_fail: Callable | None = None

    def __post_init__(self) -> None:
        if self.hidden is None:
            object.__setattr__(self, "hidden", False)
        if self.hidden_key is None:
            object.__setattr__(self, "hidden_key", "*")
        if self.hidden_start is None:
            object.__setattr__(self, "hidden_start", 5)
        if self.hidden_end is None:
            object.__setattr__(self, "hidden_end", 13)
        if self.dot_key is None:
            object.__setattr__(self, "dot_key", ".")
        if self.slash_key is None:
            object.__setattr__(self, "slash_key", "/")
        if self.dash_key is None:
            object.__setattr__(self, "dash_key", "-")
        if self.escape is None:
            object.__setattr__(self, "escape", False)
        if self.on_fail is None:
            object.__setattr__(self, "on_fail", _default_on_fail)

        self.set_hidden_range(self.hidden_start, self.hidden_end)

        if not callable(self.on_fail):
            raise TypeError(
                f'"on_fail" argument must be a callable, {type(self.on_fail).__name__} given'
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
        """Creates a new CnpjFormatterOptions instance with the given options merged with the current instance."""
        kwargs = {}

        if hidden is not None:
            kwargs["hidden"] = hidden
        if hidden_key is not None:
            kwargs["hidden_key"] = hidden_key
        if hidden_start is not None:
            kwargs["hidden_start"] = hidden_start
        if hidden_end is not None:
            kwargs["hidden_end"] = hidden_end
        if dot_key is not None:
            kwargs["dot_key"] = dot_key
        if slash_key is not None:
            kwargs["slash_key"] = slash_key
        if dash_key is not None:
            kwargs["dash_key"] = dash_key
        if escape is not None:
            kwargs["escape"] = escape
        if on_fail is not None:
            kwargs["on_fail"] = on_fail

        new_start = kwargs.get("hidden_start", self.hidden_start)
        new_end = kwargs.get("hidden_end", self.hidden_end)

        new_options = replace(self, **kwargs)
        new_options.set_hidden_range(new_start, new_end)

        return new_options

    def set_hidden_range(self, start: int, end: int) -> None:
        """Sets the range of hidden digits for the CNPJ formatter."""
        min_val = 0
        max_val = CNPJ_LENGTH - 1

        if start < min_val or start > max_val:
            raise CnpjRangeError("hidden_start", start, min_val, max_val)

        if end < min_val or end > max_val:
            raise CnpjRangeError("hidden_end", end, min_val, max_val)

        if start > end:
            start, end = end, start

        object.__setattr__(self, "hidden_start", start)
        object.__setattr__(self, "hidden_end", end)

    def __setattr__(self, name: str, value: object):
        if name == "hidden_start":
            if value is not None:
                object.__setattr__(self, name, value)

                if hasattr(self, "hidden_end") and self.hidden_end is not None:
                    self.set_hidden_range(self.hidden_start, self.hidden_end)
                    return
        elif name == "hidden_end":
            if value is not None:
                object.__setattr__(self, name, value)

                if hasattr(self, "hidden_start") and self.hidden_start is not None:
                    self.set_hidden_range(self.hidden_start, self.hidden_end)
                    return
        elif name == "on_fail":
            if value is None:
                if hasattr(self, "on_fail") and self.on_fail is not None:
                    raise TypeError(
                        '"on_fail" argument must be a callable, NoneType given'
                    )
            elif not callable(value):
                raise TypeError(
                    f'"on_fail" argument must be a callable, {type(value).__name__} given'
                )

        object.__setattr__(self, name, value)
