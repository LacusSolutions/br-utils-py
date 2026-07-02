"""Unified CNPJ formatting, generation, and validation API.

Re-exports component classes, options, exceptions, helpers, and a default
:data:`cnpj_utils` instance of :class:`CnpjUtils`.
"""

from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterException,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
    CnpjFormatterOptions,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjFormatterOptionsTypeError,
    CnpjFormatterTypeError,
    cnpj_fmt,
)
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorException,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjGeneratorTypeError,
    cnpj_gen,
)
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptions,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    CnpjValidatorTypeError,
    cnpj_val,
)

from .cnpj_utils import CnpjUtils

__all__ = [
    "CnpjFormatter",
    "CnpjFormatterException",
    "CnpjFormatterInputLengthException",
    "CnpjFormatterInputTypeError",
    "CnpjFormatterOptions",
    "CnpjFormatterOptionsForbiddenKeyCharacterException",
    "CnpjFormatterOptionsHiddenRangeInvalidException",
    "CnpjFormatterOptionsTypeError",
    "CnpjFormatterTypeError",
    "CnpjGenerator",
    "CnpjGeneratorException",
    "CnpjGeneratorOptionPrefixInvalidException",
    "CnpjGeneratorOptionTypeInvalidException",
    "CnpjGeneratorOptions",
    "CnpjGeneratorOptionsTypeError",
    "CnpjGeneratorTypeError",
    "CnpjUtils",
    "CnpjValidator",
    "CnpjValidatorException",
    "CnpjValidatorInputTypeError",
    "CnpjValidatorOptionTypeInvalidException",
    "CnpjValidatorOptions",
    "CnpjValidatorOptionsTypeError",
    "CnpjValidatorTypeError",
    "cnpj_fmt",
    "cnpj_gen",
    "cnpj_utils",
    "cnpj_val",
]

__version__ = "0.0.0"

cnpj_utils = CnpjUtils()
"""Default :class:`CnpjUtils` instance with default formatter,
generator, and validator options.
"""
