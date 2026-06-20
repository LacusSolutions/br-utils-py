import math
from collections.abc import Callable
from typing import Any


def _describe_item(item: Any) -> str:
    """Return a type label for an element inside a list or tuple."""
    if item is None:
        return "NoneType"

    if isinstance(item, bool):
        return "boolean"

    if isinstance(item, int):
        return "number"

    if isinstance(item, float):
        if math.isnan(item):
            return "NaN"

        if math.isinf(item):
            return "Infinity"

        return "number"

    if isinstance(item, str):
        return "string"

    return _describe_type(item)


def _describe_sequence(
    items: list[Any] | tuple[Any, ...],
    empty_label: str,
    suffix: str,
) -> str:
    if not items:
        return empty_label

    unique_types: dict[str, None] = {}

    for item in items:
        label = _describe_item(item)

        if label not in unique_types:
            unique_types[label] = None

    type_labels = list(unique_types.keys())

    if len(type_labels) == 1:
        return f"{type_labels[0]}{suffix}"

    return f"({' | '.join(type_labels)}){suffix}"


def _describe_type(value: Any) -> str:
    if isinstance(value, list):
        return _describe_sequence(value, "Array (empty)", "[]")

    if isinstance(value, tuple):
        return _describe_sequence(value, "tuple (empty)", " tuple")

    if value is None:
        return "NoneType"

    if isinstance(value, bool):
        return "boolean"

    if isinstance(value, int):
        return "integer number"

    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"

        if math.isinf(value):
            return "Infinity"

        return "float number"

    if isinstance(value, complex):
        return "complex number"

    if isinstance(value, str):
        return "string"

    if isinstance(value, dict):
        return "dict"

    if isinstance(value, set):
        return "set"

    if isinstance(value, frozenset):
        return "frozenset"

    if isinstance(value, bytes):
        return "bytes"

    if isinstance(value, bytearray):
        return "bytearray"

    if isinstance(value, type):
        return "type"

    if isinstance(value, Callable):
        return "function"

    return "object"


def describe_type(value: Any) -> str:
    """Describe the type of a value for error messages.

    Args:
        value: Any value to describe.

    Returns:
        A human-readable type label. For example, ``None`` returns ``"NoneType"``,
        ``42`` returns ``"integer number"``, ``[1, 2, 3]`` returns ``"number[]"``,
        and ``(1, "a")`` returns ``"(number | string) tuple"``.

    Examples:
        >>> describe_type(None)
        'NoneType'
        >>> describe_type("hello")
        'string'
        >>> describe_type(True)
        'boolean'
        >>> describe_type(42)
        'integer number'
        >>> describe_type(3.14)
        'float number'
        >>> describe_type(float("nan"))
        'NaN'
        >>> describe_type(float("inf"))
        'Infinity'
        >>> describe_type([])
        'Array (empty)'
        >>> describe_type([1, 2, 3])
        'number[]'
        >>> describe_type([1, "a", 2])
        '(number | string)[]'
        >>> describe_type({})
        'dict'
        >>> describe_type(())
        'tuple (empty)'
        >>> describe_type((1, 2))
        'number tuple'
    """
    return _describe_type(value)
