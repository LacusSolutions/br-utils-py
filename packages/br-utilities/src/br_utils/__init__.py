"""Utility resources to deal with Brazilian-related data.

Provides :class:`~br_utils.br_utils.BrUtils`, the default singleton
:data:`br_utils`, and re-exports from :mod:`br_utils.cpf` and
:mod:`br_utils.cnpj`.
"""

from .br_utils import BrUtils
from .cnpj import (
    CnpjUtils,
    cnpj_utils,
)
from .cpf import (
    CpfUtils,
    cpf_utils,
)

__all__ = [
    "BrUtils",
    "CnpjUtils",
    "CpfUtils",
    "br_utils",
    "cnpj_utils",
    "cpf_utils",
]

__version__ = "0.0.0"

br_utils = BrUtils()
"""Default :class:`BrUtils` instance with default CPF and CNPJ utilities."""
