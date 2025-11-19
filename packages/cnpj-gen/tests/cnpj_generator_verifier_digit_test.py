import pytest
from cnpj_gen import CnpjGeneratorVerifierDigit, InvalidArgumentException


class CnpjGeneratorVerifierDigitTest:
    def setup_method(self):
        self.verifier_digit = CnpjGeneratorVerifierDigit()

    def test_calculate_throws_error_with_too_few_digits(self):
        if not hasattr(self, "verifier_digit"):
            self.setup_method()

        cnpj_sequence = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2]

        with pytest.raises(InvalidArgumentException) as exc_info:
            self.verifier_digit.calculate(cnpj_sequence)
        assert (
            'To calculate the verifier digit, the CNPJ sequence must be between 12 and 13 digits long, but got 11 digits ("01230123012").'
            in str(exc_info.value)
        )

    def test_calculate_throws_error_with_too_many_digits(self):
        if not hasattr(self, "verifier_digit"):
            self.setup_method()

        cnpj_sequence = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3]

        with pytest.raises(InvalidArgumentException) as exc_info:
            self.verifier_digit.calculate(cnpj_sequence)
        assert (
            'To calculate the verifier digit, the CNPJ sequence must be between 12 and 13 digits long, but got 14 digits ("01234012340123").'
            in str(exc_info.value)
        )

    def test_calculate_verifier_digits_for_sequences_with_12_digits(self):
        if not hasattr(self, "verifier_digit"):
            self.setup_method()

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

        for input_str, expected in test_cases.items():
            input_array = [int(digit) for digit in input_str]

            first_digit = self.verifier_digit.calculate(input_array)
            input_array.append(first_digit)
            second_digit = self.verifier_digit.calculate(input_array)
            input_array.append(second_digit)
            result_string = "".join(str(digit) for digit in input_array)

            assert (
                result_string == expected
            ), f"Input: {input_str}, Expected: {expected}, Result: {result_string}"
