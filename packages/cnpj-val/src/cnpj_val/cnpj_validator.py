from cnpj_gen import CnpjGeneratorVerifierDigit as CnpjVerifierDigit

CNPJ_LENGTH = 14


class CnpjValidator:
    __slots__ = ("_verifier_digit",)

    def __init__(self) -> None:
        self._verifier_digit = CnpjVerifierDigit()

    def is_valid(self, cnpj_string: str) -> bool:
        cnpj_numbers_string = "".join(filter(str.isdigit, cnpj_string))

        if len(cnpj_numbers_string) != CNPJ_LENGTH:
            return False

        cnpj_numbers_array = [int(digit) for digit in cnpj_numbers_string]

        if not self._validate_first_verifier_digit(cnpj_numbers_array):
            return False

        if not self._validate_second_verifier_digit(cnpj_numbers_array):
            return False

        return True

    def _validate_first_verifier_digit(self, cnpj_numbers_array: list[int]) -> bool:
        first_verifier_digit_index = CNPJ_LENGTH - 2
        provided_first_verifier_digit = cnpj_numbers_array[first_verifier_digit_index]
        base_first_verifier_digit_calculation = cnpj_numbers_array[
            :first_verifier_digit_index
        ]
        calculated_first_verifier_digit = self._verifier_digit.calculate(
            base_first_verifier_digit_calculation
        )

        return provided_first_verifier_digit == calculated_first_verifier_digit

    def _validate_second_verifier_digit(self, cnpj_numbers_array: list[int]) -> bool:
        second_verifier_digit_index = CNPJ_LENGTH - 1
        provided_second_verifier_digit = cnpj_numbers_array[second_verifier_digit_index]
        base_second_verifier_digit_calculation = cnpj_numbers_array[
            :second_verifier_digit_index
        ]
        calculated_second_verifier_digit = self._verifier_digit.calculate(
            base_second_verifier_digit_calculation
        )

        return provided_second_verifier_digit == calculated_second_verifier_digit
