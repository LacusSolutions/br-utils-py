from unittest.mock import MagicMock

from cnpj_utils import CnpjUtils


class CnpjUtilsGeneratorTest:
    def test_generate_forwards_arguments(self):
        utils = CnpjUtils()
        utils.generator = MagicMock()
        utils.generator.generate.return_value = "12.345.678/0001-90"

        result = utils.generate(format=True, prefix="12345678")

        assert result == "12.345.678/0001-90"
        utils.generator.generate.assert_called_once_with(
            True,
            "12345678",
        )
