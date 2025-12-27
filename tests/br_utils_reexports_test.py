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
            CnpjFormatterError,
            CnpjFormatterHiddenRangeError,
            CnpjFormatterInputLengthError,
            CnpjFormatterOptions,
            CnpjGenerator,
            CnpjGeneratorError,
            CnpjGeneratorOptions,
            CnpjGeneratorPrefixBranchIdError,
            CnpjGeneratorPrefixLengthError,
            CnpjUtils,
            CnpjValidator,
            cnpj_fmt,
            cnpj_gen,
            cnpj_utils,
            cnpj_val,
        )

        assert CnpjFormatter is not None
        assert CnpjFormatterError is not None
        assert CnpjFormatterHiddenRangeError is not None
        assert CnpjFormatterInputLengthError is not None
        assert CnpjFormatterOptions is not None
        assert CnpjGenerator is not None
        assert CnpjGeneratorError is not None
        assert CnpjGeneratorPrefixBranchIdError is not None
        assert CnpjGeneratorPrefixLengthError is not None
        assert CnpjGeneratorOptions is not None
        assert CnpjUtils is not None
        assert CnpjValidator is not None
        assert cnpj_fmt is not None
        assert cnpj_gen is not None
        assert cnpj_utils is not None
        assert cnpj_val is not None
