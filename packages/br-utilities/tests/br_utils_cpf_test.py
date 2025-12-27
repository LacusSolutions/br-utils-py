"""Unit tests for br-utils."""

from br_utils import BrUtils


class BrUtilsCpfTest:
    def test_cpf_format(self):
        utils = BrUtils()
        result = utils.cpf.format("12345678901")

        assert result == "123.456.789-01"

    def test_cpf_generate(self):
        utils = BrUtils()
        result = utils.cpf.generate()

        assert len(result) == 11

    def test_cpf_is_valid(self):
        utils = BrUtils()

        assert utils.cpf.is_valid("52998224725") is True
        assert utils.cpf.is_valid("12345678901") is False
