"""Unit tests for br-utils."""


class BrUtilsReexportsTest:
    def test_cpf_utils_reexports(self):
        from br_utils.cpf import (
            CpfFormatter,
            CpfFormatterError,
            CpfFormatterHiddenRangeError,
            CpfFormatterInputLengthError,
            CpfFormatterOptions,
            CpfGenerator,
            CpfGeneratorError,
            CpfGeneratorOptions,
            CpfGeneratorPrefixLengthError,
            CpfGeneratorPrefixNotValidError,
            CpfUtils,
            CpfValidator,
            cpf_fmt,
            cpf_gen,
            cpf_utils,
            cpf_val,
        )

        assert CpfFormatter is not None
        assert CpfFormatterError is not None
        assert CpfFormatterHiddenRangeError is not None
        assert CpfFormatterInputLengthError is not None
        assert CpfFormatterOptions is not None
        assert CpfGenerator is not None
        assert CpfGeneratorError is not None
        assert CpfGeneratorOptions is not None
        assert CpfGeneratorPrefixLengthError is not None
        assert CpfGeneratorPrefixNotValidError is not None
        assert CpfUtils is not None
        assert CpfValidator is not None
        assert cpf_fmt is not None
        assert cpf_gen is not None
        assert cpf_utils is not None
        assert cpf_val is not None

    def test_cnpj_utils_reexports(self):
        from br_utils.cnpj import (
            CnpjFormatter,
            CnpjFormatterException,
            CnpjFormatterInputLengthException,
            CnpjFormatterInputTypeError,
            CnpjFormatterOptions,
            CnpjFormatterOptionsForbiddenKeyCharacterException,
            CnpjFormatterOptionsHiddenRangeInvalidException,
            CnpjFormatterOptionsTypeError,
            CnpjFormatterTypeError,
            CnpjGenerator,
            CnpjGeneratorException,
            CnpjGeneratorOptionPrefixInvalidException,
            CnpjGeneratorOptions,
            CnpjGeneratorOptionsTypeError,
            CnpjGeneratorOptionTypeInvalidException,
            CnpjGeneratorTypeError,
            CnpjUtils,
            CnpjValidator,
            CnpjValidatorException,
            CnpjValidatorInputTypeError,
            CnpjValidatorOptions,
            CnpjValidatorOptionsTypeError,
            CnpjValidatorOptionTypeInvalidException,
            CnpjValidatorTypeError,
            cnpj_fmt,
            cnpj_gen,
            cnpj_utils,
            cnpj_val,
        )

        assert CnpjFormatter is not None
        assert CnpjFormatterException is not None
        assert CnpjFormatterInputLengthException is not None
        assert CnpjFormatterInputTypeError is not None
        assert CnpjFormatterOptions is not None
        assert CnpjFormatterOptionsForbiddenKeyCharacterException is not None
        assert CnpjFormatterOptionsHiddenRangeInvalidException is not None
        assert CnpjFormatterOptionsTypeError is not None
        assert CnpjFormatterTypeError is not None
        assert CnpjGenerator is not None
        assert CnpjGeneratorException is not None
        assert CnpjGeneratorOptionPrefixInvalidException is not None
        assert CnpjGeneratorOptionTypeInvalidException is not None
        assert CnpjGeneratorOptions is not None
        assert CnpjGeneratorOptionsTypeError is not None
        assert CnpjGeneratorTypeError is not None
        assert CnpjUtils is not None
        assert CnpjValidator is not None
        assert CnpjValidatorException is not None
        assert CnpjValidatorInputTypeError is not None
        assert CnpjValidatorOptions is not None
        assert CnpjValidatorOptionsTypeError is not None
        assert CnpjValidatorOptionTypeInvalidException is not None
        assert CnpjValidatorTypeError is not None
        assert cnpj_fmt is not None
        assert cnpj_gen is not None
        assert cnpj_utils is not None
        assert cnpj_val is not None
