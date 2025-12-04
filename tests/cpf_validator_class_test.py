from cpf_val import CpfValidator

from .cpf_validator_test_cases import CpfValidatorTestCases


class CpfValidatorClassTest(CpfValidatorTestCases):
    def setup_method(self):
        self.validator = CpfValidator()

    def is_valid(self, cpf_string: str) -> bool:
        if not hasattr(self, "validator"):
            self.setup_method()

        return self.validator.is_valid(cpf_string)
