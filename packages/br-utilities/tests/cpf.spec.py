"""Behavioral spec for CPF utilities accessed through ``BrUtils.cpf``.

Combines the CPF delegation cases from ``php/packages/br-utils/tests/specs/BrUtils.spec.php``
and the smoke tests from the prior Python ``br_utils_cpf_test.py`` file, following
``AGENTS.md``.

Dropped cases:
- PHP ``phpunit/Cpf/*`` legacy CPF v1 component suites (Python aligns with
  ``cpf-utils`` v2, not PHP CPF v1).
- PHP positional nullable parameters on ``format()`` / ``generate()`` (Python
  uses keyword overrides and options objects per v2).
- PHP ``getFormatter()`` accessor names (Python uses ``.formatter`` property).
"""

from __future__ import annotations

import re
from collections.abc import Callable

import pytest
from br_utils import BrUtils
from br_utils.cpf import CpfFormatter, CpfGenerator

FormatFn = Callable[[str, str | None, str | None], str]
GenerateFn = Callable[..., str]


def _format_with_dict_in_constructor(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    utils = BrUtils(cpf={"formatter": {"dot_key": dot_key, "dash_key": dash_key}})
    return utils.cpf.format(cpf)


def _format_with_kwargs_in_method(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    utils = BrUtils()
    return utils.cpf.format(cpf, dot_key=dot_key, dash_key=dash_key)


def _generate_with_dict_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    utils = BrUtils(cpf={"generator": {"format": format, "prefix": prefix}})
    return utils.cpf.generate()


def _generate_with_kwargs_in_method(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    utils = BrUtils()
    return utils.cpf.generate(format=format, prefix=prefix)


FORMAT_FACTORIES = [
    pytest.param(_format_with_dict_in_constructor, id="constructor_dict"),
    pytest.param(_format_with_kwargs_in_method, id="method_kwargs"),
]

GENERATE_FACTORIES = [
    pytest.param(_generate_with_dict_in_constructor, id="constructor_dict"),
    pytest.param(_generate_with_kwargs_in_method, id="method_kwargs"),
]


def describe_cpf_utils_through_br_utils():
    def describe_format_method():
        def describe_format_contexts():
            @pytest.mark.parametrize("format_fn", FORMAT_FACTORIES)
            def it_matches_cpf_formatter_format_behavior(format_fn: FormatFn):
                input_cpf = "80976511061"
                formatter = CpfFormatter()

                result = format_fn(input_cpf)

                assert result == formatter.format(input_cpf)

            @pytest.mark.parametrize("format_fn", FORMAT_FACTORIES)
            def it_forwards_formatting_options(format_fn: FormatFn):
                input_cpf = "80976511061"
                dot_key = "_"
                dash_key = " dv "

                result = format_fn(input_cpf, dot_key, dash_key)

                assert result == "809_765_110 dv 61"

        def it_applies_constructor_formatter_defaults_when_method_options_are_omitted():
            utils = BrUtils(
                cpf={
                    "formatter": {
                        "hidden": True,
                        "hidden_key": "#",
                    },
                }
            )

            result = utils.cpf.format("80976511061")

            assert "#" in result

        def it_formats_a_basic_cpf_string():
            utils = BrUtils()
            result = utils.cpf.format("12345678901")

            assert result == "123.456.789-01"

    def describe_generate_method():
        def describe_generate_contexts():
            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_matches_cpf_generator_generate_behavior(generate_fn: GenerateFn):
                generator = CpfGenerator()

                result = generate_fn()

                assert re.fullmatch(r"\d{11}", result)
                assert len(result) == len(generator.generate())

            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_forwards_generation_options(generate_fn: GenerateFn):
                result = generate_fn(format=True, prefix="12345")

                assert re.fullmatch(r"^123\.45\d\.\d{3}-\d{2}$", result)

            @pytest.mark.parametrize("generate_fn", GENERATE_FACTORIES)
            def it_returns_a_deterministic_cpf_for_a_full_9_character_prefix(
                generate_fn: GenerateFn,
            ):
                prefix = "123456789"
                results = [generate_fn(prefix=prefix) for _ in range(20)]

                assert len(set(results)) == 1

        def it_generates_an_11_digit_cpf():
            utils = BrUtils()
            result = utils.cpf.generate()

            assert len(result) == 11

    def describe_is_valid_method():
        def it_returns_true_for_a_valid_cpf():
            utils = BrUtils()

            assert utils.cpf.is_valid("52998224725") is True

        def it_returns_false_for_an_invalid_cpf():
            utils = BrUtils()

            assert utils.cpf.is_valid("12345678901") is False
