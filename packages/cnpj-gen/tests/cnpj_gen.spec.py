"""Behavioral spec for ``cnpj_gen``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-gen/tests/cnpj-gen.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-gen/tests/specs/cnpj-gen.spec.php``), following the
business rules documented in ``AGENTS.md``.

Dropped from the JS suite: the ``spyOn(CnpjGenerator.prototype, 'generate')`` test
(delegation is asserted via behavioral parity with ``CnpjGenerator.generate``,
matching the PHP approach).
"""

import re

from cnpj_gen import cnpj_gen


def describe_cnpj_gen():
    def describe_when_called():
        def it_matches_cnpj_generator_generate_behavior():
            result = cnpj_gen()

            assert re.fullmatch(r"[0-9A-Z]{14}", result)

        def it_accepts_options_and_forwards_generating_behavior():
            options = {
                "format": True,
                "prefix": "12345",
                "type": "numeric",
            }

            assert re.fullmatch(r"^12\.345\.\d{3}/\d{4}-\d{2}$", cnpj_gen(options))
