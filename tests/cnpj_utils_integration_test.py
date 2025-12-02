from unittest.mock import MagicMock

import pytest
from cnpj_utils import CnpjUtils


class CnpjUtilsIntegrationTest:
    def test_all_methods_use_correct_instances(self):
        utils = CnpjUtils()

        utils.formatter = MagicMock()
        utils.generator = MagicMock()
        utils.validator = MagicMock()
        utils.formatter.format.return_value = "formatted"
        utils.generator.generate.return_value = "generated"
        utils.validator.is_valid.return_value = True

        assert utils.format("123") == "formatted"
        assert utils.generate() == "generated"
        assert utils.is_valid("123") is True
        utils.formatter.format.assert_called_once()
        utils.generator.generate.assert_called_once()
        utils.validator.is_valid.assert_called_once()

    def test_slots_restriction(self):
        utils = CnpjUtils()

        with pytest.raises(AttributeError):
            utils.new_attribute = "test"

        assert hasattr(utils, "formatter")
        assert hasattr(utils, "generator")
        assert hasattr(utils, "validator")
