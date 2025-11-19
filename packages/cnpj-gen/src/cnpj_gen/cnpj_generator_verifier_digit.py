from .exceptions import InvalidArgumentException

CNPJ_LENGTH = 14


class CnpjGeneratorVerifierDigit:
    def calculate(self, cnpj_sequence: list[int]) -> int:
        min_length = CNPJ_LENGTH - 2
        max_length = CNPJ_LENGTH - 1
        sequence_length = len(cnpj_sequence)

        if sequence_length < min_length or sequence_length > max_length:
            sequence_str = "".join(str(digit) for digit in cnpj_sequence)
            raise InvalidArgumentException(
                f'To calculate the verifier digit, the CNPJ sequence must be between {min_length} and {max_length} digits long, but got {sequence_length} digits ("{sequence_str}").'
            )

        factor = 2
        sum_result = 0

        for num in reversed(cnpj_sequence):
            sum_result += num * factor
            factor = 2 if factor == 9 else factor + 1

        remainder = sum_result % 11

        return 0 if remainder < 2 else 11 - remainder
