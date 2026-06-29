from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterException,
    CnpjFormatterInputLengthException,
    CnpjFormatterOptions,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    cnpj_fmt,
)
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorException,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    cnpj_gen,
)
from cnpj_val import CnpjValidator, cnpj_val

from .cnpj_utils import CnpjUtils

CnpjFormatterError = CnpjFormatterException
CnpjFormatterHiddenRangeError = CnpjFormatterOptionsHiddenRangeInvalidException
CnpjFormatterInvalidLengthError = CnpjFormatterInputLengthException
CnpjGeneratorError = CnpjGeneratorException
CnpjGeneratorInvalidPrefixBranchIdError = CnpjGeneratorOptionPrefixInvalidException
CnpjGeneratorInvalidPrefixLengthError = CnpjGeneratorOptionPrefixInvalidException

__all__ = [
    "CnpjFormatter",
    "CnpjFormatterError",
    "CnpjFormatterException",
    "CnpjFormatterHiddenRangeError",
    "CnpjFormatterInputLengthException",
    "CnpjFormatterInvalidLengthError",
    "CnpjFormatterOptions",
    "CnpjFormatterOptionsHiddenRangeInvalidException",
    "CnpjGenerator",
    "CnpjGeneratorError",
    "CnpjGeneratorException",
    "CnpjGeneratorInvalidPrefixBranchIdError",
    "CnpjGeneratorInvalidPrefixLengthError",
    "CnpjGeneratorOptionPrefixInvalidException",
    "CnpjGeneratorOptions",
    "CnpjUtils",
    "CnpjValidator",
    "cnpj_fmt",
    "cnpj_gen",
    "cnpj_utils",
    "cnpj_val",
]

__version__ = "0.0.0"

# Default instance of CnpjUtils
cnpj_utils = CnpjUtils()
