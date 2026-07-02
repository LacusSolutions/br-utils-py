"""Behavioral spec for ``CpfCheckDigits``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-dv/tests/cpf-check-digits.spec.ts``) and the PHP reference
suite (``php/packages/cpf-dv/tests/Specs/CpfCheckDigits.spec.php``), following
the business rules documented in ``AGENTS.md``.
"""

import pytest
from cpf_dv import (
    CpfCheckDigits,
    CpfCheckDigitsInputInvalidException,
    CpfCheckDigitsInputLengthException,
    CpfCheckDigitsInputTypeError,
)

# Shared conformance fixtures: (9-digit base, expected 11-digit CPF).
# Reused verbatim from the JS/PHP reference test suites.
TEST_CASES = [
    ("054496519", "05449651910"),
    ("965376562", "96537656206"),
    ("339670768", "33967076806"),
    ("623855638", "62385563827"),
    ("582286009", "58228600950"),
    ("935218534", "93521853403"),
    ("132115335", "13211533508"),
    ("492602225", "49260222575"),
    ("341428925", "34142892533"),
    ("727598627", "72759862720"),
    ("478880583", "47888058396"),
    ("336636977", "33663697797"),
    ("859249430", "85924943038"),
    ("306829569", "30682956961"),
    ("443539643", "44353964321"),
    ("439709507", "43970950783"),
    ("557601402", "55760140221"),
    ("951159579", "95115957922"),
    ("671669104", "67166910496"),
    ("627571100", "62757110004"),
    ("515930555", "51593055560"),
    ("303472731", "30347273130"),
    ("728843365", "72884336508"),
    ("523667424", "52366742479"),
    ("513362164", "51336216476"),
    ("427546407", "42754640797"),
    ("880696512", "88069651237"),
    ("571430852", "57143085227"),
    ("561416205", "56141620540"),
    ("769627950", "76962795050"),
    ("416603400", "41660340063"),
    ("853803696", "85380369634"),
    ("484667676", "48466767657"),
    ("058588388", "05858838820"),
    ("862778820", "86277882007"),
    ("047126827", "04712682752"),
    ("881801816", "88180181677"),
    ("932053118", "93205311884"),
    ("029783613", "02978361379"),
    ("950189877", "95018987766"),
    ("842528992", "84252899206"),
    ("216901618", "21690161809"),
    ("110478730", "11047873001"),
    ("032967591", "03296759158"),
    ("700386565", "70038656531"),
    ("929036812", "92903681287"),
    ("750529972", "75052997272"),
    ("481063058", "48106305872"),
    ("307721932", "30772193282"),
    ("994799423", "99479942364"),
]

REPEATED_DIGIT_INPUTS = [
    "111111111",
    "222222222",
    "333333333",
    "444444444",
    "555555555",
    "666666666",
    "777777777",
    "888888888",
    "999999999",
    "000000000",
    ["111", "111", "111"],
    ["222", "222", "222"],
    ["333", "333", "333"],
    ["444", "444", "444"],
    ["555", "555", "555"],
    ["666", "666", "666"],
    ["777", "777", "777"],
    ["888", "888", "888"],
    ["999", "999", "999"],
    ["000", "000", "000"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["3", "3", "3", "3", "3", "3", "3", "3", "3"],
    ["4", "4", "4", "4", "4", "4", "4", "4", "4"],
    ["5", "5", "5", "5", "5", "5", "5", "5", "5"],
    ["6", "6", "6", "6", "6", "6", "6", "6", "6"],
    ["7", "7", "7", "7", "7", "7", "7", "7", "7"],
    ["8", "8", "8", "8", "8", "8", "8", "8", "8"],
    ["9", "9", "9", "9", "9", "9", "9", "9", "9"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0"],
]

INVALID_LENGTH_INPUTS = [
    "",
    [],
    "abcdefghij",
    "12345678",
    "123456789100",
    ["1", "2", "3", "4", "5", "6", "7", "8"],
    ["0", "5", "4", "4", "9", "6", "5", "1", "9", "1", "0", "0"],
]

INVALID_TYPE_INPUTS = [
    12345678901,
    None,
    {"cpf": "12345678901"},
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, "2", 3, "4", 5],
]


class _CpfCheckDigitsWithCalculateSpy(CpfCheckDigits):
    """Mirror of the PHP ``CpfCheckDigitsWithCalculateSpy`` mock.

    Counts how many times the internal modulo-11 routine runs so the caching
    behavior can be asserted.
    """

    def __init__(self, cpf_input):
        self.calculate_call_count = 0
        super().__init__(cpf_input)

    def _calculate(self, cpf_sequence):
        self.calculate_call_count += 1
        return super()._calculate(cpf_sequence)


def describe_cpf_check_digits():
    def describe_constructor():
        def describe_when_given_invalid_input_type():
            @pytest.mark.parametrize("cpf_input", INVALID_TYPE_INPUTS)
            def it_raises_input_type_error(cpf_input):
                with pytest.raises(CpfCheckDigitsInputTypeError):
                    CpfCheckDigits(cpf_input)

        def describe_when_given_invalid_input_length():
            @pytest.mark.parametrize("cpf_input", INVALID_LENGTH_INPUTS)
            def it_raises_input_length_exception(cpf_input):
                with pytest.raises(CpfCheckDigitsInputLengthException):
                    CpfCheckDigits(cpf_input)

        def describe_when_given_repeated_digits():
            @pytest.mark.parametrize("cpf_input", REPEATED_DIGIT_INPUTS)
            def it_raises_input_invalid_exception(cpf_input):
                with pytest.raises(
                    CpfCheckDigitsInputInvalidException, match=r"(?i)repeated digits"
                ):
                    CpfCheckDigits(cpf_input)

    def describe_first_digit():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_first_digit_for_a_string(base, full):
            assert CpfCheckDigits(base).first == full[-2]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_first_digit_for_a_list_of_strings(base, full):
            assert CpfCheckDigits(list(base)).first == full[-2]

        def describe_when_accessing_digits_multiple_times():
            def it_returns_cached_values_on_subsequent_calls():
                cpf_check_digits = _CpfCheckDigitsWithCalculateSpy("123456789")

                first_results = {
                    cpf_check_digits.first,
                    cpf_check_digits.first,
                    cpf_check_digits.first,
                }

                assert len(first_results) == 1
                assert cpf_check_digits.calculate_call_count == 1

    def describe_second_digit():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_second_digit_for_a_string(base, full):
            assert CpfCheckDigits(base).second == full[-1]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_second_digit_for_a_list_of_strings(base, full):
            assert CpfCheckDigits(list(base)).second == full[-1]

        def describe_when_accessing_digits_multiple_times():
            def it_returns_cached_values_on_subsequent_calls():
                cpf_check_digits = _CpfCheckDigitsWithCalculateSpy("123456789")

                second_results = {
                    cpf_check_digits.second,
                    cpf_check_digits.second,
                    cpf_check_digits.second,
                }

                assert len(second_results) == 1
                assert cpf_check_digits.calculate_call_count == 2

    def describe_both_digits():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_both_digits_for_a_string(base, full):
            assert CpfCheckDigits(base).both == full[-2:]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_both_digits_for_a_list_of_strings(base, full):
            assert CpfCheckDigits(list(base)).both == full[-2:]

    def describe_actual_cpf_string():
        def describe_when_input_is_a_string():
            def it_returns_the_11_character_cpf():
                assert CpfCheckDigits("123456789").cpf == "12345678909"

        def describe_when_input_is_a_list_of_grouped_digits_string():
            def it_returns_the_11_character_cpf():
                cpf_check_digits = CpfCheckDigits(["123", "456", "789"])

                assert cpf_check_digits.cpf == "12345678909"

        def describe_when_input_is_a_list_of_individual_digits_string():
            def it_returns_the_11_character_cpf():
                cpf_check_digits = CpfCheckDigits(
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                )

                assert cpf_check_digits.cpf == "12345678909"

        def describe_when_validating_all_test_cases():
            @pytest.mark.parametrize(("base", "full"), TEST_CASES)
            def it_returns_the_expected_cpf(base, full):
                assert CpfCheckDigits(base).cpf == full

    def describe_edge_cases():
        def describe_when_input_is_a_formatted_cpf_string():
            def it_parses_and_calculates_check_digits():
                assert CpfCheckDigits("123.456.789").cpf == "12345678909"

        def describe_when_input_already_contains_check_digits():
            def it_ignores_provided_check_digits_and_recomputes():
                cpf_check_digits = CpfCheckDigits("12345678910")

                assert cpf_check_digits.first == "0"
                assert cpf_check_digits.second == "9"
                assert cpf_check_digits.cpf == "12345678909"
