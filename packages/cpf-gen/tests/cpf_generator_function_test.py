from cpf_gen import cpf_gen

from .cpf_generator_test_cases import CpfGeneratorTestCases


class CpfGeneratorFunctionTest(CpfGeneratorTestCases):
    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return cpf_gen(format, prefix)
