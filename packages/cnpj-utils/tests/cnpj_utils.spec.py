"""Behavioral spec for ``CnpjUtils``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-utils/tests/cnpj-utils.spec.ts``) and the PHP reference
suite (``php/packages/cnpj-utils/tests/specs/CnpjUtils.spec.php``), plus the
delegation and ``__slots__`` cases from the prior Python ``*_test.py`` files,
following the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``js/packages/cnpj-utils/tests/output.spec.ts`` distribution artifacts
  (UMD/CJS/ESM bundles, declaration files, global variable wiring, and export
  string parsing). Those concern JS packaging only.
- JavaScript ``spyOn(CnpjFormatter.prototype, ...)`` / prototype spies
  (replaced with instance ``MagicMock`` delegation tests that assert the same
  premise: façade methods forward to their component instances).
- PHP ``getFormatter()`` / ``getGenerator()`` / ``getValidator()`` accessor
  names (Python uses ``.formatter`` / ``.generator`` / ``.validator`` properties).
- JavaScript ``undefined`` nullish values (Python uses ``None``).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any
from unittest.mock import ANY, MagicMock

import pytest
from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterOptions,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
)
from cnpj_gen import (
    CnpjGenerator,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
)
from cnpj_utils import CnpjUtils
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorOptions,
    CnpjValidatorOptionTypeInvalidException,
)

FormatFn = Callable[[str, str | None], str]
GenerateFn = Callable[..., str]
IsValidFn = Callable[..., bool]


def _compact_options(**kwargs: Any) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def _default_formatter_options_snapshot() -> dict:
    return CnpjFormatterOptions().all


def _default_generator_options_snapshot() -> dict:
    return CnpjGeneratorOptions().all


def _default_validator_options_snapshot() -> dict:
    return CnpjValidatorOptions().all


def _format_with_dict_in_constructor(cnpj: str, slash_key: str | None = None) -> str:
    utils = CnpjUtils(formatter={"slash_key": slash_key})
    return utils.format(cnpj)


def _format_with_options_instance_in_constructor(
    cnpj: str,
    slash_key: str | None = None,
) -> str:
    options = CnpjFormatterOptions({"slash_key": slash_key})
    utils = CnpjUtils(formatter=options)
    return utils.format(cnpj)


def _format_with_kwargs_in_method(cnpj: str, slash_key: str | None = None) -> str:
    utils = CnpjUtils()
    return utils.format(cnpj, slash_key=slash_key)


def _format_with_options_in_method(cnpj: str, slash_key: str | None = None) -> str:
    utils = CnpjUtils()
    options = CnpjFormatterOptions({"slash_key": slash_key})
    return utils.format(cnpj, options)


def _generate_with_dict_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = CnpjUtils(
        generator=_compact_options(format=format, prefix=prefix, type=type)
    )
    return utils.generate()


def _generate_with_options_instance_in_constructor(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    options = CnpjGeneratorOptions(
        _compact_options(format=format, prefix=prefix, type=type)
    )
    utils = CnpjUtils(generator=options)
    return utils.generate()


def _generate_with_kwargs_in_method(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = CnpjUtils()
    return utils.generate(format=format, prefix=prefix, type=type)


def _generate_with_options_in_method(
    format: bool | None = None,
    prefix: str | None = None,
    type: str | None = None,
) -> str:
    utils = CnpjUtils()
    options = CnpjGeneratorOptions(
        _compact_options(format=format, prefix=prefix, type=type)
    )
    return utils.generate(options)


def _is_valid_with_dict_in_constructor(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = CnpjUtils(
        validator=_compact_options(type=type, case_sensitive=case_sensitive),
    )
    return utils.is_valid(cnpj)


def _is_valid_with_options_instance_in_constructor(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    options = CnpjValidatorOptions(
        _compact_options(type=type, case_sensitive=case_sensitive),
    )
    utils = CnpjUtils(validator=options)
    return utils.is_valid(cnpj)


def _is_valid_with_kwargs_in_method(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = CnpjUtils()
    return utils.is_valid(cnpj, type=type, case_sensitive=case_sensitive)


def _is_valid_with_options_in_method(
    cnpj: str,
    type: str | None = None,
    case_sensitive: bool | None = None,
) -> bool:
    utils = CnpjUtils()
    options = CnpjValidatorOptions(
        _compact_options(type=type, case_sensitive=case_sensitive),
    )
    return utils.is_valid(cnpj, options)


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
        _is_valid_with_options_instance_in_constructor, id="constructor_options"
    ),
    pytest.param(_is_valid_with_kwargs_in_method, id="method_kwargs"),
    pytest.param(_is_valid_with_options_in_method, id="method_options"),
]


def describe_cnpj_utils():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_resources_in_their_default_state():
                utils = CnpjUtils()

                assert isinstance(utils.formatter, CnpjFormatter)
                assert isinstance(utils.generator, CnpjGenerator)
                assert isinstance(utils.validator, CnpjValidator)

            def it_creates_an_instance_with_default_options():
                utils = CnpjUtils()

                _assert_options_snapshots_match(
                    utils.formatter.options.all,
                    _default_formatter_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.generator.options.all,
                    _default_generator_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.validator.options.all,
                    _default_validator_options_snapshot(),
                )

        def describe_when_called_with_instances_of_resources():
            def it_uses_the_passed_formatter_directly():
                formatter = CnpjFormatter()
                utils = CnpjUtils(formatter=formatter)

                assert isinstance(utils.formatter, CnpjFormatter)
                assert utils.formatter is formatter

            def it_uses_the_passed_generator_directly():
                generator = CnpjGenerator()
                utils = CnpjUtils(generator=generator)

                assert isinstance(utils.generator, CnpjGenerator)
                assert utils.generator is generator

            def it_uses_the_passed_validator_directly():
                validator = CnpjValidator()
                utils = CnpjUtils(validator=validator)

                assert isinstance(utils.validator, CnpjValidator)
                assert utils.validator is validator

            def it_uses_the_passed_resources_directly():
                formatter = CnpjFormatter()
                generator = CnpjGenerator()
                validator = CnpjValidator()
                utils = CnpjUtils(
                    formatter=formatter,
                    generator=generator,
                    validator=validator,
                )

                assert utils.formatter is formatter
                assert utils.generator is generator
                assert utils.validator is validator

        def describe_when_called_with_instances_of_resources_options():
            def it_creates_a_new_formatter_instance_with_the_passed_options():
                formatter_options = CnpjFormatterOptions()
                utils = CnpjUtils(formatter=formatter_options)

                assert isinstance(utils.formatter, CnpjFormatter)
                assert utils.formatter.options is formatter_options

            def it_creates_a_new_generator_instance_with_the_passed_options():
                generator_options = CnpjGeneratorOptions()
                utils = CnpjUtils(generator=generator_options)

                assert isinstance(utils.generator, CnpjGenerator)
                assert utils.generator.options is generator_options

            def it_creates_a_new_validator_instance_with_the_passed_options():
                validator_options = CnpjValidatorOptions()
                utils = CnpjUtils(validator=validator_options)

                assert isinstance(utils.validator, CnpjValidator)
                assert utils.validator.options is validator_options

            def it_creates_new_resources_instances_with_the_passed_options():
                formatter_options = CnpjFormatterOptions()
                generator_options = CnpjGeneratorOptions()
                validator_options = CnpjValidatorOptions()
                utils = CnpjUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                    validator=validator_options,
                )

                assert utils.formatter.options is formatter_options
                assert utils.generator.options is generator_options
                assert utils.validator.options is validator_options

        def describe_when_called_with_partial_options_of_resources():
            formatter_options = {
                "hidden": True,
                "hidden_key": "#",
                "hidden_start": 8,
                "hidden_end": 11,
                "dot_key": "_",
                "slash_key": "|",
                "dash_key": " dv ",
            }
            generator_options = {
                "format": True,
                "prefix": "12345678",
                "type": "numeric",
            }
            validator_options = {
                "case_sensitive": True,
                "type": "numeric",
            }

            def it_creates_a_new_formatter_instance_with_the_passed_options():
                utils = CnpjUtils(formatter=formatter_options)

                assert isinstance(utils.formatter, CnpjFormatter)
                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value

            def it_creates_a_new_generator_instance_with_the_passed_options():
                utils = CnpjUtils(generator=generator_options)

                assert isinstance(utils.generator, CnpjGenerator)
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value

            def it_creates_a_new_validator_instance_with_the_passed_options():
                utils = CnpjUtils(validator=validator_options)

                assert isinstance(utils.validator, CnpjValidator)
                for key, value in validator_options.items():
                    assert utils.validator.options.all[key] == value

            def it_creates_new_resources_instances_with_the_passed_options():
                utils = CnpjUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                    validator=validator_options,
                )

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value
                for key, value in validator_options.items():
                    assert utils.validator.options.all[key] == value

        def describe_when_called_with_arguments():
            def it_configures_formatter_generator_and_validator_from_dicts():
                formatter_options = {"slash_key": "|"}
                generator_options = {"format": True, "prefix": "12345"}
                validator_options = {"type": "numeric", "case_sensitive": False}

                utils = CnpjUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                    validator=validator_options,
                )

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value
                for key, value in validator_options.items():
                    assert utils.validator.options.all[key] == value

            def it_uses_provided_options_instances_directly():
                formatter_options = CnpjFormatterOptions({"slash_key": "|"})
                generator_options = CnpjGeneratorOptions({"format": True})
                validator_options = CnpjValidatorOptions({"type": "numeric"})

                utils = CnpjUtils(
                    formatter=formatter_options,
                    generator=generator_options,
                    validator=validator_options,
                )

                assert utils.formatter.options is formatter_options
                assert utils.generator.options is generator_options
                assert utils.validator.options is validator_options

            def it_mutates_shared_options_instances_and_affects_later_calls():
                generator_options = CnpjGeneratorOptions(
                    {"format": False, "type": "numeric"},
                )
                utils = CnpjUtils(generator=generator_options)

                generator_options.format = True
                generator_options.type = "alphabetic"

                assert utils.generator.options.all["format"] is True
                assert utils.generator.options.all["type"] == "alphabetic"

        def describe_when_called_with_invalid_options():
            def it_throws_formatter_exceptions_for_invalid_formatter_options():
                with pytest.raises(CnpjFormatterOptionsHiddenRangeInvalidException):
                    CnpjUtils(formatter={"hidden_start": -1})

                with pytest.raises(CnpjFormatterOptionsForbiddenKeyCharacterException):
                    CnpjUtils(formatter={"dash_key": "\u00e5"})

            def it_throws_generator_exceptions_for_invalid_generator_options():
                with pytest.raises(CnpjGeneratorOptionPrefixInvalidException):
                    CnpjUtils(generator={"prefix": "00000000"})

                with pytest.raises(CnpjGeneratorOptionTypeInvalidException):
                    CnpjUtils(generator={"type": "invalid"})

                with pytest.raises(CnpjGeneratorOptionsTypeError):
                    CnpjUtils(generator={"prefix": 123})

            def it_throws_validator_exceptions_for_invalid_validator_options():
                with pytest.raises(CnpjValidatorOptionTypeInvalidException):
                    CnpjUtils(validator={"type": "invalid"})

    def describe_resource_accessors():
        def it_returns_the_formatter_instance_used_internally():
            utils = CnpjUtils()

            assert isinstance(utils.formatter, CnpjFormatter)

        def it_returns_the_generator_instance_used_internally():
            utils = CnpjUtils()

            assert isinstance(utils.generator, CnpjGenerator)

        def it_returns_the_validator_instance_used_internally():
            utils = CnpjUtils()

            assert isinstance(utils.validator, CnpjValidator)

    def describe_formatter_setter():
        def describe_when_called_with_a_complete_new_instance_of_cnpj_formatter():
            def it_sets_the_formatter_instance():
                utils = CnpjUtils()
                formatter = CnpjFormatter()

                utils.formatter = formatter

                assert utils.formatter is formatter

        def describe_when_called_with_an_instance_of_cnpj_formatter_options():
            def it_sets_the_formatter_instance():
                utils = CnpjUtils()
                formatter_options = CnpjFormatterOptions()

                utils.formatter = formatter_options

                assert utils.formatter.options is formatter_options

        def describe_when_called_with_a_partial_object_with_options_to_the_formatter_options():
            formatter_options = {
                "hidden": True,
                "hidden_key": "#",
                "hidden_start": 8,
                "hidden_end": 11,
                "dot_key": "_",
                "slash_key": "|",
                "dash_key": " dv ",
            }

            def it_sets_the_formatter_instance_with_options():
                utils = CnpjUtils()

                utils.formatter = formatter_options

                for key, value in formatter_options.items():
                    assert utils.formatter.options.all[key] == value

            def it_sets_the_formatter_instance_with_empty_object():
                utils = CnpjUtils()
                original_formatter = utils.formatter
                original_formatter_options = original_formatter.options.all

                utils.formatter = {}

                assert utils.formatter is not original_formatter
                _assert_options_snapshots_match(
                    utils.formatter.options.all,
                    original_formatter_options,
                )

    def describe_generator_setter():
        def describe_when_called_with_a_complete_new_instance_of_cnpj_generator():
            def it_sets_the_generator_instance():
                utils = CnpjUtils()
                generator = CnpjGenerator()

                utils.generator = generator

                assert utils.generator is generator

        def describe_when_called_with_an_instance_of_cnpj_generator_options():
            def it_sets_the_generator_instance():
                utils = CnpjUtils()
                generator_options = CnpjGeneratorOptions()

                utils.generator = generator_options

                assert utils.generator.options is generator_options

        def describe_when_called_with_a_partial_object_with_options_to_the_generator_options():
            generator_options = {
                "format": True,
                "prefix": "12345678",
                "type": "numeric",
            }

            def it_sets_the_generator_instance_with_options():
                utils = CnpjUtils()

                utils.generator = generator_options

                for key, value in generator_options.items():
                    assert utils.generator.options.all[key] == value

            def it_sets_the_generator_instance_with_empty_object():
                utils = CnpjUtils()
                original_generator = utils.generator
                original_generator_options = original_generator.options.all

                utils.generator = {}

                assert utils.generator is not original_generator
                _assert_options_snapshots_match(
                    utils.generator.options.all,
                    original_generator_options,
                )

    def describe_validator_setter():
        def describe_when_called_with_a_complete_new_instance_of_cnpj_validator():
            def it_sets_the_validator_instance():
                utils = CnpjUtils()
                validator = CnpjValidator()

                utils.validator = validator

                assert utils.validator is validator

        def describe_when_called_with_an_instance_of_cnpj_validator_options():
            def it_sets_the_validator_instance():
                utils = CnpjUtils()
                validator_options = CnpjValidatorOptions()

                utils.validator = validator_options

                assert utils.validator.options is validator_options

        def describe_when_called_with_a_partial_object_with_options_to_the_validator_options():
            validator_options = {
                "case_sensitive": True,
                "type": "numeric",
            }

            def it_sets_the_validator_instance_with_options():
                utils = CnpjUtils()

                utils.validator = validator_options

                for key, value in validator_options.items():
                    assert utils.validator.options.all[key] == value

            def it_sets_the_validator_instance_with_empty_object():
                utils = CnpjUtils()
                original_validator = utils.validator
                original_validator_options = original_validator.options.all

                utils.validator = {}

                assert utils.validator is not original_validator
                _assert_options_snapshots_match(
                    utils.validator.options.all,
                    original_validator_options,
                )

    def describe_format_method():
        def describe_delegation():
            def it_invokes_the_formatter_method_with_the_same_arguments():
                utils = CnpjUtils()
                utils.formatter = MagicMock()
                options = CnpjFormatterOptions()
                cnpj = "AB123CDE000145"

                utils.format(cnpj, options)

                utils.formatter.format.assert_called_once_with(cnpj, options)

            def it_returns_the_formatted_cnpj():
                utils = CnpjUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.return_value = "formatted-cnpj"

                result = utils.format("12345678000190")

                assert result == "formatted-cnpj"

            def it_forwards_named_formatting_options():
                utils = CnpjUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.return_value = "12.345.678/0001-90"

                result = utils.format(
                    "12345678000190",
                    hidden=True,
                    hidden_key="X",
                    escape=True,
                    on_fail=lambda value: value,
                )

                assert result == "12.345.678/0001-90"
                utils.formatter.format.assert_called_once_with(
                    "12345678000190",
                    hidden=True,
                    hidden_key="X",
                    hidden_start=None,
                    hidden_end=None,
                    dot_key=None,
                    slash_key=None,
                    dash_key=None,
                    escape=True,
                    on_fail=ANY,
                )

            def it_throws_any_error_the_formatter_throws():
                utils = CnpjUtils()
                utils.formatter = MagicMock()
                utils.formatter.format.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.format("12345678000190")

        def it_applies_constructor_formatter_defaults_when_method_options_are_omitted():
            utils = CnpjUtils(
                formatter={
                    "hidden": True,
                    "hidden_key": "#",
                },
            )

            result = utils.format("12ABC34500DE99")

            assert "#" in result

        def describe_format_contexts():
            @pytest.mark.parametrize("format_cnpj", FORMAT_FACTORIES)
            def it_matches_cnpj_formatter_format_behavior(format_cnpj: FormatFn):
                input_value = "91415732000793"
                formatter = CnpjFormatter()

                result = format_cnpj(input_value)

                assert result == formatter.format(input_value)

            @pytest.mark.parametrize("format_cnpj", FORMAT_FACTORIES)
            def it_forwards_formatting_options(format_cnpj: FormatFn):
                input_value = "01ABC234000X56"
                slash_key = "|"

                result = format_cnpj(input_value, slash_key)

                assert result == f"01.ABC.234{slash_key}000X-56"

    def describe_generate_method():
        def describe_delegation():
            def it_invokes_the_generator_method_with_the_same_arguments():
                utils = CnpjUtils()
                utils.generator = MagicMock()
                options = CnpjGeneratorOptions()

                utils.generate(options)

                utils.generator.generate.assert_called_once_with(options)

            def it_returns_the_generated_cnpj():
                utils = CnpjUtils()
                utils.generator = MagicMock()
                utils.generator.generate.return_value = "generated-cnpj"

                result = utils.generate()

                assert result == "generated-cnpj"

            def it_forwards_named_generation_options():
                utils = CnpjUtils()
                utils.generator = MagicMock()
                utils.generator.generate.return_value = "12.345.678/0001-90"

                result = utils.generate(format=True, prefix="12345678")

                assert result == "12.345.678/0001-90"
                utils.generator.generate.assert_called_once_with(
                    format=True,
                    prefix="12345678",
                )

            def it_throws_any_error_the_generator_throws():
                utils = CnpjUtils()
                utils.generator = MagicMock()
                utils.generator.generate.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.generate()

        def describe_generate_contexts():
            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_matches_cnpj_generator_generate_behavior(generate: GenerateFn):
                generator = CnpjGenerator()

                result = generate()

                assert re.fullmatch(r"^[0-9A-Z]{14}$", result)
                assert len(result) == len(generator.generate())

            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_forwards_generation_options(generate: GenerateFn):
                result = generate(format=True, prefix="12345", type="numeric")

                assert re.fullmatch(r"^12\.345\.\d{3}/\d{4}-\d{2}$", result)

            @pytest.mark.parametrize("generate", GENERATE_FACTORIES)
            def it_returns_a_deterministic_cnpj_for_a_full_12_character_prefix(
                generate: GenerateFn,
            ):
                prefix = "123456780009"
                results = [generate(prefix=prefix) for _ in range(20)]

                assert len(set(results)) == 1

    def describe_is_valid_method():
        def describe_delegation():
            def it_invokes_the_validator_method_with_the_same_arguments():
                utils = CnpjUtils()
                utils.validator = MagicMock()
                options = CnpjValidatorOptions()
                cnpj = "AB123CDE000145"

                utils.is_valid(cnpj, options)

                utils.validator.is_valid.assert_called_once_with(cnpj, options)

            def it_returns_the_validation_result():
                utils = CnpjUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.return_value = True

                result = utils.is_valid("AB123CDE000145")

                assert result is True

            def it_returns_false_when_the_validator_returns_false():
                utils = CnpjUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.return_value = False

                result = utils.is_valid("12345678000199")

                assert result is False
                utils.validator.is_valid.assert_called_once_with("12345678000199")

            def it_throws_any_error_the_validator_throws():
                utils = CnpjUtils()
                utils.validator = MagicMock()
                utils.validator.is_valid.side_effect = RuntimeError("test error")

                with pytest.raises(RuntimeError, match="test error"):
                    utils.is_valid("AB123CDE000145")

        def describe_is_valid_contexts():
            @pytest.mark.parametrize("is_valid", IS_VALID_FACTORIES)
            def it_matches_cnpj_validator_is_valid_behavior(is_valid: IsValidFn):
                input_value = "91415732000793"
                validator = CnpjValidator()

                result = is_valid(input_value)

                assert result == validator.is_valid(input_value)

            @pytest.mark.parametrize("is_valid", IS_VALID_FACTORIES)
            def it_forwards_validation_options(is_valid: IsValidFn):
                input_value = "1QB5UKALPYFP59"

                assert is_valid(input_value, type="numeric") is False
                assert is_valid(input_value, type="alphanumeric") is True

            @pytest.mark.parametrize("is_valid", IS_VALID_FACTORIES)
            def it_validates_formatted_and_unformatted_cnpj_strings(
                is_valid: IsValidFn,
            ):
                assert is_valid("1QB5UKALPYFP59") is True
                assert is_valid("1QB5.UKAL.PYF/P59") is True
                assert is_valid("AB123CDE0001555") is False

    def describe_integration():
        def it_uses_the_correct_component_instances_for_all_methods():
            utils = CnpjUtils()
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
            utils = CnpjUtils()

            with pytest.raises(AttributeError):
                utils.new_attribute = "test"

            assert hasattr(utils, "formatter")
            assert hasattr(utils, "generator")
            assert hasattr(utils, "validator")
