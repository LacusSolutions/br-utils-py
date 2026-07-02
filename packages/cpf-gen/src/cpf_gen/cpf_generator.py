import random

from cpf_dv import CpfCheckDigits
from cpf_dv.exceptions import CpfCheckDigitsException

from .cpf_generator_options import PREFIX_MAX_LENGTH, CpfGeneratorOptions


class CpfGenerator:
    """Class to generate a valid CPF according to the given options."""

    __slots__ = "_options"

    def __init__(self, format: bool | None = None, prefix: str | None = None):
        self._options = CpfGeneratorOptions(format, prefix)

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        """Executes the CPF generation, overriding any given options with the ones set on the generator instance."""
        actual_options = self._options.merge(format, prefix)

        digits_to_generate = PREFIX_MAX_LENGTH - len(actual_options.prefix)
        generated_cpf = actual_options.prefix + self._generate_random_digits(
            digits_to_generate
        )

        try:
            generated_cpf = CpfCheckDigits(generated_cpf).cpf
        except CpfCheckDigitsException:
            return self.generate(format, prefix)

        if actual_options.format:
            return self._format(generated_cpf)

        return generated_cpf

    def _generate_random_digits(self, count: int) -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(count))

    def _format(self, cpf_string: str) -> str:
        return (
            f"{cpf_string[0:3]}.{cpf_string[3:6]}.{cpf_string[6:9]}-{cpf_string[9:11]}"
        )

    @property
    def options(self) -> CpfGeneratorOptions:
        """Direct access to the options manager for the CPF generator."""
        return self._options
