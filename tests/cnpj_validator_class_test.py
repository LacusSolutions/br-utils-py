from cnpj_val import CnpjValidator

from .cnpj_validator_test_cases import CnpjValidatorTestCases


class CnpjValidatorClassTest(CnpjValidatorTestCases):
    def setup_method(self):
        self.validator = CnpjValidator()

    def is_valid(self, cnpj_string: str) -> bool:
        if not hasattr(self, "validator"):
            self.setup_method()

        return self.validator.is_valid(cnpj_string)
