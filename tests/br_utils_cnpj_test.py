"""Unit tests for br-utils."""

from br_utils import BrUtils


class BrUtilsCnpjTest:
    def test_cnpj_format(self):
        utils = BrUtils()
        result = utils.cnpj.format("12345678000195")

        assert result == "12.345.678/0001-95"

    def test_cnpj_generate(self):
        utils = BrUtils()
        result = utils.cnpj.generate()

        assert len(result) == 14

    def test_cnpj_is_valid(self):
        utils = BrUtils()

        assert utils.cnpj.is_valid("11222333000181") is True
        assert utils.cnpj.is_valid("11111111111111") is False
