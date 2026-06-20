import secrets

from .types import SequenceType

_NUMERIC = "0123456789"
_ALPHABETIC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ALPHANUMERIC = _NUMERIC + _ALPHABETIC


def generate_random_sequence(size: int, sequence_type: SequenceType) -> str:
    """Generate a random character sequence of the given length and type.

    Args:
        size: Length of the sequence.
        sequence_type: Character set to draw from. One of ``"numeric"`` (``0-9``),
            ``"alphabetic"`` (``A-Z``), or ``"alphanumeric"`` (``0-9A-Z``).

    Returns:
        A random string of the requested length using uppercase letters and/or
        digits, depending on ``sequence_type``.

    Examples:
        >>> generate_random_sequence(10, "numeric")  # doctest: +SKIP
        '9956000611'
        >>> generate_random_sequence(6, "alphabetic")  # doctest: +SKIP
        'AXQMZB'
        >>> generate_random_sequence(8, "alphanumeric")  # doctest: +SKIP
        '8ZFB2K09'
    """
    if sequence_type == "numeric":
        chars = _NUMERIC
    elif sequence_type == "alphabetic":
        chars = _ALPHABETIC
    else:
        chars = _ALPHANUMERIC

    return "".join(secrets.choice(chars) for _ in range(size))
