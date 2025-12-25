from cpf_fmt import CpfFormatterOptions
from cpf_gen import CpfGeneratorOptions
from cpf_utils import CpfUtils


class CpfUtilsInitTest:
    def test_init_with_defaults(self):
        utils = CpfUtils()

        assert utils.formatter is not None
        assert utils.generator is not None
        assert utils.validator is not None

    def test_init_with_formatter_options(self):
        formatter_options = CpfFormatterOptions(hidden=True, hidden_key="X")
        utils = CpfUtils(formatter=formatter_options)
        result = utils.format("12345678901")

        assert utils.formatter is not None
        assert utils.formatter.options == formatter_options
        assert result == "123.XXX.XXX-XX"

    def test_init_with_generator_options(self):
        generator_options = CpfGeneratorOptions(format=True, prefix="123456789")
        utils = CpfUtils(generator=generator_options)
        result = utils.generate()

        assert utils.generator is not None
        assert utils.generator.options == generator_options
        assert result.startswith("123.456.789-")
