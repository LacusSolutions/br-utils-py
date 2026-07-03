"""Type aliases for the ``cpf_val`` package."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

CpfInput: TypeAlias = str | Sequence[str]
"""Valid input types for CPF validation.

A CPF may be given as:

- A string of numeric characters (with or without formatting).
- A sequence of strings, each representing one or more numeric characters and/or
  punctuation.
"""

__all__ = ["CpfInput"]
