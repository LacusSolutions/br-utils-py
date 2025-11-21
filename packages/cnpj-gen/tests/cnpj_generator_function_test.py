from cnpj_gen import cnpj_gen

from .cnpj_generator_test_cases import CnpjGeneratorTestCases


class CnpjGeneratorFunctionTest(CnpjGeneratorTestCases):
    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return cnpj_gen(format, prefix)
