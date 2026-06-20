import math
from typing import Any


def _describe_item(item: Any) -> str:
    """Return a JS ``typeof``-style type label for a list element."""
    if item is None:
        return "object"

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

    return "object"


def describe_type(value: Any) -> str:
    """Describe the type of a value for error messages.

    Args:
        value: Any value to describe.

    Returns:
        A human-readable type label. For example, ``None`` returns ``"null"``,
        ``42`` returns ``"integer number"``, ``[1, 2, 3]`` returns ``"number[]"``,
        and ``[1, "a", 2]`` returns ``"(number | string)[]"``.

    Examples:
        >>> describe_type(None)
        'null'
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
        'object'
    """
    if isinstance(value, list):
        if not value:
            return "Array (empty)"

        unique_types: dict[str, None] = {}

        for item in value:
            label = _describe_item(item)

            if label not in unique_types:
                unique_types[label] = None

        type_labels = list(unique_types.keys())

        if len(type_labels) == 1:
            return f"{type_labels[0]}[]"

        return f"({' | '.join(type_labels)})[]"

    if value is None:
        return "null"

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

    if isinstance(value, str):
        return "string"

    return "object"
