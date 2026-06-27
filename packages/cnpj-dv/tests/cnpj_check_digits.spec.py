"""Behavioral spec for ``CnpjCheckDigits``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-dv/tests/cnpj-check-digits.spec.ts``) and the PHP reference
suite (``php/packages/cnpj-dv/tests/specs/CnpjCheckDigits.spec.php``), following
the business rules documented in ``AGENTS.md``.
"""

import pytest
from cnpj_dv import (
    CnpjCheckDigits,
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
)

# Shared conformance fixtures: (12-char base, expected 14-char CNPJ).
# Reused verbatim from the JS/PHP reference test suites.
TEST_CASES = [
    ("313124260006", "31312426000619"),
    ("MGKGMJ9X0001", "MGKGMJ9X000168"),
    ("1EY6WPPN0001", "1EY6WPPN000164"),
    ("Y7ELKY990001", "Y7ELKY99000137"),
    ("AGPRASLP0001", "AGPRASLP000123"),
    ("017205400003", "01720540000374"),
    ("615208400003", "61520840000331"),
    ("ABDYZVE90001", "ABDYZVE9000144"),
    ("050532360008", "05053236000886"),
    ("CCLW1PDP0001", "CCLW1PDP000131"),
    ("JLNC9SM70001", "JLNC9SM7000118"),
    ("51GLNYMV0001", "51GLNYMV000138"),
    ("003579820002", "00357982000254"),
    ("573669460004", "57366946000436"),
    ("412851460002", "41285146000299"),
    ("159833710006", "15983371000612"),
    ("R39X6CAD0001", "R39X6CAD000118"),
    ("LA031XPE0001", "LA031XPE000171"),
    ("8CRCX4G90001", "8CRCX4G9000145"),
    ("002439100008", "00243910000871"),
    ("570635620003", "57063562000363"),
    ("210890360007", "21089036000759"),
    ("483494070001", "48349407000155"),
    ("871056390003", "87105639000381"),
    ("ZP64G0G50001", "ZP64G0G5000169"),
    ("RTCR3YKJ0001", "RTCR3YKJ000139"),
    ("914157320007", "91415732000793"),
    ("167805610002", "16780561000271"),
    ("4SGW7L2V0001", "4SGW7L2V000192"),
    ("51CGZ6CE0001", "51CGZ6CE000166"),
    ("4TD25XEB0001", "4TD25XEB000186"),
    ("C892RYMB0001", "C892RYMB000166"),
    ("006645070002", "00664507000220"),
    ("711081470005", "71108147000571"),
    ("410302000007", "41030200000760"),
    ("863940890002", "86394089000214"),
    ("CCBHVLD70001", "CCBHVLD7000109"),
    ("Y8E3T0H20001", "Y8E3T0H2000127"),
    ("015206300003", "01520630000311"),
    ("4LHTLHRR0001", "4LHTLHRR000129"),
    ("669041680003", "66904168000300"),
    ("470076350005", "47007635000508"),
    ("DSX3851R0001", "DSX3851R000123"),
    ("517503930003", "51750393000353"),
    ("456189710004", "45618971000480"),
    ("SVAERM5X0001", "SVAERM5X000180"),
    ("479281750001", "47928175000127"),
    ("TVHW9KYC0001", "TVHW9KYC000168"),
    ("982882590009", "98288259000931"),
    ("648275500008", "64827550000838"),
    ("023543810003", "02354381000302"),
    ("HPC6L9ZB0001", "HPC6L9ZB000101"),
    ("822313180002", "82231318000229"),
    ("W7SJP7J10001", "W7SJP7J1000104"),
    ("784153420007", "78415342000755"),
    ("451264770004", "45126477000407"),
    ("HHVRZ7860001", "HHVRZ786000190"),
    ("4BB2CZY00001", "4BB2CZY0000107"),
    ("YYWVGRDP0001", "YYWVGRDP000103"),
    ("005792660004", "00579266000483"),
    ("2V802ATH0001", "2V802ATH000108"),
    ("HVWA2TC40001", "HVWA2TC4000139"),
    ("J4LR5KNM0001", "J4LR5KNM000119"),
    ("KL46HEJ50001", "KL46HEJ5000106"),
    ("SZS0X62H0001", "SZS0X62H000177"),
    ("JM6VWMAZ0001", "JM6VWMAZ000126"),
    ("885435950009", "88543595000920"),
    ("1DYMEV6W0001", "1DYMEV6W000188"),
    ("758805710006", "75880571000671"),
    ("NK78LS4Z0001", "NK78LS4Z000127"),
    ("238857260004", "23885726000405"),
    ("723362430001", "72336243000106"),
    ("JG3TE2X30001", "JG3TE2X3000167"),
    ("782152520001", "78215252000125"),
    ("283366280009", "28336628000939"),
    ("E6SN8JC40001", "E6SN8JC4000149"),
    ("79YJNKHZ0001", "79YJNKHZ000110"),
    ("47GZ4GL10001", "47GZ4GL1000127"),
    ("069523030004", "06952303000433"),
    ("474080600006", "47408060000616"),
    ("040693560006", "04069356000647"),
    ("THTV6BM20001", "THTV6BM2000157"),
    ("TPY675ZN0001", "TPY675ZN000119"),
    ("KS4E7SAA0001", "KS4E7SAA000176"),
    ("NMPEHEVB0001", "NMPEHEVB000129"),
    ("1M917XTB0001", "1M917XTB000176"),
    ("J9M0ZD510001", "J9M0ZD51000123"),
    ("P0G334BY0001", "P0G334BY000136"),
    ("076394320005", "07639432000510"),
    ("992040290001", "99204029000152"),
    ("2D56RWZP0001", "2D56RWZP000195"),
    ("M68N7W6L0001", "M68N7W6L000175"),
    ("LH9B5RXK0001", "LH9B5RXK000171"),
    ("495517490003", "49551749000388"),
    ("307168390003", "30716839000353"),
    ("Y0EBSBLT0001", "Y0EBSBLT000105"),
    ("C9DASM460001", "C9DASM46000190"),
    ("ZZ0172HG0001", "ZZ0172HG000130"),
    ("6DYLY5060001", "6DYLY506000113"),
    ("JE5TKSJ80001", "JE5TKSJ8000109"),
    ("TRPYT31P0001", "TRPYT31P000124"),
    ("144863760009", "14486376000910"),
    ("KZEWGKT60001", "KZEWGKT6000198"),
    ("S28361BX0001", "S28361BX000165"),
    ("6VK1VBLW0001", "6VK1VBLW000154"),
    ("KJT4XC490001", "KJT4XC49000165"),
    ("H8SS5ZTT0001", "H8SS5ZTT000104"),
    ("5PYHBL870001", "5PYHBL87000149"),
    ("ZAB6JG9E0001", "ZAB6JG9E000148"),
    ("354946770003", "35494677000370"),
    ("J0EHJEXT0001", "J0EHJEXT000130"),
    ("539MLKGS0001", "539MLKGS000154"),
    ("319476190003", "31947619000301"),
    ("ZWW4XY8X0001", "ZWW4XY8X000183"),
    ("D83TW2JG0001", "D83TW2JG000100"),
    ("KPJR04DT0001", "KPJR04DT000143"),
    ("301272110005", "30127211000584"),
    ("G4T4BTDR0001", "G4T4BTDR000120"),
    ("509053950004", "50905395000492"),
    ("W95P9DKV0001", "W95P9DKV000194"),
]

# Bases made of a single repeated *digit* must be rejected.
REPEATED_DIGIT_INPUTS = [
    "111111111111",
    "222222222222",
    "333333333333",
    "444444444444",
    "555555555555",
    "666666666666",
    "777777777777",
    "888888888888",
    "999999999999",
    ["111111111111"],
    ["222222222222"],
    ["333333333333"],
    ["444444444444"],
    ["555555555555"],
    ["666666666666"],
    ["777777777777"],
    ["888888888888"],
    ["999999999999"],
    ["11", "111", "111", "1111"],
    ["22", "222", "222", "2222"],
    ["33", "333", "333", "3333"],
    ["44", "444", "444", "4444"],
    ["55", "555", "555", "5555"],
    ["66", "666", "666", "6666"],
    ["77", "777", "777", "7777"],
    ["88", "888", "888", "8888"],
    ["99", "999", "999", "9999"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3"],
    ["4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4"],
    ["5", "5", "5", "5", "5", "5", "5", "5", "5", "5", "5", "5"],
    ["6", "6", "6", "6", "6", "6", "6", "6", "6", "6", "6", "6"],
    ["7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7"],
    ["8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8"],
    ["9", "9", "9", "9", "9", "9", "9", "9", "9", "9", "9", "9"],
]

# Bases made of a single repeated *letter* are accepted (only digits are rejected).
REPEATED_LETTER_INPUTS = [
    "AAAAAAAAAAAA",
    "BBBBBBBBBBBB",
    "CCCCCCCCCCCC",
    "JJJJJJJJJJJJ",
    "KKKKKKKKKKKK",
    "LLLLLLLLLLLL",
    "XXXXXXXXXXXX",
    "YYYYYYYYYYYY",
    "ZZZZZZZZZZZZ",
    ["AAAAAAAAAAAA"],
    ["BBBBBBBBBBBB"],
    ["CCCCCCCCCCCC"],
    ["JJJJJJJJJJJJ"],
    ["KKKKKKKKKKKK"],
    ["LLLLLLLLLLLL"],
    ["XXXXXXXXXXXX"],
    ["YYYYYYYYYYYY"],
    ["ZZZZZZZZZZZZ"],
    ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
    ["B", "B", "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"],
    ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
    ["J", "J", "J", "J", "J", "J", "J", "J", "J", "J", "J", "J"],
    ["K", "K", "K", "K", "K", "K", "K", "K", "K", "K", "K", "K"],
    ["L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z"],
]

# Inputs whose first 8 normalized chars are "00000000" (with a valid branch).
INVALID_BASE_ID_INPUTS = [
    "000000000001",
    "00.000.000/0001",
    ["00", "000", "000", "0001"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
]

# Inputs whose chars 9-12 are "0000" (with a valid base).
INVALID_BRANCH_ID_INPUTS = [
    "123456780000",
    "12345678/0000",
    ["12", "345", "678", "0000"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "0", "0", "0", "0"],
]

# Inputs whose normalized length falls outside the 12-14 range.
INVALID_LENGTH_INPUTS = [
    "",
    [],
    "12345678910",
    "123456789101112",
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    ["0", "0", "1", "1", "1", "2", "2", "2", "0", "0", "0", "4", "5", "6", "7"],
]

# Inputs that are neither a string nor a list of strings.
INVALID_TYPE_INPUTS = [
    12345678901,
    None,
    {"cnpj": "12345678901"},
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, "2", 3, "4", 5],
]


class _CnpjCheckDigitsWithCalculateSpy(CnpjCheckDigits):
    """Mirror of the PHP ``CnpjCheckDigitsWithCalculateSpy`` mock.

    Counts how many times the internal modulo-11 routine runs so the caching
    behavior can be asserted.
    """

    def __init__(self, cnpj_input):
        self.calculate_call_count = 0
        super().__init__(cnpj_input)

    def _calculate(self, cnpj_sequence):
        self.calculate_call_count += 1
        return super()._calculate(cnpj_sequence)


def describe_cnpj_check_digits():
    def describe_constructor():
        def describe_when_given_invalid_input_type():
            @pytest.mark.parametrize("cnpj_input", INVALID_TYPE_INPUTS)
            def it_raises_input_type_error(cnpj_input):
                with pytest.raises(CnpjCheckDigitsInputTypeError):
                    CnpjCheckDigits(cnpj_input)

        def describe_when_given_invalid_input_length():
            @pytest.mark.parametrize("cnpj_input", INVALID_LENGTH_INPUTS)
            def it_raises_input_length_exception(cnpj_input):
                with pytest.raises(CnpjCheckDigitsInputLengthException):
                    CnpjCheckDigits(cnpj_input)

        def describe_when_given_invalid_cnpj_base_id():
            @pytest.mark.parametrize("cnpj_input", INVALID_BASE_ID_INPUTS)
            def it_raises_input_invalid_exception(cnpj_input):
                with pytest.raises(
                    CnpjCheckDigitsInputInvalidException, match=r"(?i)base id"
                ):
                    CnpjCheckDigits(cnpj_input)

        def describe_when_given_invalid_cnpj_branch_id():
            @pytest.mark.parametrize("cnpj_input", INVALID_BRANCH_ID_INPUTS)
            def it_raises_input_invalid_exception(cnpj_input):
                with pytest.raises(
                    CnpjCheckDigitsInputInvalidException, match=r"(?i)branch id"
                ):
                    CnpjCheckDigits(cnpj_input)

        def describe_when_given_repeated_numeric_characters():
            @pytest.mark.parametrize("cnpj_input", REPEATED_DIGIT_INPUTS)
            def it_raises_input_invalid_exception(cnpj_input):
                with pytest.raises(
                    CnpjCheckDigitsInputInvalidException, match=r"(?i)repeated digits"
                ):
                    CnpjCheckDigits(cnpj_input)

        def describe_when_given_repeated_non_numeric_characters():
            @pytest.mark.parametrize("cnpj_input", REPEATED_LETTER_INPUTS)
            def it_does_not_raise_and_computes_check_digits(cnpj_input):
                stringified = (
                    "".join(cnpj_input) if isinstance(cnpj_input, list) else cnpj_input
                )

                cnpj_check_digits = CnpjCheckDigits(cnpj_input)

                assert len(cnpj_check_digits.cnpj) == 14
                assert cnpj_check_digits.cnpj.startswith(stringified)

    def describe_first_digit():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_first_digit_for_a_string(base, full):
            assert CnpjCheckDigits(base).first == full[-2]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_first_digit_for_a_list_of_strings(base, full):
            assert CnpjCheckDigits(list(base)).first == full[-2]

        def describe_when_accessing_digits_multiple_times():
            def it_returns_cached_values_on_subsequent_calls():
                cnpj_check_digits = _CnpjCheckDigitsWithCalculateSpy("914157320007")

                first_results = {
                    cnpj_check_digits.first,
                    cnpj_check_digits.first,
                    cnpj_check_digits.first,
                }

                assert len(first_results) == 1
                assert cnpj_check_digits.calculate_call_count == 1

    def describe_second_digit():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_second_digit_for_a_string(base, full):
            assert CnpjCheckDigits(base).second == full[-1]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_the_second_digit_for_a_list_of_strings(base, full):
            assert CnpjCheckDigits(list(base)).second == full[-1]

        def describe_when_accessing_digits_multiple_times():
            def it_returns_cached_values_on_subsequent_calls():
                cnpj_check_digits = _CnpjCheckDigitsWithCalculateSpy("914157320007")

                second_results = {
                    cnpj_check_digits.second,
                    cnpj_check_digits.second,
                    cnpj_check_digits.second,
                }

                assert len(second_results) == 1
                assert cnpj_check_digits.calculate_call_count == 2

    def describe_both_digits():
        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_both_digits_for_a_string(base, full):
            assert CnpjCheckDigits(base).both == full[-2:]

        @pytest.mark.parametrize(("base", "full"), TEST_CASES)
        def it_returns_both_digits_for_a_list_of_strings(base, full):
            assert CnpjCheckDigits(list(base)).both == full[-2:]

    def describe_actual_cnpj_string():
        def describe_when_input_is_a_string():
            def it_returns_the_14_character_cnpj():
                assert CnpjCheckDigits("914157320007").cnpj == "91415732000793"

        def describe_when_input_is_a_list_of_grouped_characters():
            def it_returns_the_14_character_cnpj():
                cnpj_check_digits = CnpjCheckDigits(["9141", "5732", "0007"])

                assert cnpj_check_digits.cnpj == "91415732000793"

        def describe_when_input_is_a_list_of_individual_characters():
            def it_returns_the_14_character_cnpj():
                cnpj_check_digits = CnpjCheckDigits(
                    ["9", "1", "4", "1", "5", "7", "3", "2", "0", "0", "0", "7"]
                )

                assert cnpj_check_digits.cnpj == "91415732000793"

        def describe_when_validating_all_test_cases():
            @pytest.mark.parametrize(("base", "full"), TEST_CASES)
            def it_returns_the_expected_cnpj(base, full):
                assert CnpjCheckDigits(base).cnpj == full

    def describe_edge_cases():
        def describe_when_input_is_a_formatted_cnpj_string():
            def it_parses_and_calculates_check_digits():
                assert CnpjCheckDigits("91.415.732/0007").cnpj == "91415732000793"

        def describe_when_input_is_a_formatted_alphanumeric_cnpj_string():
            @pytest.mark.parametrize(
                "cnpj_input",
                ["MG.KGM.J9X/0001-68", "mg.kgm.j9x/0001-68"],
            )
            def it_parses_and_calculates_check_digits(cnpj_input):
                assert CnpjCheckDigits(cnpj_input).cnpj == "MGKGMJ9X000168"

        def describe_when_input_already_contains_check_digits():
            def it_ignores_provided_check_digits_and_recomputes():
                cnpj_check_digits = CnpjCheckDigits("91415732000700")

                assert cnpj_check_digits.first == "9"
                assert cnpj_check_digits.second == "3"
                assert cnpj_check_digits.cnpj == "91415732000793"
