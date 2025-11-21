import pytest

from .utils.external_cnpj_validator import ExternalCnpjValidator


class CnpjGeneratorTestCases:
    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        raise NotImplementedError

    def is_valid(self, cnpj_string: str) -> bool:
        validator = ExternalCnpjValidator()
        return validator.is_valid(cnpj_string)

    def test_result_length_equals_to_14_no_formatting(self):
        for _ in range(25):
            cnpj = self.generate()
            cnpj_size = len(cnpj)

            assert cnpj_size == 14, f"Input: {cnpj}, Expected: 14, Result: {cnpj_size}"

    def test_result_length_equals_to_18_with_formatting(self):
        for _ in range(25):
            cnpj = self.generate(True)
            cnpj_size = len(cnpj)

            assert cnpj_size == 18, f"Input: {cnpj}, Expected: 18, Result: {cnpj_size}"

    def test_generated_cnpj_is_valid_no_formatting(self):
        for _ in range(25):
            cnpj = self.generate()
            is_valid = self.is_valid(cnpj)

            assert is_valid, f"Input: {cnpj}, Expected: true"

    def test_generated_formatted_cnpj_is_valid_with_formatting(self):
        for _ in range(25):
            cnpj = self.generate(True)
            is_valid = self.is_valid(cnpj)

            assert is_valid, f"Input: {cnpj}, Expected: true"

    def test_generated_cnpj_is_valid_with_prefix(self):
        prefixes = [
            "1",
            "12",
            "123",
            "1234",
            "12345",
            "123456",
            "1234567",
            "12345678",
            "123456789",
            "1234567890",
            "12345678900",
            "123456789000",
            "123456780009",
            "12.345.678/0009",
        ]

        for prefix in prefixes:
            cnpj = self.generate(False, prefix)
            is_valid = self.is_valid(cnpj)

            assert is_valid, f"Input: {cnpj}, Expected: true"

    def test_formatted_cnpj_matches_pattern(self):
        import re

        pattern = r"(\d{2}).(\d{3}).(\d{3})/(\d{4})-(\d{2})"

        for _ in range(25):
            cnpj = self.generate(True)

            assert re.match(
                pattern, cnpj
            ), f"Input: {cnpj}, Expected: ##.###.###/####-##"

    def test_prefixed_value_cannot_accept_string_with_more_than_12_digits(self):
        from cnpj_gen import InvalidArgumentException

        with pytest.raises(InvalidArgumentException):
            self.generate(False, "12.345.678/0000-99")

        with pytest.raises(InvalidArgumentException):
            self.generate(False, "12345678000099")
