from unittest.mock import MagicMock

from cnpj_utils import CnpjUtils


class CnpjUtilsValidatorTest:
    def test_is_valid_forwards_argument(self):
        utils = CnpjUtils()
        utils.validator = MagicMock()
        utils.validator.is_valid.return_value = True

        result = utils.is_valid("12345678000190")

        assert result is True
        utils.validator.is_valid.assert_called_once_with("12345678000190")

    def test_is_valid_returns_false(self):
        utils = CnpjUtils()
        utils.validator = MagicMock()
        utils.validator.is_valid.return_value = False

        result = utils.is_valid("12345678000199")

        assert result is False
        utils.validator.is_valid.assert_called_once_with("12345678000199")
