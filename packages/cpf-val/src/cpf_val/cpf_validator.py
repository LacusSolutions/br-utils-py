from cpf_dv import CpfCheckDigits

CPF_LENGTH = 11


class CpfValidator:
    """Class to validate a CPF string."""

    def is_valid(self, cpf_string: str) -> bool:
        """Executes the CPF validation, returning a boolean value."""
        sanitized_cpf = "".join(filter(str.isdigit, cpf_string))

        if len(sanitized_cpf) != CPF_LENGTH:
            return False

        try:
            cpf_check_digits = CpfCheckDigits(sanitized_cpf)
        except Exception:
            return False

        return sanitized_cpf == cpf_check_digits.cpf
