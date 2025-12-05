import pytest
from cpf_gen import (
    CpfGeneratorOptions,
    CpfGeneratorPrefixLengthError,
    CpfGeneratorPrefixNotValidError,
)


class CpfGeneratorOptionsTest:
    def test_constructor_with_no_params(self):
        options = CpfGeneratorOptions()

        assert options.format is False
        assert options.prefix == ""

    def test_constructor_with_all_none_params(self):
        options = CpfGeneratorOptions(
            format=None,
            prefix=None,
        )

        assert options.format is False
        assert options.prefix == ""

    def test_constructor_with_all_params(self):
        options = CpfGeneratorOptions(
            format=True,
            prefix="123456",
        )

        assert options.format is True
        assert options.prefix == "123456"

    def test_constructor_with_mixed_none_and_valid_values(self):
        options = CpfGeneratorOptions(
            format=True,
            prefix=None,
        )

        assert options.format is True
        assert options.prefix == ""

    def test_constructor_throws_error_on_prefix_too_long(self):
        with pytest.raises(CpfGeneratorPrefixLengthError) as exc_info:
            CpfGeneratorOptions(prefix="1234567890")

        assert "The prefix length must be less than or equal to 9. Got 10." in str(
            exc_info.value
        )

    def test_constructor_throws_error_on_prefix_with_repeated_digits(self):
        invalid_prefixes = [
            "111111111",
            "222222222",
            "333333333",
            "444444444",
            "555555555",
        ]

        for prefix in invalid_prefixes:
            with pytest.raises(CpfGeneratorPrefixNotValidError) as exc_info:
                CpfGeneratorOptions(prefix=prefix)

            assert f"{prefix}" in str(exc_info.value)
            assert "Repeated digits are not considered valid." in str(exc_info.value)

    def test_merge_returns_new_instance(self):
        original_options = CpfGeneratorOptions()
        merged_options = original_options.merge()

        assert merged_options is not original_options
        assert isinstance(merged_options, CpfGeneratorOptions)

    def test_merge_with_all_nulls_preserves_original_values(self):
        original_options = CpfGeneratorOptions(
            format=True,
            prefix="123456789",
        )

        merged_options = original_options.merge(
            format=None,
            prefix=None,
        )

        assert merged_options.format is True
        assert merged_options.prefix == "123456789"

    def test_merge_with_partial_overrides(self):
        original_options = CpfGeneratorOptions(
            format=True,
            prefix="1234",
        )

        merged_options = original_options.merge(
            format=None,
            prefix="111222333",
        )

        assert merged_options.format is True
        assert merged_options.prefix == "111222333"

    def test_format_setter(self):
        options = CpfGeneratorOptions()

        options.format = True
        assert options.format is True

        options.format = False
        assert options.format is False

    def test_prefix_setter_with_few_digits(self):
        options = CpfGeneratorOptions()

        options.prefix = "11111"
        assert options.prefix == "11111"

        options.prefix = "55555"
        assert options.prefix == "55555"

    def test_prefix_setter_with_non_numeric_chars(self):
        options = CpfGeneratorOptions()

        options.prefix = "123acb"
        assert options.prefix == "123"

        options.prefix = "This is a test"
        assert options.prefix == ""

    def test_prefix_setter_throws_error_with_too_many_digits(self):
        options = CpfGeneratorOptions()

        with pytest.raises(CpfGeneratorPrefixLengthError) as exc_info:
            options.prefix = "1234567890"

        assert "The prefix length must be less than or equal to 9. Got 10." in str(
            exc_info.value
        )

    def test_prefix_setter_throws_error_with_repeated_digits(self):
        invalid_prefixes = [
            "111111111",
            "222222222",
            "333333333",
            "444444444",
            "555555555",
            "666666666",
            "777777777",
            "888888888",
            "999999999",
            "000000000",
        ]

        for prefix in invalid_prefixes:
            options = CpfGeneratorOptions()

            with pytest.raises(CpfGeneratorPrefixNotValidError) as exc_info:
                options.prefix = prefix

            assert f"{prefix}" in str(exc_info.value)
            assert "Repeated digits are not considered valid." in str(exc_info.value)
