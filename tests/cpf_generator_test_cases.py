from abc import ABC, abstractmethod

import pytest
from cpf_gen import CpfGeneratorPrefixLengthError

from .utils.external_cpf_validator import ExternalCpfValidator


class CpfGeneratorTestCases(ABC):
    @abstractmethod
    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        pass

    def is_valid(self, cpf_string: str) -> bool:
        return ExternalCpfValidator().is_valid(cpf_string)

    def test_result_length_equals_to_11_no_formatting(self):
        for _ in range(25):
            cpf = self.generate()
            cpf_size = len(cpf)

            assert cpf_size == 11, f"Input: {cpf}, Expected: 11, Result: {cpf_size}"

    def test_result_length_equals_to_14_with_formatting(self):
        for _ in range(25):
            cpf = self.generate(True)
            cpf_size = len(cpf)

            assert cpf_size == 14, f"Input: {cpf}, Expected: 14, Result: {cpf_size}"

    def test_generated_cpf_is_valid_no_formatting(self):
        for _ in range(25):
            cpf = self.generate()
            is_valid = self.is_valid(cpf)

            assert is_valid, f"Input: {cpf}, Expected: true"

    def test_generated_formatted_cpf_is_valid_with_formatting(self):
        for _ in range(25):
            cpf = self.generate(True)
            is_valid = self.is_valid(cpf)

            assert is_valid, f"Input: {cpf}, Expected: true"

    def test_generated_cpf_is_valid_with_prefix(self):
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
            "123.456.789",
        ]

        for prefix in prefixes:
            cpf = self.generate(False, prefix)
            is_valid = self.is_valid(cpf)

            assert is_valid, f"Input: {cpf}, Expected: true"

    def test_formatted_cpf_matches_pattern(self):
        import re

        pattern = r"(\d{3}).(\d{3}).(\d{3})-(\d{2})"

        for _ in range(25):
            cpf = self.generate(True)

            assert re.match(pattern, cpf), f"Input: {cpf}, Expected: ###.###.###-##"

    def test_prefixed_value_cannot_accept_string_with_more_than_9_digits(self):
        with pytest.raises(CpfGeneratorPrefixLengthError):
            self.generate(False, "1234567890")

        with pytest.raises(CpfGeneratorPrefixLengthError):
            self.generate(False, "123.456.789-0")
