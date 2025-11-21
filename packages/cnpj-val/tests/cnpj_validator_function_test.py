from cnpj_val import cnpj_val

from .cnpj_validator_test_cases import CnpjValidatorTestCases


class CnpjValidatorFunctionTest(CnpjValidatorTestCases):
    def is_valid(self, cnpj_string: str) -> bool:
        return cnpj_val(cnpj_string)
