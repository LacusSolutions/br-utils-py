"""Behavioral spec for ``cpf_val``.

Mirrors the JavaScript reference suite
(``js/packages/cpf-val/tests/cpf-val.spec.ts``) and the PHP reference suite
(``php/packages/cpf-val/tests/CpfValidatorFunctionTest.php``), following the
business rules documented in ``AGENTS.md``.

Kept parallel with the CNPJ mirror
(``python/packages/cnpj-val/tests/cnpj_val.spec.py``) via
``it_matches_..._is_valid_behavior``; the CNPJ ``options`` / named-argument
forwarding scenarios are intentionally absent (the CPF helper takes only the
input — see ``AGENTS.md`` §3 and §9.3).

Dropped from the JS suite: the ``spyOn(CpfValidator.prototype, 'isValid')`` test
(delegation is asserted via behavioral parity with ``CpfValidator.is_valid``,
matching the PHP approach and the Python ``cnpj-val`` mirror).
"""

from cpf_val import CpfValidator, cpf_val


def describe_cpf_val():
    def describe_when_called():
        def it_matches_cpf_validator_is_valid_behavior():
            input_value = "82911017366"
            validator = CpfValidator()

            assert cpf_val(input_value) == validator.is_valid(input_value)

        def it_returns_true_for_a_valid_cpf():
            assert cpf_val("82911017366") is True

        def it_returns_false_for_an_invalid_cpf():
            assert cpf_val("33528612691") is False
