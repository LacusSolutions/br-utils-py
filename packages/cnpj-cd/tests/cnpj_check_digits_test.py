import pytest
from cnpj_cd import CnpjCheckDigits, CnpjInvalidLengthError, CnpjTypeError

test_cases = {
    "914157320007": "91415732000793",
    "517503930003": "51750393000353",
    "050532360008": "05053236000886",
    "412851460002": "41285146000299",
    "003579820002": "00357982000254",
    "144863760009": "14486376000910",
    "301272110005": "30127211000584",
    "017205400003": "01720540000374",
    "723362430001": "72336243000106",
    "982882590009": "98288259000931",
    "238857260004": "23885726000405",
    "456189710004": "45618971000480",
    "871056390003": "87105639000381",
    "615208400003": "61520840000331",
    "483494070001": "48349407000155",
    "782152520001": "78215252000125",
    "023543810003": "02354381000302",
    "648275500008": "64827550000838",
    "210890360007": "21089036000759",
    "319476190003": "31947619000301",
    "758805710006": "75880571000671",
    "159833710006": "15983371000612",
    "069523030004": "06952303000433",
    "509053950004": "50905395000492",
    "573669460004": "57366946000436",
    "307168390003": "30716839000353",
    "885435950009": "88543595000920",
    "354946770003": "35494677000370",
    "006645070002": "00664507000220",
    "470076350005": "47007635000508",
    "005792660004": "00579266000483",
    "479281750001": "47928175000127",
    "167805610002": "16780561000271",
    "313124260006": "31312426000619",
    "822313180002": "82231318000229",
    "992040290001": "99204029000152",
    "040693560006": "04069356000647",
    "410302000007": "41030200000760",
    "015206300003": "01520630000311",
    "863940890002": "86394089000214",
    "002439100008": "00243910000871",
    "669041680003": "66904168000300",
    "283366280009": "28336628000939",
    "076394320005": "07639432000510",
    "451264770004": "45126477000407",
    "474080600006": "47408060000616",
    "711081470005": "71108147000571",
    "784153420007": "78415342000755",
    "495517490003": "49551749000388",
    "570635620003": "57063562000363",
}


class CnpjCheckDigitsTest:
    def test_constructor_throws_error_with_int_input(self):
        input = 12345678901234

        with pytest.raises(CnpjTypeError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "CNPJ input must be of type str, list[str] or list[int]. Got int."
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_float_input(self):
        input = 12345678901234.56

        with pytest.raises(CnpjTypeError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "CNPJ input must be of type str, list[str] or list[int]. Got float."
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_none_input(self):
        input = None

        with pytest.raises(CnpjTypeError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "CNPJ input must be of type str, list[str] or list[int]. Got NoneType."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_dict_input(self):
        input = {"12345678901234": "12345678901234"}

        with pytest.raises(CnpjTypeError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "CNPJ input must be of type str, list[str] or list[int]. Got dict."
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_empty_string_input(self):
        input = ""

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert 'Parameter "" does not contain 12 to 14 digits. Got 0.' in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_empty_list_input(self):
        input = []

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert 'Parameter "[]" does not contain 12 to 14 digits. Got 0.' in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_non_numeric_string_input(self):
        input = "abcdefghijkl"

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "abcdefghijkl" does not contain 12 to 14 digits. Got 0.'
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_string_with_too_few_digits_input(self):
        input = "12345678910"

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "12345678910" does not contain 12 to 14 digits. Got 11.'
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_string_with_too_many_digits_input(self):
        input = "123456789101112"

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "123456789101112" does not contain 12 to 14 digits. Got 15.'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_list_with_too_few_digits_input(self):
        input = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "Parameter \"['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']\" does not contain 12 to 14 digits. Got 10."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_list_with_too_many_digits_input(self):
        input = [
            "0",
            "0",
            "1",
            "1",
            "1",
            "2",
            "2",
            "2",
            "0",
            "0",
            "0",
            "4",
            "5",
            "6",
            "7",
        ]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "Parameter \"['0', '0', '1', '1', '1', '2', '2', '2', '0', '0', '0', '4', '5', '6', '7']\" does not contain 12 to 14 digits. Got 15."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_list_with_too_many_digits_input_in_fewer_items(
        self,
    ):
        input = ["001112220004567"]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            "Parameter \"['001112220004567']\" does not contain 12 to 14 digits. Got 15."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_few_digits_input(self):
        input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]" does not contain 12 to 14 digits. Got 10.'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_many_digits_input(self):
        input = [0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 4, 5, 6, 7]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "[0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 4, 5, 6, 7]" does not contain 12 to 14 digits. Got 15.'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_many_digits_input_in_fewer_items(
        self,
    ):
        input = [112223330004567]

        with pytest.raises(CnpjInvalidLengthError) as exc_info:
            CnpjCheckDigits(input)

        assert (
            'Parameter "[112223330004567]" does not contain 12 to 14 digits. Got 15.'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_calculate_first_check_digits_with_string_input(self):
        for input_str, expected in test_cases.items():
            cnpj_check_digits = CnpjCheckDigits(input_str)
            calculated_digit = cnpj_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_string_input(self):
        for input_str, expected in test_cases.items():
            cnpj_check_digits = CnpjCheckDigits(input_str)
            calculated_digit = cnpj_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_first_check_digits_with_string_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [digit for digit in input_str]
            cnpj_check_digits = CnpjCheckDigits(input_list)
            calculated_digit = cnpj_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_string_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [digit for digit in input_str]
            cnpj_check_digits = CnpjCheckDigits(input_list)
            calculated_digit = cnpj_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_first_check_digits_with_int_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [int(digit) for digit in input_str]
            cnpj_check_digits = CnpjCheckDigits(input_list)
            calculated_digit = cnpj_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_int_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [int(digit) for digit in input_str]
            cnpj_check_digits = CnpjCheckDigits(input_list)
            calculated_digit = cnpj_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"
