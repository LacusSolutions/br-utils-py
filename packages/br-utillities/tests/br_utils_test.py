"""Unit tests for br-utils."""

import pytest
from br_utils import BrUtils, br_utils


class BrUtilsInitTest:
    def test_init_creates_cpf_and_cnpj_instances(self):
        utils = BrUtils()

        assert utils.cpf is not None
        assert utils.cnpj is not None

    def test_default_instance_is_available(self):
        assert br_utils is not None
        assert isinstance(br_utils, BrUtils)

    def test_slots_restriction(self):
        utils = BrUtils()

        with pytest.raises(AttributeError):
            utils.new_attribute = "test"

        assert hasattr(utils, "cpf")
        assert hasattr(utils, "cnpj")


class BrUtilsCpfTest:
    def test_cpf_format(self):
        utils = BrUtils()
        result = utils.cpf.format("12345678901")

        assert result == "123.456.789-01"

    def test_cpf_generate(self):
        utils = BrUtils()
        result = utils.cpf.generate()

        assert len(result) == 11

    def test_cpf_is_valid(self):
        utils = BrUtils()

        assert utils.cpf.is_valid("52998224725") is True
        assert utils.cpf.is_valid("12345678901") is False


class BrUtilsCnpjTest:
    def test_cnpj_format(self):
        utils = BrUtils()
        result = utils.cnpj.format("12345678000195")

        assert result == "12.345.678/0001-95"

    def test_cnpj_generate(self):
        utils = BrUtils()
        result = utils.cnpj.generate()

        assert len(result) == 14

    def test_cnpj_is_valid(self):
        utils = BrUtils()

        assert utils.cnpj.is_valid("11222333000181") is True
        assert utils.cnpj.is_valid("11111111111111") is False


class BrUtilsReexportsTest:
    def test_cpf_utils_reexports(self):
        from br_utils import (
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
        from br_utils import (
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
