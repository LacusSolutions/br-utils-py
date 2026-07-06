"""Behavioral spec for ``BrUtils``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/br-utils/tests/br-utils.spec.ts``) and the PHP reference suite
(``php/packages/br-utils/tests/specs/BrUtils.spec.php``), plus the ``__slots__``
and flat-options cases from the prior Python ``br_utils_init_test.py`` file,
following the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``js/packages/br-utils/tests/output.spec.ts`` distribution artifacts
  (UMD/CJS/ESM bundles, declaration files, global variable wiring, and export
  string parsing). Those concern JS packaging only.
- JavaScript ``undefined`` nullish values (Python uses ``None`` only).
- PHP ``getCpfUtils()`` / ``getCnpjUtils()`` accessor names (Python uses
  ``.cpf`` / ``.cnpj`` properties).
- PHP legacy CPF v1 ``InvalidArgumentException`` for formatter options (Python
  mirrors JS v2 structured exceptions).
- PHP ``phpunit/Cpf/*`` legacy CPF v1 component suites (Python aligns with
  ``cpf-utils`` v2, not PHP CPF v1).
"""

from __future__ import annotations

import pytest
from br_utils import BrUtils
from br_utils.cnpj import (
    CnpjFormatter,
    CnpjFormatterOptions,
    CnpjFormatterOptionsForbiddenKeyCharacterException,
    CnpjFormatterOptionsHiddenRangeInvalidException,
    CnpjGenerator,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptions,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjUtils,
    CnpjValidator,
    CnpjValidatorOptions,
    CnpjValidatorOptionTypeInvalidException,
)
from br_utils.cpf import (
    CpfFormatter,
    CpfFormatterOptions,
    CpfFormatterOptionsHiddenRangeInvalidException,
    CpfGenerator,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorOptions,
    CpfUtils,
    CpfValidator,
)


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key == "on_fail":
            assert actual[key] is expected_value
        else:
            assert actual[key] == expected_value


def _default_cpf_formatter_options_snapshot() -> dict:
    return CpfFormatterOptions().all


def _default_cpf_generator_options_snapshot() -> dict:
    return CpfGeneratorOptions().all


def _default_cnpj_formatter_options_snapshot() -> dict:
    return CnpjFormatterOptions().all


def _default_cnpj_generator_options_snapshot() -> dict:
    return CnpjGeneratorOptions().all


def _default_cnpj_validator_options_snapshot() -> dict:
    return CnpjValidatorOptions().all


def describe_br_utils():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_necessary_resource_instances():
                utils = BrUtils()

                assert isinstance(utils.cnpj, CnpjUtils)
                assert isinstance(utils.cpf, CpfUtils)

            def it_creates_an_instance_with_default_options():
                utils = BrUtils()

                _assert_options_snapshots_match(
                    utils.cpf.formatter.options.all,
                    _default_cpf_formatter_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.cpf.generator.options.all,
                    _default_cpf_generator_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.cnpj.formatter.options.all,
                    _default_cnpj_formatter_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.cnpj.generator.options.all,
                    _default_cnpj_generator_options_snapshot(),
                )
                _assert_options_snapshots_match(
                    utils.cnpj.validator.options.all,
                    _default_cnpj_validator_options_snapshot(),
                )

        def describe_when_called_with_instances_of_resources():
            def it_uses_the_passed_cnpj_utils_directly():
                cnpj_utils = CnpjUtils()

                utils = BrUtils(cnpj=cnpj_utils)

                assert isinstance(utils.cnpj, CnpjUtils)
                assert utils.cnpj is cnpj_utils

            def it_uses_the_passed_cpf_utils_directly():
                cpf_utils = CpfUtils()

                utils = BrUtils(cpf=cpf_utils)

                assert isinstance(utils.cpf, CpfUtils)
                assert utils.cpf is cpf_utils

            def it_uses_the_passed_resources_directly():
                cnpj_utils = CnpjUtils()
                cpf_utils = CpfUtils()

                utils = BrUtils(cnpj=cnpj_utils, cpf=cpf_utils)

                assert utils.cnpj is cnpj_utils
                assert utils.cpf is cpf_utils

        def describe_when_called_with_literal_object_parameters():
            cnpj_utils_options = {
                "formatter": {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 8,
                    "hidden_end": 11,
                    "dot_key": "_",
                    "slash_key": "|",
                    "dash_key": " dv ",
                },
                "generator": {
                    "format": True,
                    "prefix": "12345678",
                    "type": "numeric",
                },
                "validator": {
                    "type": "numeric",
                },
            }

            def it_creates_a_new_br_utils_instance_with_the_cnpj_options():
                utils = BrUtils(cnpj=cnpj_utils_options)

                assert isinstance(utils.cnpj, CnpjUtils)
                assert isinstance(utils.cnpj.formatter, CnpjFormatter)
                assert isinstance(utils.cnpj.formatter.options, CnpjFormatterOptions)
                for key, value in cnpj_utils_options["formatter"].items():
                    assert utils.cnpj.formatter.options.all[key] == value
                assert isinstance(utils.cnpj.generator, CnpjGenerator)
                assert isinstance(utils.cnpj.generator.options, CnpjGeneratorOptions)
                for key, value in cnpj_utils_options["generator"].items():
                    assert utils.cnpj.generator.options.all[key] == value
                assert isinstance(utils.cnpj.validator, CnpjValidator)
                assert isinstance(utils.cnpj.validator.options, CnpjValidatorOptions)
                for key, value in cnpj_utils_options["validator"].items():
                    assert utils.cnpj.validator.options.all[key] == value

            cpf_utils_options = {
                "formatter": {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 8,
                    "hidden_end": 10,
                    "dot_key": "_",
                    "dash_key": " dv ",
                },
                "generator": {
                    "format": True,
                    "prefix": "12345678",
                },
            }

            def it_creates_a_new_br_utils_instance_with_the_cpf_options():
                utils = BrUtils(cpf=cpf_utils_options)

                assert isinstance(utils.cpf, CpfUtils)
                assert isinstance(utils.cpf.formatter, CpfFormatter)
                assert isinstance(utils.cpf.formatter.options, CpfFormatterOptions)
                for key, value in cpf_utils_options["formatter"].items():
                    assert utils.cpf.formatter.options.all[key] == value
                assert isinstance(utils.cpf.generator, CpfGenerator)
                assert isinstance(utils.cpf.generator.options, CpfGeneratorOptions)
                for key, value in cpf_utils_options["generator"].items():
                    assert utils.cpf.generator.options.all[key] == value

        def describe_when_called_with_flat_formatter_and_generator_options():
            def it_applies_cpf_formatter_options():
                formatter_options = CpfFormatterOptions(hidden=True, hidden_key="X")
                utils = BrUtils(cpf_formatter=formatter_options)
                result = utils.cpf.format("12345678901")

                assert utils.cpf.formatter.options is formatter_options
                assert result == "123.XXX.XXX-XX"

            def it_applies_cpf_generator_options():
                generator_options = CpfGeneratorOptions(format=True, prefix="123456789")
                utils = BrUtils(cpf_generator=generator_options)
                result = utils.cpf.generate()

                assert utils.cpf.generator.options is generator_options
                assert result.startswith("123.456.789-")

            def it_applies_cnpj_formatter_options():
                formatter_options = CnpjFormatterOptions(hidden=True, hidden_key="X")
                utils = BrUtils(cnpj_formatter=formatter_options)
                result = utils.cnpj.format("11222333000181")

                assert utils.cnpj.formatter.options is formatter_options
                assert result == "11.222.XXX/XXXX-XX"

            def it_applies_cnpj_generator_options():
                generator_options = CnpjGeneratorOptions(format=True, prefix="11222333")
                utils = BrUtils(cnpj_generator=generator_options)
                result = utils.cnpj.generate()

                assert utils.cnpj.generator.options is generator_options
                assert result.startswith("11.222.333/")

            def it_applies_all_flat_options_together():
                cpf_fmt_opts = CpfFormatterOptions(hidden=True)
                cpf_gen_opts = CpfGeneratorOptions(format=True)
                cnpj_fmt_opts = CnpjFormatterOptions(hidden=True)
                cnpj_gen_opts = CnpjGeneratorOptions(format=True)

                utils = BrUtils(
                    cpf_formatter=cpf_fmt_opts,
                    cpf_generator=cpf_gen_opts,
                    cnpj_formatter=cnpj_fmt_opts,
                    cnpj_generator=cnpj_gen_opts,
                )

                assert utils.cpf.formatter.options is cpf_fmt_opts
                assert utils.cpf.generator.options is cpf_gen_opts
                assert utils.cnpj.formatter.options is cnpj_fmt_opts
                assert utils.cnpj.generator.options is cnpj_gen_opts

        def describe_when_called_with_arguments():
            def it_configures_cpfs_formatter_and_generator_from_dicts():
                formatter_options = {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 8,
                    "hidden_end": 10,
                    "dot_key": "_",
                    "dash_key": " dv ",
                }
                generator_options = {"format": True, "prefix": "12345678"}

                utils = BrUtils(
                    cpf={
                        "formatter": formatter_options,
                        "generator": generator_options,
                    }
                )

                for key, value in formatter_options.items():
                    assert utils.cpf.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.cpf.generator.options.all[key] == value

            def it_configures_cnpjs_formatter_generator_and_validator_from_dicts():
                formatter_options = {"slash_key": "|"}
                generator_options = {"format": True, "prefix": "12345"}
                validator_options = {"type": "numeric", "case_sensitive": False}

                utils = BrUtils(
                    cnpj={
                        "formatter": formatter_options,
                        "generator": generator_options,
                        "validator": validator_options,
                    }
                )

                for key, value in formatter_options.items():
                    assert utils.cnpj.formatter.options.all[key] == value
                for key, value in generator_options.items():
                    assert utils.cnpj.generator.options.all[key] == value
                for key, value in validator_options.items():
                    assert utils.cnpj.validator.options.all[key] == value

            def it_uses_provided_options_instances_directly():
                cnpj_formatter_options = CnpjFormatterOptions()
                cnpj_generator_options = CnpjGeneratorOptions()
                cnpj_validator_options = CnpjValidatorOptions()

                utils = BrUtils(
                    cnpj={
                        "formatter": cnpj_formatter_options,
                        "generator": cnpj_generator_options,
                        "validator": cnpj_validator_options,
                    }
                )

                assert utils.cnpj.formatter.options is cnpj_formatter_options
                assert utils.cnpj.generator.options is cnpj_generator_options
                assert utils.cnpj.validator.options is cnpj_validator_options

            def it_mutates_shared_options_instances_and_affects_later_calls():
                cnpj_formatter_options = CnpjFormatterOptions()
                utils = BrUtils(cnpj={"formatter": cnpj_formatter_options})

                cnpj_formatter_options.dash_key = "|"

                assert utils.cnpj.formatter.options.all["dash_key"] == "|"

        def describe_when_called_with_invalid_options():
            def it_raises_cpf_formatter_exceptions_for_invalid_formatter_options():
                with pytest.raises(CpfFormatterOptionsHiddenRangeInvalidException):
                    BrUtils(cpf={"formatter": {"hidden_start": -1}})

            def it_raises_cpf_generator_exceptions_for_invalid_generator_options():
                with pytest.raises(CpfGeneratorOptionPrefixInvalidException):
                    BrUtils(cpf={"generator": {"prefix": "000000000"}})

            def it_raises_cnpj_formatter_exceptions_for_invalid_formatter_options():
                with pytest.raises(CnpjFormatterOptionsHiddenRangeInvalidException):
                    BrUtils(cnpj={"formatter": {"hidden_start": -1}})

                with pytest.raises(CnpjFormatterOptionsForbiddenKeyCharacterException):
                    BrUtils(cnpj={"formatter": {"dash_key": "\u00e5"}})

            def it_raises_cnpj_generator_exceptions_for_invalid_generator_options():
                with pytest.raises(CnpjGeneratorOptionPrefixInvalidException):
                    BrUtils(cnpj={"generator": {"prefix": "00000000"}})

                with pytest.raises(CnpjGeneratorOptionTypeInvalidException):
                    BrUtils(cnpj={"generator": {"type": "invalid"}})

                with pytest.raises(CnpjGeneratorOptionsTypeError):
                    BrUtils(cnpj={"generator": {"prefix": 123}})

            def it_raises_cnpj_validator_exceptions_for_invalid_validator_options():
                with pytest.raises(CnpjValidatorOptionTypeInvalidException):
                    BrUtils(cnpj={"validator": {"type": "invalid"}})

    def describe_cnpj_setter():
        def describe_when_called_with_a_complete_new_instance_of_cnpj_utils():
            def it_sets_the_cnpj_utils_instance():
                utils = BrUtils()
                cnpj_utils = CnpjUtils()

                utils.cnpj = cnpj_utils

                assert utils.cnpj is cnpj_utils

        def describe_when_called_with_literal_object_parameters():
            cnpj_utils_options = {
                "formatter": {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 8,
                    "hidden_end": 11,
                    "dot_key": "_",
                    "slash_key": "|",
                    "dash_key": " dv ",
                },
                "generator": {
                    "format": True,
                    "prefix": "12345678",
                    "type": "numeric",
                },
                "validator": {
                    "type": "numeric",
                },
            }

            def it_sets_the_cnpj_utils_instance_with_options():
                utils = BrUtils()

                utils.cnpj = cnpj_utils_options

                assert isinstance(utils.cnpj, CnpjUtils)
                for key, value in cnpj_utils_options["formatter"].items():
                    assert utils.cnpj.formatter.options.all[key] == value
                for key, value in cnpj_utils_options["generator"].items():
                    assert utils.cnpj.generator.options.all[key] == value
                for key, value in cnpj_utils_options["validator"].items():
                    assert utils.cnpj.validator.options.all[key] == value

        def describe_when_called_with_none():
            def it_creates_a_new_cnpj_utils_instance_with_default_options():
                utils = BrUtils()
                original_cnpj_utils = utils.cnpj

                utils.cnpj = None

                assert isinstance(utils.cnpj, CnpjUtils)
                assert utils.cnpj is not original_cnpj_utils

    def describe_cpf_setter():
        def describe_when_called_with_a_complete_new_instance_of_cpf_utils():
            def it_sets_the_cpf_utils_instance():
                utils = BrUtils()
                cpf_utils = CpfUtils()

                utils.cpf = cpf_utils

                assert utils.cpf is cpf_utils

        def describe_when_called_with_literal_object_parameters():
            cpf_utils_options = {
                "formatter": {
                    "hidden": True,
                    "hidden_key": "#",
                    "hidden_start": 8,
                    "hidden_end": 10,
                    "dot_key": "_",
                    "dash_key": " dv ",
                },
                "generator": {
                    "format": True,
                    "prefix": "12345678",
                },
            }

            def it_sets_the_cpf_utils_instance_with_options():
                utils = BrUtils()

                utils.cpf = cpf_utils_options

                assert isinstance(utils.cpf, CpfUtils)
                for key, value in cpf_utils_options["formatter"].items():
                    assert utils.cpf.formatter.options.all[key] == value
                for key, value in cpf_utils_options["generator"].items():
                    assert utils.cpf.generator.options.all[key] == value

        def describe_when_called_with_none():
            def it_creates_a_new_cpf_utils_instance_with_default_options():
                utils = BrUtils()
                original_cpf_utils = utils.cpf

                utils.cpf = None

                assert isinstance(utils.cpf, CpfUtils)
                assert utils.cpf is not original_cpf_utils

    def describe_resource_accessors():
        def it_returns_the_cpf_utils_instance():
            utils = BrUtils()

            assert isinstance(utils.cpf, CpfUtils)

        def it_returns_the_cpf_formatter_instance():
            utils = BrUtils()

            assert isinstance(utils.cpf.formatter, CpfFormatter)

        def it_returns_the_cpf_generator_instance():
            utils = BrUtils()

            assert isinstance(utils.cpf.generator, CpfGenerator)

        def it_returns_the_cpf_validator_instance():
            utils = BrUtils()

            assert isinstance(utils.cpf.validator, CpfValidator)

        def it_returns_the_cnpj_utils_instance():
            utils = BrUtils()

            assert isinstance(utils.cnpj, CnpjUtils)

        def it_returns_the_cnpj_formatter_instance():
            utils = BrUtils()

            assert isinstance(utils.cnpj.formatter, CnpjFormatter)

        def it_returns_the_cnpj_generator_instance():
            utils = BrUtils()

            assert isinstance(utils.cnpj.generator, CnpjGenerator)

        def it_returns_the_cnpj_validator_instance():
            utils = BrUtils()

            assert isinstance(utils.cnpj.validator, CnpjValidator)

    def describe_slots():
        def it_restricts_dynamic_attributes():
            utils = BrUtils()

            with pytest.raises(AttributeError):
                utils.new_attribute = "test"

            assert hasattr(utils, "cpf")
            assert hasattr(utils, "cnpj")
