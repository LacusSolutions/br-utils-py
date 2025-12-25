from unittest.mock import ANY, MagicMock

from cpf_utils import CpfUtils


class CpfUtilsFormatterTest:
    def test_format_forwards_arguments(self):
        utils = CpfUtils()
        utils.formatter = MagicMock()
        utils.formatter.format.return_value = "123.456.789-01"

        result = utils.format(
            "12345678901",
            hidden=True,
            hidden_key="X",
            escape=True,
            on_fail=lambda x: x,
        )

        assert result == "123.456.789-01"
        utils.formatter.format.assert_called_once_with(
            "12345678901",
            True,
            "X",
            None,
            None,
            None,
            None,
            True,
            ANY,
        )
