from cpf_val import cpf_val

from .cpf_validator_test_cases import CpfValidatorTestCases


class CpfValidatorFunctionTest(CpfValidatorTestCases):
    def is_valid(self, cpf_string: str) -> bool:
        return cpf_val(cpf_string)
