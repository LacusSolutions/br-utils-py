"""Unit tests for br-utils."""

import pytest
from br_utils import BrUtils, br_utils


class BrUtilsInitTest:
    def test_init_creates_cpf_and_cnpj_instances(self):
        utils = BrUtils()

        assert utils.cpf is not None
        assert utils.cnpj is not None

    def test_default_instance_is_available(self):
        assert br_utils is not None
        assert isinstance(br_utils, BrUtils)

    def test_slots_restriction(self):
        utils = BrUtils()

        with pytest.raises(AttributeError):
            utils.new_attribute = "test"

        assert hasattr(utils, "cpf")
        assert hasattr(utils, "cnpj")
