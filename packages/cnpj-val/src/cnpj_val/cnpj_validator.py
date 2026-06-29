from cnpj_dv import CnpjCheckDigits
from cnpj_dv.exceptions import CnpjCheckDigitsException

CNPJ_LENGTH = 14


class CnpjValidator:
    """Class to validate a CNPJ string."""

    def is_valid(self, cnpj_string: str) -> bool:
        """Executes the CNPJ validation, returning a boolean value."""
        cnpj_str_digits = "".join(filter(str.isdigit, cnpj_string))

        if len(cnpj_str_digits) != CNPJ_LENGTH:
            return False

        try:
            cnpj_check_digits = CnpjCheckDigits(cnpj_str_digits)
        except CnpjCheckDigitsException:
            return False

        return cnpj_str_digits == cnpj_check_digits.cnpj
