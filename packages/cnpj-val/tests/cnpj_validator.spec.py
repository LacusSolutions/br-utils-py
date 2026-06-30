"""Behavioral spec for ``CnpjValidator``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-val/tests/cnpj-validator.spec.ts``) and the PHP reference
suite (``php/packages/cnpj-val/tests/specs/CnpjValidator.spec.php``), following
the business rules documented in ``AGENTS.md``.

Dropped cases:
- ``undefined`` input type (JavaScript-only; Python uses ``None`` with
  ``actual_type`` ``"NoneType"`` via ``lacus.utils.describe_type``).
- PHP named constructor / per-call ``type`` / ``caseSensitive`` keyword arguments
  (PHP-only API shape; Python follows the JS options-object model).
"""

import re
from collections.abc import Callable, Sequence
from typing import Any

import pytest
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptions,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
)

IsValidFn = Callable[..., bool]
ValidatorFactory = Callable[[dict[str, Any]], IsValidFn]

REPEATED_DIGIT_PREFIXES = [
    "111111111111",
    "222222222222",
    "333333333333",
    "444444444444",
    "555555555555",
    "666666666666",
    "777777777777",
    "888888888888",
    "999999999999",
]

INVALID_INPUT_CASES = [
    (None, "NoneType"),
    (42, "integer number"),
    (3.14, "float number"),
    (True, "boolean"),
    ({}, "dict"),
    ([1, 2, 3], "number[]"),
]


def _default_options_snapshot() -> dict:
    return CnpjValidatorOptions().all


def _assert_options_snapshots_match(actual: dict, expected: dict) -> None:
    assert actual == expected


def _create_inputs_set(cnpj: str) -> list[tuple[str, str | Sequence[str]]]:
    unformatted_string = cnpj
    formatted_string = re.sub(
        r"([0-9A-Z]{2})([0-9A-Z]{3})([0-9A-Z]{3})([0-9A-Z]{4})(\d+)",
        r"\1.\2.\3/\4-\5",
        cnpj,
        flags=re.IGNORECASE,
    )
    unformatted_array = list(unformatted_string)
    formatted_array = list(formatted_string)
    grouped_array = re.split(r"[./-]", formatted_string)

    return [
        ("string", unformatted_string),
        ("formatted string", formatted_string),
        ("array", unformatted_array),
        ("formatted array", formatted_array),
        ("grouped array", grouped_array),
    ]


def _create_validator_with_literal_options_in_constructor(
    options: dict[str, Any],
) -> IsValidFn:
    validator = CnpjValidator(options)

    def is_valid(
        cnpj_input: str | Sequence[str],
        options_override: Any = None,
    ) -> bool:
        return validator.is_valid(cnpj_input, options_override)

    return is_valid


def _create_validator_with_options_instance_in_constructor(
    options: dict[str, Any],
) -> IsValidFn:
    validator_options = CnpjValidatorOptions(options)
    validator = CnpjValidator(validator_options)

    def is_valid(
        cnpj_input: str | Sequence[str],
        options_override: Any = None,
    ) -> bool:
        return validator.is_valid(cnpj_input, options_override)

    return is_valid


def _create_validator_with_literal_options_in_method(
    options: dict[str, Any],
) -> IsValidFn:
    validator = CnpjValidator()

    def is_valid(
        cnpj_input: str | Sequence[str],
        options_override: Any = None,
    ) -> bool:
        if options_override is None:
            return validator.is_valid(cnpj_input, options)
        if isinstance(options_override, CnpjValidatorOptions):
            return validator.is_valid(
                cnpj_input,
                CnpjValidatorOptions(options, options_override),
            )
        return validator.is_valid(cnpj_input, {**options, **options_override})

    return is_valid


def _create_validator_with_options_instance_in_method(
    options: dict[str, Any],
) -> IsValidFn:
    validator = CnpjValidator()

    def is_valid(
        cnpj_input: str | Sequence[str],
        options_override: Any = None,
    ) -> bool:
        validator_options = CnpjValidatorOptions(
            options,
            options_override if options_override is not None else {},
        )
        return validator.is_valid(cnpj_input, validator_options)

    return is_valid


IS_VALID_FACTORIES = [
    pytest.param(
        _create_validator_with_literal_options_in_constructor,
        id="constructor_literal",
    ),
    pytest.param(
        _create_validator_with_options_instance_in_constructor,
        id="constructor_options",
    ),
    pytest.param(
        _create_validator_with_literal_options_in_method,
        id="method_literal",
    ),
    pytest.param(
        _create_validator_with_options_instance_in_method,
        id="method_options",
    ),
]


def describe_cnpj_validator():
    def describe_constructor():
        def describe_when_called_with_no_arguments():
            def it_creates_an_instance_with_default_options():
                validator = CnpjValidator()

                _assert_options_snapshots_match(
                    validator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_an_empty_object():
            def it_creates_an_instance_with_default_options():
                validator = CnpjValidator({})

                _assert_options_snapshots_match(
                    validator.options.all,
                    _default_options_snapshot(),
                )

        def describe_when_called_with_a_cnpj_validator_options_instance():
            def it_uses_that_instance_directly_without_copying():
                options = CnpjValidatorOptions(
                    {
                        "case_sensitive": False,
                        "type": "numeric",
                    }
                )
                validator = CnpjValidator(options)

                assert validator.options is options
                _assert_options_snapshots_match(
                    validator.options.all,
                    options.all,
                )

            def it_mutations_to_the_instance_affect_future_is_valid_calls():
                options = CnpjValidatorOptions(
                    {
                        "case_sensitive": False,
                        "type": "numeric",
                    }
                )
                validator = CnpjValidator(options)

                options.case_sensitive = True
                options.type = "alphanumeric"

                assert validator.options.case_sensitive is True
                assert validator.options.type == "alphanumeric"

        def describe_when_called_with_a_literal_options_object():
            def it_creates_a_new_cnpj_validator_options_instance_from_the_provided_values():
                input_options = {
                    "case_sensitive": False,
                    "type": "numeric",
                }
                validator = CnpjValidator(input_options)

                assert isinstance(validator.options, CnpjValidatorOptions)
                assert validator.options.case_sensitive is False
                assert validator.options.type == "numeric"

        def describe_when_called_with_invalid_options():
            def it_throws_cnpj_validator_option_type_invalid_exception_for_invalid_type():
                with pytest.raises(CnpjValidatorOptionTypeInvalidException):
                    CnpjValidator({"type": "invalid"})

            def it_throws_cnpj_validator_options_type_error_for_non_string_type():
                with pytest.raises(CnpjValidatorOptionsTypeError):
                    CnpjValidator({"type": 123})  # type: ignore[dict-item]

    def describe_is_valid_method():
        def describe_when_no_options_are_passed():
            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("1QB5UKALPYFP59"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_valid_cnpj_with_numbers_and_uppercase_letters(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({})

                assert is_valid(input_value) is True

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("96206256120884"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_valid_cnpj_with_only_numbers(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({})

                assert is_valid(input_value) is True

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("1QB5UKALpyfp59"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_valid_cnpj_with_numbers_and_lowercase_letters(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({})

                assert is_valid(input_value) is False

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("AB123CDE00015"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_cnpj_with_less_than_14_digits(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({})

                assert is_valid(input_value) is False

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("AB123CDE0001555"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_cnpj_with_more_than_14_digits(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({})

                assert is_valid(input_value) is False

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            def it_returns_false_for_a_cnpj_with_base_id_all_zeros(
                create_validator,
            ):
                is_valid = create_validator({})

                for index in range(100):
                    input_value = f"00000000A001{index:02d}"

                    assert is_valid(input_value) is False

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            def it_returns_false_for_a_cnpj_with_branch_id_all_zeros(
                create_validator,
            ):
                is_valid = create_validator({})

                for index in range(100):
                    input_value = f"AB123CDE0000{index:02d}"

                    assert is_valid(input_value) is False

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize("prefix", REPEATED_DIGIT_PREFIXES)
            def it_returns_false_for_a_cnpj_with_all_digits_the_same(
                create_validator,
                prefix,
            ):
                is_valid = create_validator({})

                for index in range(100):
                    input_value = f"{prefix}{index:02d}"

                    assert is_valid(input_value) is False

        def describe_when_case_sensitive_option_is_false():
            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("1QB5UKALpyfp59"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_valid_cnpj_with_numbers_and_lowercase_letters(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({"case_sensitive": False})

                assert is_valid(input_value) is True

        def describe_when_type_option_is_numeric():
            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("96206256120884"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_valid_cnpj_with_only_numbers(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({"type": "numeric"})

                assert is_valid(input_value) is True

            @pytest.mark.parametrize("create_validator", IS_VALID_FACTORIES)
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("1QB5UKALPYFP59"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_valid_cnpj_with_numbers_and_uppercase_letters(
                create_validator,
                _input_type,
                input_value,
            ):
                is_valid = create_validator({"type": "numeric"})

                assert is_valid(input_value) is False

        def describe_when_called_with_invalid_arguments():
            @pytest.mark.parametrize(
                ("input_value", "actual_type"), INVALID_INPUT_CASES
            )
            def it_raises_cnpj_validator_input_type_error(input_value, actual_type):
                validator = CnpjValidator()

                with pytest.raises(CnpjValidatorInputTypeError) as exc_info:
                    validator.is_valid(input_value)  # type: ignore[arg-type]

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input is input_value
                assert error.actual_type == actual_type
                assert (
                    str(error)
                    == f"CNPJ input must be of type string or string[]. Got {actual_type}."
                )
