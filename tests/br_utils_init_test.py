"""Unit tests for br-utils."""

import pytest
from br_utils import BrUtils, br_utils
from br_utils.cnpj import CnpjFormatterOptions, CnpjGeneratorOptions
from br_utils.cpf import CpfFormatterOptions, CpfGeneratorOptions


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

    def test_init_with_cpf_formatter_options(self):
        formatter_options = CpfFormatterOptions(hidden=True, hidden_key="X")
        utils = BrUtils(cpf_formatter=formatter_options)
        result = utils.cpf.format("12345678901")

        assert utils.cpf.formatter is not None
        assert utils.cpf.formatter.options == formatter_options
        assert result == "123.XXX.XXX-XX"

    def test_init_with_cpf_generator_options(self):
        generator_options = CpfGeneratorOptions(format=True, prefix="123456789")
        utils = BrUtils(cpf_generator=generator_options)
        result = utils.cpf.generate()

        assert utils.cpf.generator is not None
        assert utils.cpf.generator.options == generator_options
        assert result.startswith("123.456.789-")

    def test_init_with_cnpj_formatter_options(self):
        formatter_options = CnpjFormatterOptions(hidden=True, hidden_key="X")
        utils = BrUtils(cnpj_formatter=formatter_options)
        result = utils.cnpj.format("11222333000181")

        assert utils.cnpj.formatter is not None
        assert utils.cnpj.formatter.options == formatter_options
        assert result == "11.222.XXX/XXXX-XX"

    def test_init_with_cnpj_generator_options(self):
        generator_options = CnpjGeneratorOptions(format=True, prefix="11222333")
        utils = BrUtils(cnpj_generator=generator_options)
        result = utils.cnpj.generate()

        assert utils.cnpj.generator is not None
        assert utils.cnpj.generator.options == generator_options
        assert result.startswith("11.222.333/")

    def test_init_with_all_options(self):
        cpf_fmt_opts = CpfFormatterOptions(hidden=True)
        cpf_gen_opts = CpfGeneratorOptions(format=True)
        cnpj_fmt_opts = CnpjFormatterOptions(hidden=True)
        cnpj_gen_opts = CnpjGeneratorOptions(format=True)

        utils = BrUtils(
            cpf_formatter=cpf_fmt_opts,
            cpf_generator=cpf_gen_opts,
            cnpj_formatter=cnpj_fmt_opts,
            cnpj_generator=cnpj_gen_opts,
        )

        assert utils.cpf.formatter.options == cpf_fmt_opts
        assert utils.cpf.generator.options == cpf_gen_opts
        assert utils.cnpj.formatter.options == cnpj_fmt_opts
        assert utils.cnpj.generator.options == cnpj_gen_opts
