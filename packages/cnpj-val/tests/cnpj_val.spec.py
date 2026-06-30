"""Behavioral spec for ``cnpj_val``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-val/tests/cnpj-val.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-val/tests/specs/cnpj-val.spec.php``), following the
business rules documented in ``AGENTS.md``.

Dropped from the JS suite: the ``spyOn(CnpjValidator.prototype, 'isValid')`` test
(delegation is asserted via behavioral parity with ``CnpjValidator.is_valid``,
matching the PHP approach).
"""

from cnpj_val import CnpjValidator, cnpj_val


def describe_cnpj_val():
    def describe_when_called():
        def it_matches_cnpj_validator_is_valid_behavior():
            input_value = "91415732000793"
            validator = CnpjValidator()

            assert cnpj_val(input_value) == validator.is_valid(input_value)

        def it_accepts_options_and_forwards_validation_behavior():
            input_value = "01ABC234000X56"
            options = {"type": "numeric"}

            assert cnpj_val(input_value, options) is False

    def describe_when_called_with_named_options():
        input_value = "9jn7mgljzxio50"

        def it_forwards_type_to_the_validator():
            assert cnpj_val(input_value, type="numeric") == CnpjValidator(
                type="numeric"
            ).is_valid(input_value)

            assert cnpj_val(input_value, type="numeric") is False

        def it_forwards_case_sensitive_to_the_validator():
            assert cnpj_val(input_value, case_sensitive=False) == CnpjValidator(
                case_sensitive=False
            ).is_valid(input_value)

            assert cnpj_val(input_value, case_sensitive=False) is True

        def it_combines_options_mapping_with_named_overrides():
            assert cnpj_val(
                input_value,
                {"type": "alphanumeric"},
                case_sensitive=False,
            ) == CnpjValidator(
                {"type": "alphanumeric"},
                case_sensitive=False,
            ).is_valid(
                input_value
            )
