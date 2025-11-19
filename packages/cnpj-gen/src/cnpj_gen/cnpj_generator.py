from .cnpj_generator_options import CnpjGeneratorOptions
from .cnpj_generator_verifier_digit import CnpjGeneratorVerifierDigit


class CnpjGenerator:
    def __init__(self, format: bool | None = None, prefix: str | None = None):
        self._verifier_digit = CnpjGeneratorVerifierDigit()
        self._options = CnpjGeneratorOptions(format, prefix)

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return ""

    def get_options(self) -> CnpjGeneratorOptions:
        return self._options
