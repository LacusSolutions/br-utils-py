import re

from cnpj_gen import CnpjGeneratorVerifierDigit

CNPJ_LENGTH = 14


class CnpjValidator:
    def __init__(self):
        self.verifier_digit = CnpjGeneratorVerifierDigit()

    def is_valid(self, cnpj_string: str) -> bool:
        cnpj_numbers_string = re.sub(r"[^0-9]", "", cnpj_string)
        cnpj_numbers_array = [int(digit) for digit in cnpj_numbers_string]

        if len(cnpj_numbers_array) != CNPJ_LENGTH:
            return False

        first_verifier_digit_index = CNPJ_LENGTH - 2
        provided_first_verifier_digit = cnpj_numbers_array[first_verifier_digit_index]
        base_first_verifier_digit_calculation = cnpj_numbers_array[
            :first_verifier_digit_index
        ]
        calculated_first_verifier_digit = self.verifier_digit.calculate(
            base_first_verifier_digit_calculation
        )

        if provided_first_verifier_digit != calculated_first_verifier_digit:
            return False

        second_verifier_digit_index = CNPJ_LENGTH - 1
        base_second_verifier_digit_calculation = cnpj_numbers_array[
            :second_verifier_digit_index
        ]
        provided_second_verifier_digit = cnpj_numbers_array[second_verifier_digit_index]
        calculated_second_verifier_digit = self.verifier_digit.calculate(
            base_second_verifier_digit_calculation
        )

        if provided_second_verifier_digit != calculated_second_verifier_digit:
            return False

        return True
