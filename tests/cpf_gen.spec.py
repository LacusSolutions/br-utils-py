"""Behavioral spec for ``cpf_gen``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-gen/tests/cpf-gen.spec.ts``) and the PHP reference suite
(``php/packages/cpf-gen/tests/CpfGeneratorFunctionTest.php``), following the
business rules documented in ``AGENTS.md``.

Dropped from the JS suite: the ``spyOn(CpfGenerator.prototype, 'generate')`` test
(delegation is asserted via behavioral parity with ``CpfGenerator.generate``,
matching the PHP approach).
"""

import re

from cpf_gen import cpf_gen


def describe_cpf_gen():
    def describe_when_called():
        def it_matches_cpf_generator_generate_behavior():
            result = cpf_gen()

            assert re.fullmatch(r"\d{11}", result)

        def it_accepts_options_and_forwards_generating_behavior():
            options = {
                "format": True,
                "prefix": "12345",
            }

            # CPF groups as 3-3-3-2 (not CNPJ's 2-3-3/4-2); prefix "12345" → "123.45?.???-??"
            assert re.fullmatch(r"^123\.45\d\.\d{3}-\d{2}$", cpf_gen(options))
