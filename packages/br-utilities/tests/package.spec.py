"""Spec for the public API surface of the ``br_utils`` package.

Combines the default-instance case from ``js/packages/br-utils/tests/br-utils.spec.ts``
and the re-export smoke tests from the prior Python ``br_utils_reexports_test.py`` /
``br_utils_init_test.py`` files, following ``AGENTS.md``.

Dropped from the JS suite:
- ``js/packages/br-utils/tests/output.spec.ts`` distribution artifacts (UMD/CJS/ESM
  bundles, declaration files, global variable wiring, and export string parsing).
  Those concern JS packaging only.
- Root-level re-exports of ``cpf_fmt``, ``cnpj_fmt``, and component classes (Python
  exposes them via ``br_utils.cpf`` / ``br_utils.cnpj`` submodules per ``AGENTS.md`` §6.3).
"""

import br_utils as br_utils_module
from br_utils import BrUtils, CnpjUtils, CpfUtils, br_utils, cnpj_utils, cpf_utils


def describe_the_br_utils_package_api():
    def describe_default_instance():
        def it_exports_an_instance_of_br_utils_class():
            assert isinstance(br_utils, BrUtils)

        def it_exposes_cpf_and_cnpj_utilities():
            assert isinstance(br_utils.cpf, CpfUtils)
            assert isinstance(br_utils.cnpj, CnpjUtils)

    def describe_when_inspecting_top_level_names():
        def it_exports_the_documented_public_symbols():
            assert set(br_utils_module.__all__) == {
                "BrUtils",
                "CnpjUtils",
                "CpfUtils",
                "br_utils",
                "cnpj_utils",
                "cpf_utils",
            }

        def it_exports_singleton_instances_from_dependencies():
            assert isinstance(cpf_utils, CpfUtils)
            assert isinstance(cnpj_utils, CnpjUtils)

    def describe_cpf_submodule_reexports():
        def it_exports_all_public_cpf_resources():
            from br_utils.cpf import (
                CpfFormatter,
                CpfFormatterException,
                CpfFormatterInputLengthException,
                CpfFormatterInputTypeError,
                CpfFormatterOptions,
                CpfFormatterOptionsForbiddenKeyCharacterException,
                CpfFormatterOptionsHiddenRangeInvalidException,
                CpfFormatterOptionsTypeError,
                CpfFormatterTypeError,
                CpfGenerator,
                CpfGeneratorException,
                CpfGeneratorOptionPrefixInvalidException,
                CpfGeneratorOptions,
                CpfGeneratorOptionsTypeError,
                CpfGeneratorTypeError,
                CpfUtils,
                CpfValidator,
                cpf_fmt,
                cpf_gen,
                cpf_utils,
                cpf_val,
            )

            assert CpfFormatter is not None
            assert CpfFormatterException is not None
            assert CpfFormatterInputLengthException is not None
            assert CpfFormatterInputTypeError is not None
            assert CpfFormatterOptions is not None
            assert CpfFormatterOptionsForbiddenKeyCharacterException is not None
            assert CpfFormatterOptionsHiddenRangeInvalidException is not None
            assert CpfFormatterOptionsTypeError is not None
            assert CpfFormatterTypeError is not None
            assert CpfGenerator is not None
            assert CpfGeneratorException is not None
            assert CpfGeneratorOptionPrefixInvalidException is not None
            assert CpfGeneratorOptions is not None
            assert CpfGeneratorOptionsTypeError is not None
            assert CpfGeneratorTypeError is not None
            assert CpfUtils is not None
            assert CpfValidator is not None
            assert cpf_fmt is not None
            assert cpf_gen is not None
            assert cpf_utils is not None
            assert cpf_val is not None

    def describe_cnpj_submodule_reexports():
        def it_exports_all_public_cnpj_resources():
            from br_utils.cnpj import (
                CnpjFormatter,
                CnpjFormatterException,
                CnpjFormatterInputLengthException,
                CnpjFormatterInputTypeError,
                CnpjFormatterOptions,
                CnpjFormatterOptionsForbiddenKeyCharacterException,
                CnpjFormatterOptionsHiddenRangeInvalidException,
                CnpjFormatterOptionsTypeError,
                CnpjFormatterTypeError,
                CnpjGenerator,
                CnpjGeneratorException,
                CnpjGeneratorOptionPrefixInvalidException,
                CnpjGeneratorOptions,
                CnpjGeneratorOptionsTypeError,
                CnpjGeneratorOptionTypeInvalidException,
                CnpjGeneratorTypeError,
                CnpjUtils,
                CnpjValidator,
                CnpjValidatorException,
                CnpjValidatorInputTypeError,
                CnpjValidatorOptions,
                CnpjValidatorOptionsTypeError,
                CnpjValidatorOptionTypeInvalidException,
                CnpjValidatorTypeError,
                cnpj_fmt,
                cnpj_gen,
                cnpj_utils,
                cnpj_val,
            )

            assert CnpjFormatter is not None
            assert CnpjFormatterException is not None
            assert CnpjFormatterInputLengthException is not None
            assert CnpjFormatterInputTypeError is not None
            assert CnpjFormatterOptions is not None
            assert CnpjFormatterOptionsForbiddenKeyCharacterException is not None
            assert CnpjFormatterOptionsHiddenRangeInvalidException is not None
            assert CnpjFormatterOptionsTypeError is not None
            assert CnpjFormatterTypeError is not None
            assert CnpjGenerator is not None
            assert CnpjGeneratorException is not None
            assert CnpjGeneratorOptionPrefixInvalidException is not None
            assert CnpjGeneratorOptionTypeInvalidException is not None
            assert CnpjGeneratorOptions is not None
            assert CnpjGeneratorOptionsTypeError is not None
            assert CnpjGeneratorTypeError is not None
            assert CnpjUtils is not None
            assert CnpjValidator is not None
            assert CnpjValidatorException is not None
            assert CnpjValidatorInputTypeError is not None
            assert CnpjValidatorOptions is not None
            assert CnpjValidatorOptionsTypeError is not None
            assert CnpjValidatorOptionTypeInvalidException is not None
            assert CnpjValidatorTypeError is not None
            assert cnpj_fmt is not None
            assert cnpj_gen is not None
            assert cnpj_utils is not None
            assert cnpj_val is not None
