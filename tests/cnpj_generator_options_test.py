import pytest
from cnpj_gen import CnpjGeneratorOptions, InvalidArgumentException


class CnpjGeneratorOptionsTest:
    def test_constructor_with_no_params(self):
        options = CnpjGeneratorOptions()

        assert options.is_formatting() is False
        assert options.get_prefix() == ""

    def test_constructor_with_all_null_params(self):
        options = CnpjGeneratorOptions(None, None)

        assert options.is_formatting() is False
        assert options.get_prefix() == ""

    def test_constructor_with_all_params(self):
        options = CnpjGeneratorOptions(True, "12345678")

        assert options.is_formatting() is True
        assert options.get_prefix() == "12345678"

    def test_constructor_with_mixed_null_and_valid_values(self):
        options = CnpjGeneratorOptions(True, None)

        assert options.is_formatting() is True
        assert options.get_prefix() == ""

    def test_merge_returns_new_instance(self):
        original_options = CnpjGeneratorOptions()
        merged_options = original_options.merge()

        assert merged_options is not original_options
        assert isinstance(merged_options, CnpjGeneratorOptions)

    def test_merge_with_all_nulls_preserves_original_values(self):
        original_options = CnpjGeneratorOptions(True, "333666")

        merged_options = original_options.merge(None, None)

        assert merged_options.is_formatting() is True
        assert merged_options.get_prefix() == "333666"

    def test_merge_with_partial_overrides(self):
        original_options = CnpjGeneratorOptions(True, "1234")

        merged_options = original_options.merge(None, "111222333")

        assert merged_options.is_formatting() is True
        assert merged_options.get_prefix() == "111222333"

    def test_set_format(self):
        options = CnpjGeneratorOptions()

        options.set_format(True)
        assert options.is_formatting() is True

        options.set_format(False)
        assert options.is_formatting() is False

    def test_set_prefix_with_few_digits(self):
        options = CnpjGeneratorOptions()

        options.set_prefix("12345")
        assert options.get_prefix() == "12345"

        options.set_prefix("8888")
        assert options.get_prefix() == "8888"

    def test_set_prefix_with_non_numeric_chars(self):
        options = CnpjGeneratorOptions()

        options.set_prefix("123acb")
        assert options.get_prefix() == "123"

        options.set_prefix("This is a test")
        assert options.get_prefix() == ""

    def test_set_prefix_throws_error_with_too_many_digits(self):
        options = CnpjGeneratorOptions()

        with pytest.raises(InvalidArgumentException) as exc_info:
            options.set_prefix("12345678000910")
        assert (
            'Option "prefix" must be a string containing between 0 and 12 digits.'
            in str(exc_info.value)
        )

    def test_set_prefix_throws_error_with_invalid_branch_id(self):
        options = CnpjGeneratorOptions()

        with pytest.raises(InvalidArgumentException) as exc_info:
            options.set_prefix("123456780000")
        assert 'The branch ID (characters 8 to 11) cannot be "0000".' in str(
            exc_info.value
        )
