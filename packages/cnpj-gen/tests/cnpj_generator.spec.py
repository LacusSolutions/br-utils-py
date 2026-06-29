"""Behavioral spec for ``CnpjGenerator``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-gen/tests/cnpj-generator.spec.ts``) and the PHP reference
suite (``php/packages/cnpj-gen/tests/specs/CnpjGenerator.spec.php``), plus the
process-isolation retry cases from
``php/packages/cnpj-gen/tests/specs/CnpjGenerator.isolated.spec.php``, following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` option values (JavaScript-only; Python uses ``None``).
- ``js/packages/cnpj-gen/tests/output.spec.ts`` (UMD/CJS/ESM distribution
  artifacts; not applicable to the Python package layout).
"""

import re
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
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
    "1234567890",
    "12345678910",
    "123456780009",
    "A",
    "AB",
    "ABC",
    "ABCD",
    "ABCDE",
    "ABCDEF",
    "ABCDEFG",
    "ABCDEFGH",
    "ABCDEFGHI",
    "ABCDEFGHIJ",
    "ABCDEFGHIJK",
    "ABCDEFGHIJKL",
    "AB123CDE0001",
]

TRUNCATION_PREFIX_CASES = [
    ("numeric", "123456780009"),
    ("alphabetic", "ABCDEFGHIJKL"),
    ("alphanumeric", "AB123CDE0001"),
]

TYPE_CONTEXTS = [
    ("numeric", r"\d"),
    ("alphabetic", r"[A-Z]"),
    ("alphanumeric", r"[0-9A-Z]"),
]


def _default_options_snapshot() -> dict:
    return CnpjGeneratorOptions().all


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def _create_generator_with_literal_in_constructor(
    options: dict[str, Any],
) -> GenerateFn:
    generator = CnpjGenerator(options)

    def generate(options_override=None) -> str:
        return generator.generate(options_override)

    return generate


def _create_generator_with_options_instance_in_constructor(
    options: dict[str, Any],
) -> GenerateFn:
    generator_options = CnpjGeneratorOptions(options)
    generator = CnpjGenerator(generator_options)

    def generate(options_override=None) -> str:
        return generator.generate(options_override)

    return generate


def _create_generator_with_literal_in_method(options: dict[str, Any]) -> GenerateFn:
    generator = CnpjGenerator()

    def generate(options_override=None) -> str:
        if options_override is None:
            return generator.generate(options)
        if isinstance(options_override, CnpjGeneratorOptions):
            return generator.generate(
                CnpjGeneratorOptions(options, options_override),
            )
        return generator.generate({**options, **options_override})

    return generate


def _create_generator_with_options_instance_in_method(
    options: dict[str, Any],
) -> GenerateFn:
    generator = CnpjGenerator()

    def generate(options_override=None) -> str:
        generator_options = CnpjGeneratorOptions(
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

        assert len(result) == 14
        assert not re.search(r"[a-z]", result)
        assert not re.search(r"[./-]", result)
        assert re.fullmatch(r"[0-9A-Z]+", result)


def _assert_check_digits_are_numeric(generate: GenerateFn, **kwargs) -> None:
    for _ in range(100):
        result = generate(**kwargs)

        assert re.search(r"\d{2}$", result)


def _assert_formatted_defaults(generate: GenerateFn) -> None:
    for _ in range(100):
        result = generate()

        assert len(result) == 18
        assert not re.search(r"[a-z]", result)
        assert re.search(r"[./-]", result)
        assert re.search(r"[0-9A-Z]{2,4}", result)


def _assert_formatted_mask(generate: GenerateFn) -> None:
    for _ in range(100):
        result = generate()

        assert re.fullmatch(
            r"^[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-[0-9A-Z]{2}$",
            result,
            flags=re.IGNORECASE,
        )


def _assert_type_pattern(generate: GenerateFn, pattern: str, **kwargs) -> None:
    for _ in range(100):
        result = generate(**kwargs)

        assert len(result) == 14
        assert not re.search(r"[a-z]", result)
        assert not re.search(r"[./-]", result)
        assert re.fullmatch(rf"^{pattern}{{12}}\d{{2}}$", result)


class _CnpjGeneratorCallsSpy(CnpjGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls_count = 0
        self.calls_arguments: list[tuple[Any, dict[str, Any]]] = []

    def generate(self, options=None, **kwargs) -> str:
        self.calls_count += 1
        self.calls_arguments.append((options, kwargs))
        return super().generate(options, **kwargs)


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


def describe_cnpj_generator():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_default_options():
                generator = CnpjGenerator()

                _assert_options_snapshots_match(
                    generator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_an_empty_object():
            def it_creates_an_instance_with_default_options():
                generator = CnpjGenerator({})

                _assert_options_snapshots_match(
                    generator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_a_cnpj_generator_options_instance():
            def it_uses_that_instance_directly_without_copying():
                options = CnpjGeneratorOptions(
                    {
                        "format": True,
                        "prefix": "12345678",
                        "type": "numeric",
                    }
                )
                generator = CnpjGenerator(options)

                assert generator.options is options
                _assert_options_snapshots_match(
                    generator.options.all,
                    options.all,
                )

            def it_mutates_the_instance_and_affects_future_generate_calls():
                options = CnpjGeneratorOptions({"format": False, "type": "numeric"})
                generator = CnpjGenerator(options)

                options.format = True
                options.type = "alphabetic"

                assert generator.options.format is True
                assert generator.options.type == "alphabetic"

        def describe_when_called_with_a_literal_options_object():
            def it_creates_a_new_cnpj_generator_options_instance_from_the_provided_values():
                input_options = {
                    "format": True,
                    "prefix": "12345678",
                    "type": "numeric",
                }
                generator = CnpjGenerator(input_options)

                assert isinstance(generator.options, CnpjGeneratorOptions)
                assert generator.options.format is True
                assert generator.options.prefix == "12345678"
                assert generator.options.type == "numeric"

        def describe_when_called_with_invalid_options():
            def it_throws_cnpj_generator_option_prefix_invalid_exception_for_invalid_prefix():
                with pytest.raises(CnpjGeneratorOptionPrefixInvalidException):
                    CnpjGenerator({"prefix": "00000000"})

            def it_throws_cnpj_generator_option_type_invalid_exception_for_invalid_type():
                with pytest.raises(CnpjGeneratorOptionTypeInvalidException):
                    CnpjGenerator({"type": "invalid"})

            def it_throws_cnpj_generator_options_type_error_for_non_string_prefix():
                with pytest.raises(CnpjGeneratorOptionsTypeError):
                    CnpjGenerator({"prefix": 123})  # type: ignore[dict-item]

    def describe_generate_method():
        def describe_when_no_options_are_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_a_14_character_string_with_only_numbers_and_uppercase_letters(
                create_generator,
            ):
                generate = create_generator({})

                _assert_unformatted_defaults(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_contains_2_numeric_check_digits(create_generator):
                generate = create_generator({})

                _assert_check_digits_are_numeric(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_different_values_on_successive_calls(create_generator):
                generate = create_generator({})

                assert _unique_result_count(generate) >= 99

        def describe_when_format_option_is_true():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_an_18_character_string_with_numbers_uppercase_letters_and_punctuation(
                create_generator,
            ):
                generate = create_generator({"format": True})

                _assert_formatted_defaults(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_contains_2_numeric_check_digits(create_generator):
                generate = create_generator({"format": True})

                _assert_check_digits_are_numeric(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_a_string_with_standard_cnpj_formatting(create_generator):
                generate = create_generator({"format": True})

                _assert_formatted_mask(generate)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_different_values_on_successive_calls(create_generator):
                generate = create_generator({"format": True})

                assert _unique_result_count(generate) >= 99

        def describe_when_prefix_option_is_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize("prefix", PREFIX_CASES)
            def it_returns_a_14_character_string_with_prefix(create_generator, prefix):
                generate = create_generator({"prefix": prefix})

                for _ in range(100):
                    result = generate()

                    assert len(result) == 14
                    assert re.fullmatch(r"[0-9A-Z]+", result)
                    assert result.startswith(prefix)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("_type_name", "prefix"), TRUNCATION_PREFIX_CASES)
            def it_ignores_characters_after_the_12th_position(
                create_generator,
                _type_name,
                prefix,
            ):
                generate = create_generator({"prefix": f"{prefix}XY"})

                result = generate()

                assert len(result) == 14
                assert not result.endswith("XY")
                assert re.fullmatch(rf"^{re.escape(prefix)}\d{{2}}$", result)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("_type_name", "prefix"), TRUNCATION_PREFIX_CASES)
            def it_always_generates_the_same_cnpj_with_the_same_12_character_prefix(
                create_generator,
                _type_name,
                prefix,
            ):
                generate = create_generator({"prefix": prefix})

                assert len({generate({"prefix": prefix}) for _ in range(100)}) == 1

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_strips_non_alphanumeric_characters_from_prefix_before_generating(
                create_generator,
            ):
                generate = create_generator(
                    {"prefix": "AB.12.CDE/0001", "format": False},
                )

                result = generate()

                assert result.startswith("AB12CDE0001")

        def describe_when_type_option_is_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("type_name", "pattern"), TYPE_CONTEXTS)
            def it_returns_a_14_character_string(create_generator, type_name, pattern):
                generate = create_generator({"type": type_name})

                _assert_type_pattern(generate, pattern)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("type_name", "_pattern"), TYPE_CONTEXTS)
            def it_returns_different_values_on_successive_calls(
                create_generator,
                type_name,
                _pattern,
            ):
                generate = create_generator({"type": type_name})

                assert _unique_result_count(generate) >= 98

        def describe_when_different_options_are_passed():
            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            def it_returns_an_18_character_cnpj_when_format_true_and_prefix_ab123cde000(
                create_generator,
            ):
                generate = create_generator(
                    {"format": True, "prefix": "AB123CDE000"},
                )

                result = generate()

                assert len(result) == 18
                assert not re.search(r"[a-z]", result)
                assert re.fullmatch(r"^AB\.123\.CDE/000[0-9A-Z]-\d{2}$", result)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("type_name", "pattern"), TYPE_CONTEXTS)
            def it_returns_an_18_character_cnpj_when_format_true_and_type_set(
                create_generator,
                type_name,
                pattern,
            ):
                generate = create_generator({"format": True, "type": type_name})

                result = generate()

                assert len(result) == 18
                assert not re.search(r"[a-z]", result)
                assert re.fullmatch(
                    rf"^{pattern}{{2}}\.{pattern}{{3}}\.{pattern}{{3}}/{pattern}{{4}}-\d{{2}}$",
                    result,
                )

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("type_name", "pattern"), TYPE_CONTEXTS)
            def it_returns_a_14_character_cnpj_when_prefix_ab123cde_and_type_set(
                create_generator,
                type_name,
                pattern,
            ):
                generate = create_generator({"prefix": "AB123CDE", "type": type_name})

                result = generate()

                assert len(result) == 14
                assert not re.search(r"[a-z]", result)
                assert not re.search(r"[./-]", result)
                assert re.fullmatch(rf"^AB123CDE{pattern}{{4}}\d{{2}}$", result)

            @pytest.mark.parametrize("create_generator", GENERATOR_FACTORIES)
            @pytest.mark.parametrize(("type_name", "pattern"), TYPE_CONTEXTS)
            def it_returns_an_18_character_cnpj_when_format_prefix_and_type_are_set(
                create_generator,
                type_name,
                pattern,
            ):
                generate = create_generator(
                    {
                        "format": True,
                        "prefix": "AB123CDE",
                        "type": type_name,
                    },
                )

                result = generate()

                assert len(result) == 18
                assert not re.search(r"[a-z]", result)
                assert re.fullmatch(rf"^AB\.123\.CDE/{pattern}{{4}}-\d{{2}}$", result)

        def describe_when_cnpj_check_digits_throws_an_exception():
            def it_retries_generation_and_returns_a_valid_cnpj():
                with patch(
                    "cnpj_gen.cnpj_generator.generate_random_sequence",
                ) as mock_sequence:
                    mock_sequence.side_effect = ["111111111111", "123456780001"]

                    result = CnpjGenerator().generate()

                    assert len(result) == 14
                    assert result.startswith("123456780001")
                    assert mock_sequence.call_count == 2

            def it_uses_the_same_options_on_retry():
                with patch(
                    "cnpj_gen.cnpj_generator.generate_random_sequence",
                ) as mock_sequence:
                    mock_sequence.side_effect = ["0000", "0001"]

                    result = CnpjGenerator({"prefix": "12345678"}).generate()

                    assert len(result) == 14
                    assert result.startswith("12345678")
                    assert mock_sequence.call_count == 2
                    mock_sequence.assert_any_call(4, "alphanumeric")
                    assert mock_sequence.call_args_list == [
                        ((4, "alphanumeric"),),
                        ((4, "alphanumeric"),),
                    ]

            def it_retries_with_the_same_per_call_options():
                with patch(
                    "cnpj_gen.cnpj_generator.generate_random_sequence",
                ) as mock_sequence:
                    mock_sequence.side_effect = ["0000000000", "ABC1230001"]

                    generator = _CnpjGeneratorCallsSpy()
                    result = generator.generate(
                        format=False,
                        prefix="00",
                        type="alphanumeric",
                    )

                    assert len(result) == 14
                    assert result.startswith("00ABC1230001")
                    assert generator.calls_count == 2
                    assert generator.calls_arguments == [
                        (
                            None,
                            {"format": False, "prefix": "00", "type": "alphanumeric"},
                        ),
                        (
                            None,
                            {"format": False, "prefix": "00", "type": "alphanumeric"},
                        ),
                    ]
