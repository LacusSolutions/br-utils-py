from typing import Literal

SequenceType = Literal["alphabetic", "alphanumeric", "numeric"]
"""Character type for random sequence generation.

- ``"alphanumeric"``: digits and uppercase letters (``0-9A-Z``).
- ``"numeric"``: digits only (``0-9``).
- ``"alphabetic"``: uppercase letters only (``A-Z``).
"""
