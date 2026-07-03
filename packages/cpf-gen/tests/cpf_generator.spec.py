"""Behavioral spec for ``CpfGenerator``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-gen/tests/cpf-generator.spec.ts``) and the PHP reference
suite (``php/packages/cpf-gen/tests/CpfGeneratorTestCases.php`` and
``CpfGeneratorClassTest.php``), following the business rules documented in
``AGENTS.md``.

Dropped cases:
- ``undefined`` option values (JavaScript-only; Python uses ``None``).
- ``js/packages/cpf-gen/tests/output.spec.ts`` (UMD/CJS/ESM distribution
  artifacts; not applicable to the Python package layout).
- PHP ``CpfGeneratorVerifierDigitTest`` (internal verifier class; Python
  delegates to ``cpf-dv`` per ``AGENTS.md`` §9.2).
- PHP external CPF validation via ``ExternalCpfValidator`` (replaced by
  structural assertions from the JS suite: length, regex, uniqueness).
- PHP prefix >9 digit ``InvalidArgumentException`` (JS truncates silently;
  canonical behavior per ``AGENTS.md`` §8 #6).
"""

import re
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest
from cpf_gen import (
    CpfGenerator,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
    CpfGeneratorOptionsTypeError,
)

GenerateFn = Callable[..., str]
GeneratorFactory = Callable[[dict[str, Any]], GenerateFn]

PREFIX_CASES = [
    "1",
    "12",
    "123",
    "1234",
    "12345",
    "123456",
    "1234567",
    "12345678",
    "123456789",
]


def _default_options_snapshot() -> dict:
    return CpfGeneratorOptions().all


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def _create_generator_with_literal_in_constructor(
    options: dict[str, Any],
) -> GenerateFn:
    generator = CpfGenerator(options)

    def generate(options_override=None) -> str:
        return generator.generate(options_override)

    return generate


def _create_generator_with_options_instance_in_constructor(
    options: dict[str, Any],
) -> GenerateFn:
    generator_options = CpfGeneratorOptions(options)
    generator = CpfGenerator(generator_options)

    def generate(options_override=None) -> str:
        return generator.generate(options_override)

    return generate


def _create_generator_with_literal_in_method(options: dict[str, Any]) -> GenerateFn:
    generator = CpfGenerator()

    def generate(options_override=None) -> str:
        if options_override is None:
            return generator.generate(options)
        if isinstance(options_override, CpfGeneratorOptions):
            return generator.generate(
                CpfGeneratorOptions(options, options_override),
            )
        return generator.generate({**options, **options_override})

    return generate


def _create_generator_with_options_instance_in_method(
    options: dict[str, Any],
) -> GenerateFn:
    generator = CpfGenerator()

    def generate(options_override=None) -> str:
        generator_options = CpfGeneratorOptions(
            options,
            options_override if options_override is not None else {},
        )
        return generator.generate(generator_options)

    return generate


def _unique_result_count(generate: GenerateFn, count: int = 100, **kwargs) -> int:
    return len({generate(**kwargs) for _ in range(count)})


def _assert_unformatted_defaults(generate: GenerateFn) -> None:
    for _ in range(100):
        result = generate()

        assert len(result) == 11
        assert not re.search(r"[a-z]", result)
        assert not re.search(r"[./-]", result)
        assert re.fullmatch(r"\d+", result)


def _assert_formatted_defaults(generate: GenerateFn) -> None:
    for _ in range(100):
        result = generate()

        assert len(result) == 14
        assert not re.search(r"[a-z]", result)
        assert re.search(r"[./-]", result)
        assert re.search(r"\d{2,3}", result)


def _assert_formatted_mask(generate: GenerateFn) -> None:
    for _ in range(100):
        result = generate()

        assert re.fullmatch(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", result)


GENERATOR_FACTORIES = [
    pytest.param(
        _create_generator_with_literal_in_constructor,
        id="constructor_literal",
    ),
    pytest.param(
        _create_generator_with_options_instance_in_constructor,
        id="constructor_options",
    ),
    pytest.param(
        _create_generator_with_literal_in_method,
        id="method_literal",
    ),
    pytest.param(
        _create_generator_with_options_instance_in_method,
        id="method_options",
    ),
]


def describe_cpf_generator():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_default_options():
                generator = CpfGenerator()

                _assert_options_snapshots_match(
                    generator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_an_empty_object():
            def it_creates_an_instance_with_default_options():
                generator = CpfGenerator({})

                _assert_options_snapshots_match(
                    generator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_a_cpf_generator_options_instance():
            def it_uses_that_instance_directly_without_copying():
                options = CpfGeneratorOptions(
                    {
                        "format": True,
                        "prefix": "123456",
                    }
                )
                generator = CpfGenerator(options)

                assert generator.options is options
                _assert_options_snapshots_match(
                    generator.options.all,
                    options.all,
                )

            def it_mutations_to_the_instance_affect_future_generate_calls():
                options = CpfGeneratorOptions(
                    {
                        "prefix": "123456",
                        "format": True,
                    }
                )
                generator = CpfGenerator(options)
                options.prefix = "112233"
                options.format = False

                result = generator.generate()

                assert len(result) == 11
                assert re.fullmatch(r"^112233\d{5}$", result)

        def describe_when_called_with_a_literal_options_object():
            def it_creates_a_new_cpf_generator_options_instance_from_the_provided_values():
                input_options = {
                    "format": True,
                    "prefix": "123456",
                }
                generator = CpfGenerator(input_options)

                assert isinstance(generator.options, CpfGeneratorOptions)
                assert generator.options.format is True
                assert generator.options.prefix == "123456"

        def describe_when_called_with_invalid_options():
            def it_throws_cpf_generator_option_prefix_invalid_exception_for_invalid_prefix():
                with pytest.raises(CpfGeneratorOptionPrefixInvalidException):
                    CpfGenerator({"prefix": "000000000"})

            def it_throws_cpf_generator_options_type_error_for_non_string_prefix():
                with pytest.raises(CpfGeneratorOptionsTypeError):
                    CpfGenerator({"prefix": 123})  # type: ignore[dict-item]

    def describe_generate_method():
        def describe_when_no_options_are_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_an_11_digit_string_with_only_numbers(create_generator):
                generate = create_generator({})

                _assert_unformatted_defaults(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_different_values_on_successive_calls(create_generator):
                generate = create_generator({})

                assert _unique_result_count(generate) >= 99

        def describe_when_format_option_is_true():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_a_14_character_string_with_numbers_and_punctuation(
                create_generator,
            ):
                generate = create_generator({"format": True})

                _assert_formatted_defaults(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_a_string_with_standard_cpf_formatting(create_generator):
                generate = create_generator({"format": True})

                _assert_formatted_mask(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_different_values_on_successive_calls(create_generator):
                generate = create_generator({"format": True})

                assert _unique_result_count(generate) >= 99

        def describe_when_prefix_option_is_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize("prefix", PREFIX_CASES)
            def it_returns_an_11_digit_string_with_prefix(create_generator, prefix):
                generate = create_generator({"prefix": prefix})

                for _ in range(100):
                    result = generate()

                    assert len(result) == 11
                    assert re.fullmatch(r"\d+", result)
                    assert result.startswith(prefix)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_ignores_characters_after_the_9th_position(create_generator):
                generate = create_generator({"prefix": "12345678910"})

                result = generate()

                assert len(result) == 11
                assert not result.endswith("10")
                assert re.fullmatch(r"^123456789\d{2}$", result)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_always_generates_the_same_cpf_with_the_same_9_digit_prefix(
                create_generator,
            ):
                generate = create_generator({"prefix": "987654321"})

                assert len({generate() for _ in range(100)}) == 1

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_strips_non_numeric_characters_from_prefix_before_generating(
                create_generator,
            ):
                generate = create_generator(
                    {"prefix": "ABC.123.DEF.456.GHI.789", "format": False},
                )

                result = generate()

                assert result.startswith("123456789")

        def describe_when_different_options_are_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_a_14_character_cpf_when_format_true_and_prefix_12345678(
                create_generator,
            ):
                generate = create_generator(
                    {"format": True, "prefix": "12345678"},
                )

                result = generate()

                assert len(result) == 14
                assert not re.search(r"[a-z]", result)
                assert re.fullmatch(r"^123\.456\.78\d-\d{2}$", result)

        def describe_when_cpf_check_digits_throws_an_exception():
            def it_retries_generation_and_returns_a_valid_cpf():
                with patch(
                    "cpf_gen.cpf_generator.generate_random_sequence",
                ) as mock_sequence:
                    mock_sequence.side_effect = ["111111111", "123456789"]

                    result = CpfGenerator().generate()

                    assert len(result) == 11
                    assert result.startswith("123456789")
                    assert mock_sequence.call_count == 2

            def it_uses_the_same_options_on_retry():
                with patch(
                    "cpf_gen.cpf_generator.generate_random_sequence",
                ) as mock_sequence:
                    mock_sequence.side_effect = ["111111", "222333"]

                    result = CpfGenerator(
                        {"prefix": "111", "format": True},
                    ).generate()

                    assert len(result) == 14
                    assert result.startswith("111.222.333-")
                    assert mock_sequence.call_count == 2
                    mock_sequence.assert_any_call(6, "numeric")
                    assert mock_sequence.call_args_list == [
                        ((6, "numeric"),),
                        ((6, "numeric"),),
                    ]
