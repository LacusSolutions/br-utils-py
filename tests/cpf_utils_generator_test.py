from unittest.mock import MagicMock

from cpf_utils import CpfUtils


class CpfUtilsGeneratorTest:
    def test_generate_forwards_arguments(self):
        utils = CpfUtils()
        utils.generator = MagicMock()
        utils.generator.generate.return_value = "123.456.789-01"

        result = utils.generate(format=True, prefix="123456789")

        assert result == "123.456.789-01"
        utils.generator.generate.assert_called_once_with(
            True,
            "123456789",
        )
