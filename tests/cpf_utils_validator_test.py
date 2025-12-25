from unittest.mock import MagicMock

from cpf_utils import CpfUtils


class CpfUtilsValidatorTest:
    def test_is_valid_forwards_argument(self):
        utils = CpfUtils()
        utils.validator = MagicMock()
        utils.validator.is_valid.return_value = True

        result = utils.is_valid("12345678901")

        assert result is True
        utils.validator.is_valid.assert_called_once_with("12345678901")

    def test_is_valid_returns_false(self):
        utils = CpfUtils()
        utils.validator = MagicMock()
        utils.validator.is_valid.return_value = False

        result = utils.is_valid("12345678909")

        assert result is False
        utils.validator.is_valid.assert_called_once_with("12345678909")
