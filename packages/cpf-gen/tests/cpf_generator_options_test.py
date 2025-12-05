import pytest
from cpf_gen import CpfGeneratorOptions, CpfGeneratorPrefixLengthError


class CpfGeneratorOptionsTest:
    def test_constructor_with_no_params(self):
        options = CpfGeneratorOptions()

        assert options.format is False
        assert options.prefix == ""

    def test_constructor_with_all_null_params(self):
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

    def test_constructor_with_mixed_null_and_valid_values(self):
        options = CpfGeneratorOptions(
            format=True,
            prefix=None,
        )

        assert options.format is True
        assert options.prefix == ""

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
