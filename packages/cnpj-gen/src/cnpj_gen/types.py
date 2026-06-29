"""Type aliases for the ``cnpj_gen`` package."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeAlias, TypedDict

CnpjType = Literal["alphanumeric", "alphabetic", "numeric"]
"""Character type for the generated CNPJ sequence.

- ``"alphanumeric"`` (default): Generates a sequence of alphanumeric characters
  (``0-9A-Z``).
- ``"numeric"``: Generates a sequence of numbers-only characters (``0-9``).
- ``"alphabetic"``: Generates a sequence of alphabetic characters (``A-Z``).
"""


class CnpjGeneratorOptionsType(TypedDict):
    """Configuration for CNPJ generation options.

    Defines the resolved options used internally: ``format`` (standard
    masking), ``prefix`` (partial start string), and ``type`` (character
    set). All properties have default values when creating a
    :class:`~cnpj_gen.cnpj_generator_options.CnpjGeneratorOptions`
    instance.

    Attributes:
        ``format``: Whether to format the generated CNPJ string as
            ``00.000.000/0000-00``.
        ``prefix``: A partial string containing 0 to 12 alphanumeric
            characters to use as the start of the generated CNPJ. Only
            alphanumeric characters are kept; the rest is stripped. If
            provided, only the missing characters are generated
            randomly. For example, if the ``prefix`` ``AAABBB`` (``6``
            characters) is given, only the next 8 characters are
            randomly generated and concatenated to the ``prefix``.

            A common use case is to provide a base ID (first ``8``
            characters) and let the library generate the branch ID
            (characters ``9`` to ``12``) for multiple runs. This way you
            can generate multiple CNPJs under the same "business
            umbrella".

            Note: If the evaluated ``prefix`` (after stripping
            non-alphanumeric characters) is longer than 12 characters,
            the extra characters are ignored, because a CNPJ has 12 base
            characters followed by 2 calculated check digits.
        type: The character ``type`` for random CNPJ segments. If a
            ``prefix`` is provided, only the remaining characters
            (those generated randomly) use this ``type``.

            The options are:

            - ``"alphabetic"``: Generates a sequence of alphabetic characters
              (``A-Z``).
            - ``"alphanumeric"``: Generates a sequence of alphanumeric
              characters (``0-9A-Z``).
            - ``"numeric"``: Generates a sequence of numbers-only characters
              (``0-9``).
    """

    format: bool
    prefix: str
    type: CnpjType


from .cnpj_generator_options import CnpjGeneratorOptions  # noqa: E402

CnpjGeneratorOptionsInput: TypeAlias = CnpjGeneratorOptions | Mapping[str, Any] | None
"""Options input accepted by constructors and merge helpers.

May be a :class:`~cnpj_gen.cnpj_generator_options.CnpjGeneratorOptions`
instance, a partial options ``Mapping[str, Any]``, or ``None``.
"""

__all__ = [
    "CnpjGeneratorOptionsInput",
    "CnpjGeneratorOptionsType",
    "CnpjType",
]
