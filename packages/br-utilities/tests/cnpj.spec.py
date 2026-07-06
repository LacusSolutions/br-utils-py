"""Behavioral spec for CNPJ utilities accessed through ``BrUtils.cnpj``.

Combines the CNPJ delegation cases from ``php/packages/br-utils/tests/specs/BrUtils.spec.php``
and the smoke tests from the prior Python ``br_utils_cnpj_test.py`` file, following
``AGENTS.md``.

Dropped cases:
- PHP ``CnpjType`` / ``CnpjValidationType`` enum types (Python uses string literals).
- PHP ``getFormatter()`` accessor names (Python uses ``.formatter`` property).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

import pytest
from br_utils import BrUtils
from br_utils.cnpj import (
    CnpjFormatter,
    CnpjFormatterOptions,
    CnpjGenerator,
    CnpjGeneratorOptions,
    CnpjValidator,
    CnpjValidatorOptions,
)

FormatFn = Callable[[str, str | None], str]
GenerateFn = Callable[..., str]
IsValidFn = Callable[..., bool]


def _compact_options(**kwargs: Any) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _format_with_dict_in_constructor(cnpj: str, slash_key: str | None = None) -> str:
    utils = BrUtils(cnpj={"formatter": {"slash_key": slash_key}})
    return utils.cnpj.format(cnpj)


def _format_with_options_instance_in_constructor(
    cnpj: str,
    slash_key: str | None = None,
) -> str:
    options = CnpjFormatterOptions({"slash_key": slash_key})
    utils = BrUtils(cnpj={"formatter": options})
    return utils.cnpj.format(cnpj)


def _format_with_kwargs_in_method(cnpj: str, slash_key: str | None = None) -> str:
    utils = BrUtils()
    return utils.cnpj.format(cnpj, slash_key=slash_key)


def _format_with_options_in_method(cnpj: str, slash_key: str | None = None) -> str:
    utils = BrUtils()
    options = CnpjFormatterOptions({"slash_key": slash_key})
    return utils.cnpj.format(cnpj, options)


def _generate_with_dict_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = BrUtils(
        cnpj={"generator": _compact_options(format=format, prefix=prefix, type=type)}
    )
    return utils.cnpj.generate()


def _generate_with_options_instance_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    options = CnpjGeneratorOptions(
        _compact_options(format=format, prefix=prefix, type=type)
    )
    utils = BrUtils(cnpj={"generator": options})
    return utils.cnpj.generate()


def _generate_with_kwargs_in_method(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = BrUtils()
    return utils.cnpj.generate(format=format, prefix=prefix, type=type)


def _generate_with_options_in_method(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = BrUtils()
    options = CnpjGeneratorOptions(
        _compact_options(format=format, prefix=prefix, type=type)
    )
    return utils.cnpj.generate(options)


def _is_valid_with_dict_in_constructor(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = BrUtils(
        cnpj={"validator": _compact_options(type=type, case_sensitive=case_sensitive)}
    )
    return utils.cnpj.is_valid(cnpj)


def _is_valid_with_validator_options_in_constructor(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    options = CnpjValidatorOptions(
        _compact_options(type=type, case_sensitive=case_sensitive)
    )
    utils = BrUtils(cnpj={"validator": options})
    return utils.cnpj.is_valid(cnpj)


def _is_valid_with_kwargs_in_method(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = BrUtils()
    return utils.cnpj.is_valid(cnpj, type=type, case_sensitive=case_sensitive)


def _is_valid_with_validator_options_in_method(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = BrUtils()
    options = CnpjValidatorOptions(
        _compact_options(type=type, case_sensitive=case_sensitive)
    )
    return utils.cnpj.is_valid(cnpj, options)


FORMAT_FACTORIES = [
    pytest.param(_format_with_dict_in_constructor, id="constructor_dict"),
    pytest.param(
        _format_with_options_instance_in_constructor, id="constructor_options"
    ),
    pytest.param(_format_with_kwargs_in_method, id="method_kwargs"),
    pytest.param(_format_with_options_in_method, id="method_options"),
]

GENERATE_FACTORIES = [
    pytest.param(_generate_with_dict_in_constructor, id="constructor_dict"),
    pytest.param(
        _generate_with_options_instance_in_constructor, id="constructor_options"
    ),
    pytest.param(_generate_with_kwargs_in_method, id="method_kwargs"),
    pytest.param(_generate_with_options_in_method, id="method_options"),
]

IS_VALID_FACTORIES = [
    pytest.param(_is_valid_with_dict_in_constructor, id="constructor_dict"),
    pytest.param(
        _is_valid_with_validator_options_in_constructor, id="constructor_options"
    ),
    pytest.param(_is_valid_with_kwargs_in_method, id="method_kwargs"),
    pytest.param(_is_valid_with_validator_options_in_method, id="method_options"),
]


def describe_cnpj_utils_through_br_utils():
    def describe_format_method():
        def describe_format_contexts():
            @pytest.mark.parametrize("format_fn", FORMAT_FACTORIES)
            def it_matches_cnpj_formatter_format_behavior(format_fn: FormatFn):
                input_cnpj = "91415732000793"
                formatter = CnpjFormatter()

                result = format_fn(input_cnpj)

                assert result == formatter.format(input_cnpj)

            @pytest.mark.parametrize("format_fn", FORMAT_FACTORIES)
            def it_forwards_formatting_options(format_fn: FormatFn):
                input_cnpj = "01ABC234000X56"
                slash_key = "|"

                result = format_fn(input_cnpj, slash_key)

                assert result == f"01.ABC.234{slash_key}000X-56"

        def it_applies_constructor_formatter_defaults_when_method_options_are_omitted():
            utils = BrUtils(
                cnpj={
                    "formatter": {
                        "hidden": True,
                        "hidden_key": "#",
                    },
                }
            )

            result = utils.cnpj.format("12ABC34500DE99")

            assert "#" in result

        def it_formats_a_basic_cnpj_string():
            utils = BrUtils()
            result = utils.cnpj.format("12345678000195")

            assert result == "12.345.678/0001-95"

    def describe_generate_method():
        def describe_generate_contexts():
            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_matches_cnpj_generator_generate_behavior(generate_fn: GenerateFn):
                generator = CnpjGenerator()

                result = generate_fn()

                assert re.fullmatch(r"^[0-9A-Z]{14}$", result)
                assert len(result) == len(generator.generate())

            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_forwards_generation_options(generate_fn: GenerateFn):
                result = generate_fn(format=True, prefix="12345", type="numeric")

                assert re.fullmatch(r"^12\.345\.\d{3}/\d{4}-\d{2}$", result)

            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_returns_a_deterministic_cnpj_for_a_full_12_character_prefix(
                generate_fn: GenerateFn,
            ):
                prefix = "123456780009"
                results = [generate_fn(prefix=prefix) for _ in range(20)]

                assert len(set(results)) == 1

        def it_generates_a_14_character_cnpj():
            utils = BrUtils()
            result = utils.cnpj.generate()

            assert len(result) == 14

    def describe_is_valid_method():
        def describe_is_valid_contexts():
            @pytest.mark.parametrize("is_valid_fn", IS_VALID_FACTORIES)
            def it_matches_cnpj_validator_is_valid_behavior(is_valid_fn: IsValidFn):
                input_cnpj = "91415732000793"
                validator = CnpjValidator()

                result = is_valid_fn(input_cnpj)

                assert result == validator.is_valid(input_cnpj)

            @pytest.mark.parametrize("is_valid_fn", IS_VALID_FACTORIES)
            def it_forwards_validation_options(is_valid_fn: IsValidFn):
                input_cnpj = "1QB5UKALPYFP59"

                assert is_valid_fn(input_cnpj, type="numeric") is False
                assert is_valid_fn(input_cnpj, type="alphanumeric") is True

            @pytest.mark.parametrize("is_valid_fn", IS_VALID_FACTORIES)
            def it_validates_formatted_and_unformatted_cnpj_strings(
                is_valid_fn: IsValidFn,
            ):
                assert is_valid_fn("1QB5UKALPYFP59") is True
                assert is_valid_fn("1QB5.UKAL.PYF/P59") is True
                assert is_valid_fn("AB123CDE0001555") is False

        def it_returns_true_for_a_valid_numeric_cnpj():
            utils = BrUtils()

            assert utils.cnpj.is_valid("11222333000181") is True

        def it_returns_false_for_an_invalid_cnpj():
            utils = BrUtils()

            assert utils.cnpj.is_valid("11111111111111") is False
