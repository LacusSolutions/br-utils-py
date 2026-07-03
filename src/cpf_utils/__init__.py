"""Unified CPF formatting, generation, and validation API.

Re-exports component classes, options, exceptions, helpers, and a default
:data:`cpf_utils` instance of :class:`CpfUtils`.
"""

from cpf_fmt import (
    CpfFormatter,
    CpfFormatterException,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
    CpfFormatterOptions,
    CpfFormatterOptionsForbiddenKeyCharacterException,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfFormatterOptionsTypeError,
    CpfFormatterTypeError,
    cpf_fmt,
)
from cpf_gen import (
    CpfGenerator,
    CpfGeneratorError,
    CpfGeneratorOptions,
    CpfGeneratorPrefixLengthError,
    CpfGeneratorPrefixNotValidError,
    cpf_gen,
)
from cpf_val import CpfValidator, cpf_val

from .cpf_utils import CpfUtils

__all__ = [
    "CpfFormatter",
    "CpfFormatterException",
    "CpfFormatterInputLengthException",
    "CpfFormatterInputTypeError",
    "CpfFormatterOptions",
    "CpfFormatterOptionsForbiddenKeyCharacterException",
    "CpfFormatterOptionsHiddenRangeInvalidException",
    "CpfFormatterOptionsTypeError",
    "CpfFormatterTypeError",
    "CpfGenerator",
    "CpfGeneratorError",
    "CpfGeneratorOptions",
    "CpfGeneratorPrefixLengthError",
    "CpfGeneratorPrefixNotValidError",
    "CpfUtils",
    "CpfValidator",
    "cpf_fmt",
    "cpf_gen",
    "cpf_utils",
    "cpf_val",
]

__version__ = "0.0.0"

cpf_utils = CpfUtils()
"""Default :class:`CpfUtils` instance with default formatter,
generator, and validator options.
"""
