from unittest.mock import ANY, MagicMock

from cnpj_utils import CnpjUtils


class CnpjUtilsFormatterTest:
    def test_format_forwards_arguments(self):
        utils = CnpjUtils()
        utils.formatter = MagicMock()
        utils.formatter.format.return_value = "12.345.678/0001-90"

        result = utils.format(
            "12345678000190",
            hidden=True,
            hidden_key="X",
            escape=True,
            on_fail=lambda x: x,
        )

        assert result == "12.345.678/0001-90"
        utils.formatter.format.assert_called_once_with(
            "12345678000190",
            True,
            "X",
            None,
            None,
            None,
            None,
            None,
            True,
            ANY,
        )
