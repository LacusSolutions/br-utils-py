from cnpj_gen import CnpjGeneratorVerifierDigit

CNPJ_LENGTH = 14


class CnpjValidator:
    def __init__(self):
        self.verifier_digit = CnpjGeneratorVerifierDigit()

    def is_valid(self, _cnpj_string: str) -> bool:
        return False
