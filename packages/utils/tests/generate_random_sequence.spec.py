import re

import pytest
from lacus.utils import generate_random_sequence


def describe_generate_random_sequence():
    def describe_when_generating_numeric_sequences():
        @pytest.mark.parametrize("_", range(20))
        def it_generates_sequences_of_the_correct_length(_):
            result = generate_random_sequence(32, "numeric")
            assert len(result) == 32

        @pytest.mark.parametrize("_", range(50))
        def it_only_contains_digits(_):
            result = generate_random_sequence(100, "numeric")
            assert re.fullmatch(r"\d+", result)

    def describe_when_generating_alphabetic_sequences():
        @pytest.mark.parametrize("_", range(20))
        def it_generates_sequences_of_the_correct_length(_):
            result = generate_random_sequence(32, "alphabetic")
            assert len(result) == 32

        @pytest.mark.parametrize("_", range(50))
        def it_only_contains_uppercase_letters(_):
            result = generate_random_sequence(100, "alphabetic")
            assert re.fullmatch(r"[A-Z]+", result)

        @pytest.mark.parametrize("_", range(50))
        def it_does_not_contain_digits(_):
            result = generate_random_sequence(100, "alphabetic")
            assert not re.search(r"\d", result)

    def describe_when_generating_alphanumeric_sequences():
        @pytest.mark.parametrize("_", range(20))
        def it_generates_sequences_of_the_correct_length(_):
            result = generate_random_sequence(32, "alphanumeric")
            assert len(result) == 32

        @pytest.mark.parametrize("_", range(50))
        def it_only_contains_digits_and_uppercase_letters(_):
            result = generate_random_sequence(100, "alphanumeric")
            assert re.fullmatch(r"[0-9A-Z]+", result)

        @pytest.mark.parametrize("_", range(50))
        def it_does_not_contain_lowercase_letters(_):
            result = generate_random_sequence(100, "alphanumeric")
            assert not re.search(r"[a-z]", result)

    def describe_edge_cases():
        def it_returns_an_empty_string_for_size_zero():
            assert generate_random_sequence(0, "numeric") == ""
            assert generate_random_sequence(0, "alphabetic") == ""
            assert generate_random_sequence(0, "alphanumeric") == ""

    def describe_validation():
        def it_raises_value_error_for_negative_size():
            with pytest.raises(ValueError, match="size must be non-negative"):
                generate_random_sequence(-1, "numeric")
