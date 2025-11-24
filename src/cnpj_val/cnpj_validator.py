from cnpj_cd import CnpjCheckDigits

CNPJ_LENGTH = 14


class CnpjValidator:
    def is_valid(self, cnpj_string: str) -> bool:
        cnpj_str_digits = "".join(filter(str.isdigit, cnpj_string))

        if len(cnpj_str_digits) != CNPJ_LENGTH:
            return False

        cnpj_num_digits = [int(digit) for digit in cnpj_str_digits]
        cnpj_first_check_digit = cnpj_num_digits[-2]
        cnpj_second_check_digit = cnpj_num_digits[-1]
        cnpj_check_digits = CnpjCheckDigits(cnpj_num_digits)

        if cnpj_first_check_digit != cnpj_check_digits.first_digit:
            return False

        if cnpj_second_check_digit != cnpj_check_digits.second_digit:
            return False

        return True
