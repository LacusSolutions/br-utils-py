"""Behavioral spec for ``CpfUtils``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-utils/tests/cpf-utils.spec.ts``) and the PHP reference
suite (``php/packages/cpf-utils/tests/`` exercising ``CpfFormatterTestCases``,
``CpfGeneratorTestCases``, and ``CpfValidatorTestCases`` through the facade),
plus the delegation and ``__slots__`` cases from the prior Python ``*_test.py``
files, following the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``js/packages/cpf-utils/tests/output.spec.ts`` distribution artifacts
  (UMD/CJS/ESM bundles, declaration files, global variable wiring, and export
  string parsing). Those concern JS packaging only.
- JavaScript ``spyOn(CpfFormatter.prototype, ...)`` / prototype spies
  (replaced with instance ``MagicMock`` delegation tests that assert the same
  premise: façade methods forward to their component instances).
- PHP ``getFormatter()`` / ``getGenerator()`` / ``getValidator()`` accessor
  names (Python uses ``.formatter`` / ``.generator`` / ``.validator`` properties).
- JavaScript ``undefined`` nullish values (Python uses ``None``).
- CNPJ-only scenarios: validator options, ``slash_key``, generator ``type``,
  alphanumeric inputs, 14-character lengths.
- PHP ``CpfGeneratorTestCases::testPrefixedValueCannotAcceptStringWithMoreThan9Digits``
  (PHP rejects prefixes longer than 9 digits; JS/Python truncate silently).
- PHP native ``TypeError`` from typed ``string`` parameters on ``isValid`` for
  ``true`` / ``false`` / ``INF`` / closures (Python mirrors JS and raises
  ``CpfValidatorInputTypeError`` for non-``str`` / non-``Sequence[str]`` inputs;
  the int/bool/null/list cases cover that behavior).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any
from unittest.mock import ANY, MagicMock

import pytest
from cpf_fmt import (
    CpfFormatter,
    CpfFormatterOptions,
    CpfFormatterOptionsForbiddenKeyCharacterException,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfFormatterOptionsTypeError,
)
from cpf_gen import (
    CpfGenerator,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
    CpfGeneratorOptionsTypeError,
)
from cpf_utils import CpfUtils
from cpf_val import CpfValidator, CpfValidatorInputTypeError

FormatFn = Callable[[str, str | None, str | None], str]
GenerateFn = Callable[..., str]
IsValidFn = Callable[[str], bool]


def _compact_options(**kwargs: Any) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def _default_formatter_options_snapshot() -> dict:
    return CpfFormatterOptions().all


def _default_generator_options_snapshot() -> dict:
    return CpfGeneratorOptions().all


def _format_with_dict_in_constructor(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    utils = CpfUtils(formatter=_compact_options(dot_key=dot_key, dash_key=dash_key))
    return utils.format(cpf)


def _format_with_options_instance_in_constructor(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    options = CpfFormatterOptions(_compact_options(dot_key=dot_key, dash_key=dash_key))
    utils = CpfUtils(formatter=options)
    return utils.format(cpf)


def _format_with_kwargs_in_method(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    utils = CpfUtils()
    return utils.format(cpf, dot_key=dot_key, dash_key=dash_key)


def _format_with_options_in_method(
    cpf: str,
    dot_key: str | None = None,
    dash_key: str | None = None,
) -> str:
    utils = CpfUtils()
    options = CpfFormatterOptions(_compact_options(dot_key=dot_key, dash_key=dash_key))
    return utils.format(cpf, options)


def _generate_with_dict_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    utils = CpfUtils(generator=_compact_options(format=format, prefix=prefix))
    return utils.generate()


def _generate_with_options_instance_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    options = CpfGeneratorOptions(_compact_options(format=format, prefix=prefix))
    utils = CpfUtils(generator=options)
    return utils.generate()


def _generate_with_kwargs_in_method(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    utils = CpfUtils()
    return utils.generate(format=format, prefix=prefix)


def _generate_with_options_in_method(
    format: bool | None = None,
    prefix: str | None = None,
) -> str:
    utils = CpfUtils()
    options = CpfGeneratorOptions(_compact_options(format=format, prefix=prefix))
    return utils.generate(options)


def _is_valid_with_validator_instance_in_constructor(cpf: str) -> bool:
    validator = CpfValidator()
    utils = CpfUtils(validator=validator)
    return utils.is_valid(cpf)


def _is_valid_direct(cpf: str) -> bool:
    return CpfUtils().is_valid(cpf)


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
    pytest.param(_is_valid_direct, id="default_instance"),
    pytest.param(
        _is_valid_with_validator_instance_in_constructor, id="constructor_validator"
    ),
]


def describe_cpf_utils():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_resources_in_their_default_state():
                utils = CpfUtils()

                assert isinstance(utils.formatter, CpfFormatter)
                assert isinstance(utils.generator, CpfGenerator)
                assert isinstance(utils.validator, CpfValidator)

            def it_creates_an_instance_with_default_options():
                utils = CpfUtils()

                _assert_options_snapshots_match(
                    utils.formatter.options.all,
                    _default_formatter_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.generator.options.all,
                    _default_generator_options_snapshot(),
                )

        def describe_when_called_with_instances_of_resources():
            def it_uses_the_passed_formatter_directly():
                formatter = CpfFormatter()
                utils = CpfUtils(formatter=formatter)

                assert isinstance(utils.formatter, CpfFormatter)
                assert utils.formatter is formatter

            def it_uses_the_passed_generator_directly():
                generator = CpfGenerator()
                utils = CpfUtils(generator=generator)

                assert isinstance(utils.generator, CpfGenerator)
                assert utils.generator is generator

            def it_uses_the_passed_validator_directly():
                validator = CpfValidator()
                utils = CpfUtils(validator=validator)

                assert isinstance(utils.validator, CpfValidator)
                assert utils.validator is validator

            def it_uses_the_passed_resources_directly():
                formatter = CpfFormatter()
                generator = CpfGenerator()
                validator = CpfValidator()
                utils = CpfUtils(
                    formatter=formatter,
                    generator=generator,
                    validator=validator,
                )

                assert utils.formatter is formatter
                assert utils.generator is generator
                assert utils.validator is validator

        def describe_when_called_with_instances_of_resources_options():
            def it_creates_a_new_formatter_instance_with_the_passed_options():
                formatter_options = CpfFormatterOptions()
                utils = CpfUtils(formatter=formatter_options)

                assert isinstance(utils.formatter, CpfFormatter)
                assert utils.formatter.options is formatter_options

            def it_creates_a_new_generator_instance_with_the_passed_options():
                generator_options = CpfGeneratorOptions()
                utils = CpfUtils(generator=generator_options)

                assert isinstance(utils.generator, CpfGenerator)
                assert utils.generator.options is generator_options

            def it_creates_new_resources_instances_with_the_passed_options():
                formatter_options = CpfFormatterOptions()
                generator_options = CpfGeneratorOptions()
                utils = CpfUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                )

                assert utils.formatter.options is formatter_options
                assert utils.generator.options is generator_options
                assert isinstance(utils.validator, CpfValidator)

        def describe_when_called_with_partial_options_of_resources():
            formatter_options = {
                "hidden": True,
                "hidden_key": "#",
                "hidden_start": 8,
                "hidden_end": 10,
                "dot_key": "_",
                "dash_key": " dv ",
            }
            generator_options = {
                "format": True,
                "prefix": "12345678",
            }

            def it_creates_a_new_formatter_instance_with_the_passed_options():
                utils = CpfUtils(formatter=formatter_options)

                assert isinstance(utils.formatter, CpfFormatter)
                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value

            def it_creates_a_new_generator_instance_with_the_passed_options():
                utils = CpfUtils(generator=generator_options)

                assert isinstance(utils.generator, CpfGenerator)
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value

            def it_creates_new_resources_instances_with_the_passed_options():
                utils = CpfUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                )

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value
                assert isinstance(utils.validator, CpfValidator)

        def describe_when_called_with_arguments():
            def it_configures_formatter_and_generator_from_dicts():
                formatter_options = {"hidden": True, "hidden_key": "X"}
                generator_options = {"format": True, "prefix": "12345"}

                utils = CpfUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                )

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value

            def it_uses_provided_options_instances_directly():
                formatter_options = CpfFormatterOptions({"hidden": True})
                generator_options = CpfGeneratorOptions({"format": True})

                utils = CpfUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                )

                assert utils.formatter.options is formatter_options
                assert utils.generator.options is generator_options

            def it_mutates_shared_options_instances_and_affects_later_calls():
                generator_options = CpfGeneratorOptions({"format": False})
                utils = CpfUtils(generator=generator_options)

                generator_options.format = True
                generator_options.prefix = "12345678"

                assert utils.generator.options.all["format"] is True
                assert utils.generator.options.all["prefix"] == "12345678"

        def describe_when_called_with_invalid_options():
            def it_throws_formatter_exceptions_for_invalid_formatter_options():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    CpfUtils(formatter={"hidden_start": -1})

                with pytest.raises(CpfFormatterOptionsForbiddenKeyCharacterException):
                    CpfUtils(formatter={"dash_key": "\u00e5"})

            def it_throws_generator_exceptions_for_invalid_generator_options():
                with pytest.raises(CpfGeneratorOptionPrefixInvalidException):
                    CpfUtils(generator={"prefix": "000000000"})

                with pytest.raises(CpfGeneratorOptionsTypeError):
                    CpfUtils(generator={"prefix": 123})

    def describe_resource_accessors():
        def it_returns_the_formatter_instance_used_internally():
            utils = CpfUtils()

            assert isinstance(utils.formatter, CpfFormatter)

        def it_returns_the_generator_instance_used_internally():
            utils = CpfUtils()

            assert isinstance(utils.generator, CpfGenerator)

        def it_returns_the_validator_instance_used_internally():
            utils = CpfUtils()

            assert isinstance(utils.validator, CpfValidator)

    def describe_formatter_setter():
        def describe_when_called_with_a_complete_new_instance_of_cpf_formatter():
            def it_sets_the_formatter_instance():
                utils = CpfUtils()
                formatter = CpfFormatter()

                utils.formatter = formatter

                assert utils.formatter is formatter

        def describe_when_called_with_an_instance_of_cpf_formatter_options():
            def it_sets_the_formatter_instance():
                utils = CpfUtils()
                formatter_options = CpfFormatterOptions()

                utils.formatter = formatter_options

                assert utils.formatter.options is formatter_options

        def describe_when_called_with_a_partial_object_with_options_to_the_formatter_options():
            formatter_options = {
                "hidden": True,
                "hidden_key": "#",
                "hidden_start": 8,
                "hidden_end": 10,
                "dot_key": "_",
                "dash_key": " dv ",
            }

            def it_sets_the_formatter_instance_with_options():
                utils = CpfUtils()

                utils.formatter = formatter_options

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value

            def it_sets_the_formatter_instance_with_empty_object():
                utils = CpfUtils()
                original_formatter = utils.formatter
                original_formatter_options = original_formatter.options.all

                utils.formatter = {}

                assert utils.formatter is not original_formatter
                _assert_options_snapshots_match(
                    utils.formatter.options.all,
                    original_formatter_options,
                )

    def describe_generator_setter():
        def describe_when_called_with_a_complete_new_instance_of_cpf_generator():
            def it_sets_the_generator_instance():
                utils = CpfUtils()
                generator = CpfGenerator()

                utils.generator = generator

                assert utils.generator is generator

        def describe_when_called_with_an_instance_of_cpf_generator_options():
            def it_sets_the_generator_instance():
                utils = CpfUtils()
                generator_options = CpfGeneratorOptions()

                utils.generator = generator_options

                assert utils.generator.options is generator_options

        def describe_when_called_with_a_partial_object_with_options_to_the_generator_options():
            generator_options = {
                "format": True,
                "prefix": "12345678",
            }

            def it_sets_the_generator_instance_with_options():
                utils = CpfUtils()

                utils.generator = generator_options

                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value

            def it_sets_the_generator_instance_with_empty_object():
                utils = CpfUtils()
                original_generator = utils.generator
                original_generator_options = original_generator.options.all

                utils.generator = {}

                assert utils.generator is not original_generator
                _assert_options_snapshots_match(
                    utils.generator.options.all,
                    original_generator_options,
                )

    def describe_validator_setter():
        def describe_when_called_with_a_complete_new_instance_of_cpf_validator():
            def it_sets_the_validator_instance():
                utils = CpfUtils()
                validator = CpfValidator()

                utils.validator = validator

                assert utils.validator is validator

    def describe_format_method():
        def describe_delegation():
            def it_invokes_the_formatter_method_with_the_same_arguments():
                utils = CpfUtils()
                utils.formatter = MagicMock()
                options = CpfFormatterOptions()
                cpf = "12345678909"

                utils.format(cpf, options)

                utils.formatter.format.assert_called_once_with(cpf, options)

            def it_returns_the_formatted_cpf():
                utils = CpfUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.return_value = "formatted-cpf"

                result = utils.format("12345678909")

                assert result == "formatted-cpf"

            def it_forwards_named_formatting_options():
                utils = CpfUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.return_value = "123.456.789-09"

                result = utils.format(
                    "12345678909",
                    hidden=True,
                    hidden_key="X",
                    escape=True,
                    on_fail=lambda value: value,
                )

                assert result == "123.456.789-09"
                utils.formatter.format.assert_called_once_with(
                    "12345678909",
                    hidden=True,
                    hidden_key="X",
                    hidden_start=None,
                    hidden_end=None,
                    dot_key=None,
                    dash_key=None,
                    escape=True,
                    on_fail=ANY,
                )

            def it_throws_any_error_the_formatter_throws():
                utils = CpfUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.format("12345678909")

        def it_applies_constructor_formatter_defaults_when_method_options_are_omitted():
            utils = CpfUtils(
                formatter={
                    "hidden": True,
                    "hidden_key": "#",
                },
            )

            result = utils.format("12345678909")

            assert "#" in result

        def describe_format_contexts():
            @pytest.mark.parametrize("format_cpf", FORMAT_FACTORIES)
            def it_matches_cpf_formatter_format_behavior(format_cpf: FormatFn):
                input_value = "80976511061"
                formatter = CpfFormatter()

                result = format_cpf(input_value, None, None)

                assert result == formatter.format(input_value)

            @pytest.mark.parametrize("format_cpf", FORMAT_FACTORIES)
            def it_forwards_formatting_options(format_cpf: FormatFn):
                input_value = "12345678909"
                dot_key = "_"
                dash_key = " dv "

                result = format_cpf(input_value, dot_key, dash_key)

                assert result == "123_456_789 dv 09"

        def describe_php_formatter_test_cases():
            def it_formats_cpf_with_dots_and_dash_to_same_format():
                utils = CpfUtils()

                assert utils.format("809.765.110-61") == "809.765.110-61"

            def it_formats_cpf_without_formatting_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("80976511061") == "809.765.110-61"

            def it_formats_cpf_with_dashes_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("809-765-110-61") == "809.765.110-61"

            def it_formats_cpf_with_spaces_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("809 765 110 61") == "809.765.110-61"

            def it_formats_cpf_with_trailing_space_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("80976511061 ") == "809.765.110-61"

            def it_formats_cpf_with_leading_space_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format(" 80976511061") == "809.765.110-61"

            def it_formats_cpf_with_individual_dots_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("8.0.9.7.6.5.1.1.0.6.1") == "809.765.110-61"

            def it_formats_cpf_with_individual_dashes_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("8-0-9-7-6-5-1-1-0-6-1") == "809.765.110-61"

            def it_formats_cpf_with_individual_spaces_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("8 0 9 7 6 5 1 1 0 6 1") == "809.765.110-61"

            def it_formats_cpf_with_letters_to_dots_and_dash():
                utils = CpfUtils()

                assert utils.format("80976511061abc") == "809.765.110-61"

            def it_formats_cpf_with_mixed_characters_correctly():
                utils = CpfUtils()

                assert utils.format("809765110 dv 61") == "809.765.110-61"

            def it_formats_cpf_to_custom_delimiters_without_dots():
                utils = CpfUtils()

                assert utils.format("80976511061", dot_key="") == "809765110-61"

            def it_formats_cpf_to_custom_delimiters_with_dash_as_dot():
                utils = CpfUtils()

                assert utils.format("80976511061", dash_key=".") == "809.765.110.61"

            def it_formats_cpf_to_no_delimiters():
                utils = CpfUtils()

                assert (
                    utils.format("809.765.110-61", dot_key="", dash_key="")
                    == "80976511061"
                )

            def it_formats_cpf_to_custom_delimiters_with_escape():
                utils = CpfUtils()

                assert (
                    utils.format(
                        "80976511061",
                        escape=True,
                        dot_key="<",
                        dash_key=">",
                    )
                    == "809&lt;765&lt;110&gt;61"
                )

            def it_formats_cpf_to_hidden_format():
                utils = CpfUtils()

                assert utils.format("80976511061", hidden=True) == "809.***.***-**"

            def it_formats_cpf_to_hidden_format_with_start_range():
                utils = CpfUtils()

                assert (
                    utils.format("80976511061", hidden=True, hidden_start=6)
                    == "809.765.***-**"
                )

            def it_formats_cpf_to_hidden_format_with_end_range():
                utils = CpfUtils()

                assert (
                    utils.format("80976511061", hidden=True, hidden_end=8)
                    == "809.***.***-61"
                )

            def it_formats_cpf_to_hidden_format_with_start_and_end_range():
                utils = CpfUtils()

                assert (
                    utils.format(
                        "80976511061",
                        hidden=True,
                        hidden_start=0,
                        hidden_end=8,
                    )
                    == "***.***.***-61"
                )

            def it_formats_cpf_to_hidden_format_with_reversed_range():
                utils = CpfUtils()

                assert (
                    utils.format(
                        "80976511061",
                        hidden=True,
                        hidden_start=9,
                        hidden_end=3,
                    )
                    == "809.***.***-*1"
                )

            def it_formats_cpf_to_hidden_format_with_custom_key():
                utils = CpfUtils()

                assert (
                    utils.format("80976511061", hidden=True, hidden_key="#")
                    == "809.###.###-##"
                )

            def it_formats_cpf_to_hidden_format_with_custom_key_and_range():
                utils = CpfUtils()

                assert (
                    utils.format(
                        "80976511061",
                        hidden=True,
                        hidden_key="#",
                        hidden_start=6,
                    )
                    == "809.765.###-##"
                )

            def it_falls_back_to_on_fail_callback_for_invalid_input():
                utils = CpfUtils()

                assert (
                    utils.format(
                        "abc",
                        on_fail=lambda value, _error: value.upper(),
                    )
                    == "ABC"
                )

            def it_throws_when_hidden_start_is_out_of_range():
                utils = CpfUtils()

                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    utils.format("80976511061", hidden=True, hidden_start=-1)

                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    utils.format("80976511061", hidden=True, hidden_start=11)

            def it_throws_when_hidden_end_is_out_of_range():
                utils = CpfUtils()

                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    utils.format("80976511061", hidden=True, hidden_end=-1)

                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    utils.format("80976511061", hidden=True, hidden_end=11)

            def it_throws_when_on_fail_is_not_callable():
                utils = CpfUtils()

                with pytest.raises(CpfFormatterOptionsTypeError):
                    utils.format("80976511061", on_fail="testing")

    def describe_generate_method():
        def describe_delegation():
            def it_invokes_the_generator_method_with_the_same_arguments():
                utils = CpfUtils()
                utils.generator = MagicMock()
                options = CpfGeneratorOptions()

                utils.generate(options)

                utils.generator.generate.assert_called_once_with(options)

            def it_returns_the_generated_cpf():
                utils = CpfUtils()
                utils.generator = MagicMock()
                utils.generator.generate.return_value = "generated-cpf"

                result = utils.generate()

                assert result == "generated-cpf"

            def it_forwards_named_generation_options():
                utils = CpfUtils()
                utils.generator = MagicMock()
                utils.generator.generate.return_value = "123.456.789-09"

                result = utils.generate(format=True, prefix="12345678")

                assert result == "123.456.789-09"
                utils.generator.generate.assert_called_once_with(
                    format=True,
                    prefix="12345678",
                )

            def it_throws_any_error_the_generator_throws():
                utils = CpfUtils()
                utils.generator = MagicMock()
                utils.generator.generate.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.generate()

        def describe_generate_contexts():
            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_matches_cpf_generator_generate_behavior(generate: GenerateFn):
                generator = CpfGenerator()

                result = generate()

                assert re.fullmatch(r"^\d{11}$", result)
                assert len(result) == len(generator.generate())

            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_forwards_generation_options(generate: GenerateFn):
                result = generate(format=True, prefix="12345678")

                assert re.fullmatch(r"^123\.456\.78\d-\d{2}$", result)

            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_returns_a_deterministic_cpf_for_a_full_9_digit_prefix(
                generate: GenerateFn,
            ):
                prefix = "123456789"
                results = [generate(prefix=prefix) for _ in range(20)]

                assert len(set(results)) == 1

        def describe_php_generator_test_cases():
            def it_generates_11_digit_strings_without_formatting():
                utils = CpfUtils()

                for _ in range(25):
                    assert len(utils.generate()) == 11

            def it_generates_14_character_strings_with_formatting():
                utils = CpfUtils()

                for _ in range(25):
                    assert len(utils.generate(format=True)) == 14

            def it_generates_valid_cpfs_without_formatting():
                utils = CpfUtils()

                for _ in range(25):
                    cpf = utils.generate()
                    assert utils.is_valid(cpf) is True, f"Expected {cpf!r} to be valid"

            def it_generates_valid_formatted_cpfs_with_formatting():
                utils = CpfUtils()

                for _ in range(25):
                    cpf = utils.generate(format=True)
                    assert utils.is_valid(cpf) is True, f"Expected {cpf!r} to be valid"

            def it_generates_valid_cpfs_with_prefixes():
                utils = CpfUtils()
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
                    cpf = utils.generate(prefix=prefix)
                    assert (
                        utils.is_valid(cpf) is True
                    ), f"Expected {cpf!r} with prefix {prefix!r} to be valid"

            def it_generates_formatted_cpfs_matching_the_default_pattern():
                utils = CpfUtils()

                for _ in range(25):
                    cpf = utils.generate(format=True)
                    assert re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf), cpf

            def it_generates_cpfs_with_prefix_matching_expected_length():
                utils = CpfUtils()
                result = utils.generate({"prefix": "12345"})

                assert re.fullmatch(r"^12345\d{6}$", result)

    def describe_is_valid_method():
        def describe_delegation():
            def it_invokes_the_validator_method_with_the_same_arguments():
                utils = CpfUtils()
                utils.validator = MagicMock()
                cpf = "12345678909"

                utils.is_valid(cpf)

                utils.validator.is_valid.assert_called_once_with(cpf)

            def it_returns_the_validation_result():
                utils = CpfUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.return_value = True

                result = utils.is_valid("12345678909")

                assert result is True

            def it_returns_false_when_the_validator_returns_false():
                utils = CpfUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.return_value = False

                result = utils.is_valid("12345678900")

                assert result is False
                utils.validator.is_valid.assert_called_once_with("12345678900")

            def it_throws_any_error_the_validator_throws():
                utils = CpfUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.is_valid("12345678909")

        def describe_is_valid_contexts():
            @pytest.mark.parametrize("is_valid", IS_VALID_FACTORIES)
            def it_matches_cpf_validator_is_valid_behavior(is_valid: IsValidFn):
                input_value = "86244870050"
                validator = CpfValidator()

                result = is_valid(input_value)

                assert result == validator.is_valid(input_value)

            @pytest.mark.parametrize("is_valid", IS_VALID_FACTORIES)
            def it_validates_formatted_and_unformatted_cpf_strings(
                is_valid: IsValidFn,
            ):
                assert is_valid("12345678909") is True
                assert is_valid("123.456.789-09") is True
                assert is_valid("12345678900") is False

        def describe_php_validator_test_cases():
            def it_validates_cpf_string_with_dots_and_dash():
                utils = CpfUtils()

                assert utils.is_valid("499.784.420-90") is True

            def it_validates_cpf_string_with_dots():
                utils = CpfUtils()

                assert utils.is_valid("028.062.110.85") is True

            def it_validates_cpf_string_with_underscores():
                utils = CpfUtils()

                assert utils.is_valid("011_258_960_00") is True

            def it_validates_cpf_string_with_dash():
                utils = CpfUtils()

                assert utils.is_valid("779953010-30") is True

            def it_validates_cpf_string_without_formatting():
                utils = CpfUtils()

                assert utils.is_valid("86244870050") is True

            def it_validates_known_valid_cpf_samples():
                utils = CpfUtils()
                valid_samples = [
                    "22312659077",
                    "96215666068",
                    "67107095072",
                    "48039958008",
                    "20954431014",
                ]

                for cpf in valid_samples:
                    assert utils.is_valid(cpf) is True, f"Expected {cpf!r} to be valid"

            def it_rejects_cpf_string_09087121971():
                utils = CpfUtils()

                assert utils.is_valid("090.871.219-71") is False

            def it_rejects_cpf_string_08146572910():
                utils = CpfUtils()

                assert utils.is_valid("081.465.729.10") is False

            def it_rejects_cpf_string_01125896099():
                utils = CpfUtils()

                assert utils.is_valid("011_258_960_99") is False

            def it_rejects_cpf_string_49978442075():
                utils = CpfUtils()

                assert utils.is_valid("499784420-75") is False

            def it_rejects_cpf_string_86244870011():
                utils = CpfUtils()

                assert utils.is_valid("86244870011") is False

            def it_raises_for_non_string_input():
                utils = CpfUtils()

                with pytest.raises(CpfValidatorInputTypeError):
                    utils.is_valid(123)

            def it_rejects_abc():
                utils = CpfUtils()

                assert utils.is_valid("abc") is False

            def it_rejects_abc123():
                utils = CpfUtils()

                assert utils.is_valid("abc123") is False

            def it_raises_for_boolean_input():
                utils = CpfUtils()

                with pytest.raises(CpfValidatorInputTypeError):
                    utils.is_valid(True)

            def it_raises_for_null_input():
                utils = CpfUtils()

                with pytest.raises(CpfValidatorInputTypeError):
                    utils.is_valid(None)

            def it_raises_for_array_input():
                utils = CpfUtils()

                with pytest.raises(CpfValidatorInputTypeError):
                    utils.is_valid([1, 2, 3])

            def it_raises_for_object_input():
                utils = CpfUtils()

                with pytest.raises(CpfValidatorInputTypeError):
                    utils.is_valid({"a": 1, "b": 2, "c": 3})

    def describe_integration():
        def it_uses_the_correct_component_instances_for_all_methods():
            utils = CpfUtils()
            utils.formatter = MagicMock()
            utils.generator = MagicMock()
            utils.validator = MagicMock()
            utils.formatter.format.return_value = "formatted"
            utils.generator.generate.return_value = "generated"
            utils.validator.is_valid.return_value = True

            assert utils.format("123") == "formatted"
            assert utils.generate() == "generated"
            assert utils.is_valid("123") is True
            utils.formatter.format.assert_called_once()
            utils.generator.generate.assert_called_once()
            utils.validator.is_valid.assert_called_once()

    def describe_slots():
        def it_restricts_dynamic_attributes():
            utils = CpfUtils()

            with pytest.raises(AttributeError):
                utils.new_attribute = "test"

            assert hasattr(utils, "formatter")
            assert hasattr(utils, "generator")
            assert hasattr(utils, "validator")
