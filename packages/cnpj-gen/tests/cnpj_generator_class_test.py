from cnpj_gen import CnpjGenerator, CnpjGeneratorOptions

from .cnpj_generator_test_cases import CnpjGeneratorTestCases


class CnpjGeneratorClassTest(CnpjGeneratorTestCases):
    def setup_method(self):
        self.generator = CnpjGenerator()

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        if not hasattr(self, "generator"):
            self.setup_method()

        return self.generator.generate(format, prefix)

    def test_object_oriented_get_options(self):
        if not hasattr(self, "generator"):
            self.setup_method()

        options = self.generator.options

        assert isinstance(options, CnpjGeneratorOptions)
        assert options.format is False
        assert options.prefix == ""
