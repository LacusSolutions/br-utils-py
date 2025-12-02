from cnpj_fmt import CnpjFormatterOptions
from cnpj_gen import CnpjGeneratorOptions
from cnpj_utils import CnpjUtils


class CnpjUtilsInitTest:
    def test_init_with_defaults(self):
        utils = CnpjUtils()

        assert utils.formatter is not None
        assert utils.generator is not None
        assert utils.validator is not None

    def test_init_with_formatter_options(self):
        formatter_options = CnpjFormatterOptions(hidden=True, hidden_key="X")
        utils = CnpjUtils(formatter=formatter_options)
        result = utils.format("12345678000190")

        assert utils.formatter is not None
        assert utils.formatter.options == formatter_options
        assert result == "12.345.XXX/XXXX-XX"

    def test_init_with_generator_options(self):
        generator_options = CnpjGeneratorOptions(format=True, prefix="12345678")
        utils = CnpjUtils(generator=generator_options)
        result = utils.generate()

        assert utils.generator is not None
        assert utils.generator.options == generator_options
        assert result.startswith("12.345.678/000")
