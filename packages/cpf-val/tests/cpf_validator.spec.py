"""Behavioral spec for ``CpfValidator``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-val/tests/cpf-validator.spec.ts``) and the PHP reference
suite (``php/packages/cpf-val/tests/CpfValidatorTestCases.php``, exercised by
both ``CpfValidatorClassTest`` and ``CpfValidatorFunctionTest``), following the
business rules documented in ``AGENTS.md``. The legacy ``*_test.py`` cases that
previously lived in this directory are folded in here.

Parallel naming with the CNPJ mirror
(``python/packages/cnpj-val/tests/cnpj_validator.spec.py``) is preserved for the
shared scenario shapes (``describe_is_valid_method``, ``_create_inputs_set``,
``it_returns_false_for_a_cpf_with_all_digits_the_same``,
``it_raises_..._input_type_error``); CNPJ-only ``options`` / ``type`` /
``case_sensitive`` scenarios are intentionally absent (CPF has no options).

Dropped cases:
- JS ``undefined`` input: Python has no ``undefined``; the ``None`` case already
  covers the nullish input (``actual_type`` ``"NoneType"`` via
  ``lacus.utils.describe_type``).
- PHP native ``TypeError`` variants for ``true`` / ``false`` / ``INF`` / closure:
  PHP raises those from its ``string`` parameter declaration. Python mirrors the
  JS model and raises ``CpfValidatorInputTypeError`` for the same non-``str`` /
  non-``Sequence[str]`` inputs; the boolean, float, object and array-of-numbers
  cases already represent that behavior, so the redundant PHP-only variants are
  dropped.
- PHP's acceptance of repeated-digit CPFs is NOT mirrored: per ``AGENTS.md`` §8.1
  the Python target follows JS and rejects all-identical-digit CPFs.
"""

import re

import pytest
from cpf_val import CpfValidator, CpfValidatorInputTypeError

REPEATED_DIGIT_PREFIXES = [
    "000000000",
    "111111111",
    "222222222",
    "333333333",
    "444444444",
    "555555555",
    "666666666",
    "777777777",
    "888888888",
    "999999999",
]

VALID_CPF_SAMPLES = [
    "82911017366",
    "33528612690",
    "86244870050",
    "22312659077",
    "96215666068",
    "67107095072",
    "48039958008",
    "20954431014",
    "11144477735",
    "12345678909",
    "97705597411",
    "71699299960",
    "35449963599",
    "43571251113",
    "43603425197",
    "61100255346",
    "86845729395",
    "03000443991",
    "74849560822",
    "59980231700",
    "90248115707",
    "82056229145",
    "68988687647",
    "59657429161",
    "04396907656",
    "89702485444",
    "49334640499",
    "89843515200",
    "26627637286",
    "96517650466",
    "81941692249",
    "20838028888",
    "00413864855",
    "79471093112",
    "06897074950",
    "70180285661",
    "51808354451",
    "57541651702",
    "07180937045",
    "01848900392",
    "28917222056",
    "34438615399",
    "46655439680",
    "05928803621",
    "88153164007",
    "92518925988",
    "00377949655",
    "60967893402",
    "37909039140",
    "88407302066",
    "74646326213",
    "07149896065",
    "42752317085",
    "58129750864",
    "17717087600",
]

FORMATTED_VALID_CPFS = [
    ("dots and dash", "499.784.420-90"),
    ("dots only", "028.062.110.85"),
    ("underscores", "011_258_960_00"),
    ("dash only", "779953010-30"),
]

INVALID_CPF_SAMPLES = [
    "86244870011",
    "33528612691",
    "12345678901",
    "12345678910",
    "499784420-75",
    "090.871.219-71",
    "081.465.729.10",
    "011_258_960_99",
]

NON_DIGIT_STRINGS = [
    "",
    "abc",
    "abc123",
    "true",
    "false",
    "null",
]

SHORT_OR_LONG_NUMERIC_STRINGS = [
    "1",
    "12",
    "123",
    "1234",
    "12345",
    "123456",
    "1234567",
    "12345678",
    "123456789",
    "1234567890",
]

INVALID_INPUT_CASES = [
    (None, "NoneType"),
    (42, "integer number"),
    (3.14, "float number"),
    (True, "boolean"),
    ({}, "dict"),
    ([1, 2, 3], "number[]"),
]


def _create_inputs_set(cpf: str) -> list[tuple[str, str | list[str]]]:
    unformatted_string = cpf
    formatted_string = re.sub(
        r"(\d{3})(\d{3})(\d{3})(\d+)",
        r"\1.\2.\3-\4",
        cpf,
    )
    unformatted_array = list(unformatted_string)
    formatted_array = list(formatted_string)
    grouped_array = re.split(r"[.-]", formatted_string)

    return [
        ("string", unformatted_string),
        ("formatted string", formatted_string),
        ("array", unformatted_array),
        ("formatted array", formatted_array),
        ("grouped array", grouped_array),
    ]


def describe_cpf_validator():
    def describe_constructor():
        def describe_when_called():
            def it_creates_an_instance_of_cpf_validator():
                validator = CpfValidator()

                assert isinstance(validator, CpfValidator)

    def describe_is_valid_method():
        def describe_when_given_a_valid_cpf():
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("82911017366"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_valid_cpf(_input_type, input_value):
                validator = CpfValidator()

                assert validator.is_valid(input_value) is True

            @pytest.mark.parametrize("cpf", VALID_CPF_SAMPLES)
            def it_returns_true_for_valid_cpf_samples(cpf):
                validator = CpfValidator()

                assert validator.is_valid(cpf) is True, f'Expected "{cpf}" to be valid.'

            @pytest.mark.parametrize(
                ("_format_label", "cpf"),
                FORMATTED_VALID_CPFS,
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_true_for_a_formatted_valid_cpf(_format_label, cpf):
                validator = CpfValidator()

                assert validator.is_valid(cpf) is True

        def describe_when_the_length_is_wrong():
            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("8291101736"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_cpf_with_less_than_11_digits(
                _input_type, input_value
            ):
                validator = CpfValidator()

                assert validator.is_valid(input_value) is False

            @pytest.mark.parametrize(
                ("_input_type", "input_value"),
                _create_inputs_set("829110173666"),
                ids=lambda param: param[0] if isinstance(param, tuple) else param,
            )
            def it_returns_false_for_a_cpf_with_more_than_11_digits(
                _input_type, input_value
            ):
                validator = CpfValidator()

                assert validator.is_valid(input_value) is False

            @pytest.mark.parametrize("cpf", SHORT_OR_LONG_NUMERIC_STRINGS)
            def it_returns_false_for_a_numeric_string_of_wrong_length(cpf):
                validator = CpfValidator()

                assert validator.is_valid(cpf) is False

        def describe_when_the_check_digits_are_wrong():
            @pytest.mark.parametrize("cpf", INVALID_CPF_SAMPLES)
            def it_returns_false_for_an_invalid_cpf(cpf):
                validator = CpfValidator()

                assert (
                    validator.is_valid(cpf) is False
                ), f'Expected "{cpf}" to be invalid.'

            def it_returns_false_for_every_wrong_check_digit_of_a_known_base():
                validator = CpfValidator()
                base = "177170876"
                valid_check_digits = "00"

                for index in range(100):
                    check_digits = f"{index:02d}"
                    input_value = f"{base}{check_digits}"
                    expected = check_digits == valid_check_digits

                    assert validator.is_valid(input_value) is expected

        def describe_when_the_cpf_has_all_digits_the_same():
            @pytest.mark.parametrize("prefix", REPEATED_DIGIT_PREFIXES)
            def it_returns_false_for_a_cpf_with_all_digits_the_same(prefix):
                validator = CpfValidator()

                for index in range(100):
                    input_value = f"{prefix}{index:02d}"

                    assert validator.is_valid(input_value) is False

        def describe_when_given_a_non_digit_string():
            @pytest.mark.parametrize("cpf", NON_DIGIT_STRINGS)
            def it_returns_false_for_a_non_digit_string(cpf):
                validator = CpfValidator()

                assert validator.is_valid(cpf) is False

        def describe_when_called_with_invalid_arguments():
            def it_does_not_throw_with_string_input():
                validator = CpfValidator()

                assert validator.is_valid("12345678901") is False

            def it_does_not_throw_with_array_of_strings_input():
                validator = CpfValidator()

                assert validator.is_valid(["12345678901"]) is False

            @pytest.mark.parametrize(
                ("input_value", "actual_type"), INVALID_INPUT_CASES
            )
            def it_raises_cpf_validator_input_type_error(input_value, actual_type):
                validator = CpfValidator()

                with pytest.raises(CpfValidatorInputTypeError) as exc_info:
                    validator.is_valid(input_value)

                error = exc_info.value

                assert error.expected_type == "string or string[]"
                assert error.actual_input is input_value
                assert error.actual_type == actual_type
                assert (
                    str(error)
                    == f"CPF input must be of type string or string[]. Got {actual_type}."
                )
