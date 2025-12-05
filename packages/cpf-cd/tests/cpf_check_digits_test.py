import pytest
from cpf_cd import (
    CpfCheckDigits,
    CpfCheckDigitsInputLengthError,
    CpfCheckDigitsInputTypeError,
)

test_cases = {
    "054496519": "05449651910",
    "965376562": "96537656206",
    "339670768": "33967076806",
    "623855638": "62385563827",
    "582286009": "58228600950",
    "935218534": "93521853403",
    "132115335": "13211533508",
    "492602225": "49260222575",
    "341428925": "34142892533",
    "727598627": "72759862720",
    "478880583": "47888058396",
    "336636977": "33663697797",
    "859249430": "85924943038",
    "306829569": "30682956961",
    "443539643": "44353964321",
    "439709507": "43970950783",
    "557601402": "55760140221",
    "951159579": "95115957922",
    "671669104": "67166910496",
    "627571100": "62757110004",
    "515930555": "51593055560",
    "303472731": "30347273130",
    "728843365": "72884336508",
    "523667424": "52366742479",
    "513362164": "51336216476",
    "427546407": "42754640797",
    "880696512": "88069651237",
    "571430852": "57143085227",
    "561416205": "56141620540",
    "769627950": "76962795050",
    "416603400": "41660340063",
    "853803696": "85380369634",
    "484667676": "48466767657",
    "058588388": "05858838820",
    "862778820": "86277882007",
    "047126827": "04712682752",
    "881801816": "88180181677",
    "932053118": "93205311884",
    "029783613": "02978361379",
    "950189877": "95018987766",
    "842528992": "84252899206",
    "216901618": "21690161809",
    "110478730": "11047873001",
    "032967591": "03296759158",
    "700386565": "70038656531",
    "929036812": "92903681287",
    "750529972": "75052997272",
    "481063058": "48106305872",
    "307721932": "30772193282",
    "994799423": "99479942364",
}


class CpfCheckDigitsTest:
    def test_constructor_throws_error_with_int_input(self):
        input = 12345678901

        with pytest.raises(CpfCheckDigitsInputTypeError) as exc_info:
            CpfCheckDigits(input)

        assert "CPF input must be of type str, list[str] or list[int]. Got int." in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_float_input(self):
        input = 12345678901.23

        with pytest.raises(CpfCheckDigitsInputTypeError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input must be of type str, list[str] or list[int]. Got float."
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_none_input(self):
        input = None

        with pytest.raises(CpfCheckDigitsInputTypeError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input must be of type str, list[str] or list[int]. Got NoneType."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_dict_input(self):
        input = {"12345678901": "12345678901"}

        with pytest.raises(CpfCheckDigitsInputTypeError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input must be of type str, list[str] or list[int]. Got dict."
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_empty_string_input(self):
        input = ""

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert 'CPF input "" does not contain 9 to 11 digits. Got 0.' in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_empty_list_input(self):
        input = []

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert 'CPF input [] does not contain 9 to 11 digits. Got 0 in "".' in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_non_numeric_string_input(self):
        input = "abcdefghij"

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            'CPF input "abcdefghij" does not contain 9 to 11 digits. Got 0 in "".'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_with_too_few_digits_input(self):
        input = "12345678"

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert 'CPF input "12345678" does not contain 9 to 11 digits. Got 8.' in str(
            exc_info.value
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_with_too_many_digits_input(self):
        input = "123456789012"

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            'CPF input "123456789012" does not contain 9 to 11 digits. Got 12.'
            in str(exc_info.value)
        ), (f"Input: {input}, Exception: {exc_info.value}")

    def test_constructor_throws_error_with_string_list_with_too_few_digits_input(self):
        input = ["1", "2", "3", "4", "5", "6", "7", "8"]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input ['1', '2', '3', '4', '5', '6', '7', '8'] does not contain 9 to 11 digits. Got 8 in \"12345678\"."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_list_with_too_many_digits_input(self):
        input = ["0", "5", "4", "4", "9", "6", "5", "1", "9", "1", "0", "1"]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input ['0', '5', '4', '4', '9', '6', '5', '1', '9', '1', '0', '1'] does not contain 9 to 11 digits. Got 12 in \"054496519101\"."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_string_list_with_too_many_digits_input_in_fewer_items(
        self,
    ):
        input = ["054496519101"]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            "CPF input ['054496519101'] does not contain 9 to 11 digits. Got 12 in \"054496519101\"."
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_few_digits_input(self):
        input = [1, 2, 3, 4, 5, 6, 7, 8]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            'CPF input [1, 2, 3, 4, 5, 6, 7, 8] does not contain 9 to 11 digits. Got 8 in "12345678".'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_many_digits_input(self):
        input = [0, 5, 4, 4, 9, 6, 5, 1, 9, 1, 0, 1]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            'CPF input [0, 5, 4, 4, 9, 6, 5, 1, 9, 1, 0, 1] does not contain 9 to 11 digits. Got 12 in "054496519101".'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_constructor_throws_error_with_int_list_with_too_many_digits_input_in_fewer_items(
        self,
    ):
        input = [544965191012]

        with pytest.raises(CpfCheckDigitsInputLengthError) as exc_info:
            CpfCheckDigits(input)

        assert (
            'CPF input [544965191012] does not contain 9 to 11 digits. Got 12 in "544965191012".'
            in str(exc_info.value)
        ), f"Input: {input}, Exception: {exc_info.value}"

    def test_calculate_first_check_digits_with_string_input(self):
        for input_str, expected in test_cases.items():
            cpf_check_digits = CpfCheckDigits(input_str)
            calculated_digit = cpf_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_string_input(self):
        for input_str, expected in test_cases.items():
            cpf_check_digits = CpfCheckDigits(input_str)
            calculated_digit = cpf_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_first_check_digits_with_string_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = list(input_str)
            cpf_check_digits = CpfCheckDigits(input_list)
            calculated_digit = cpf_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_string_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = list(input_str)
            cpf_check_digits = CpfCheckDigits(input_list)
            calculated_digit = cpf_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_first_check_digits_with_int_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [int(digit) for digit in input_str]
            cpf_check_digits = CpfCheckDigits(input_list)
            calculated_digit = cpf_check_digits.first_digit
            expected_digit = int(expected[-2])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_second_check_digits_with_int_list_input(self):
        for input_str, expected in test_cases.items():
            input_list = [int(digit) for digit in input_str]
            cpf_check_digits = CpfCheckDigits(input_list)
            calculated_digit = cpf_check_digits.second_digit
            expected_digit = int(expected[-1])

            assert (
                calculated_digit == expected_digit
            ), f"Input: {input_str}, Expected: {expected_digit}, Result: {calculated_digit}"

    def test_calculate_check_digits_with_negative_integers_in_list(self):
        input_with_negatives = [-0, -5, -4, -4, -9, -6, -5, -1, -9]
        expected_check_digits = CpfCheckDigits([0, 5, 4, 4, 9, 6, 5, 1, 9])

        check_digits = CpfCheckDigits(input_with_negatives)

        assert check_digits.first_digit == expected_check_digits.first_digit
        assert check_digits.second_digit == expected_check_digits.second_digit
        assert check_digits.to_string() == expected_check_digits.to_string()

    def test_calculate_check_digits_with_mixed_positive_negative_integers(self):
        input_mixed = [0, -5, 4, -4, 9, 6, -5, 1, 9]
        expected_check_digits = CpfCheckDigits([0, 5, 4, 4, 9, 6, 5, 1, 9])

        check_digits = CpfCheckDigits(input_mixed)

        assert check_digits.first_digit == expected_check_digits.first_digit
        assert check_digits.second_digit == expected_check_digits.second_digit

    def test_calculate_check_digits_with_negative_multi_digit_integer(self):
        input_negative = [-544965191]
        expected_check_digits = CpfCheckDigits([544965191])

        check_digits = CpfCheckDigits(input_negative)

        assert check_digits.first_digit == expected_check_digits.first_digit
        assert check_digits.second_digit == expected_check_digits.second_digit
        assert check_digits.to_string() == expected_check_digits.to_string()
