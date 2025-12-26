"""Unit tests for br-utils."""

import pytest
from br_utils import br_utils


def test_br_utils():
    """Test br_utils function."""
    assert br_utils() == "Hello, 'br-utils'!"


def test_dependencies_available():
    """Test if dependencies are available."""
    try:
        import cnpj_utils
        import cpf_utils

        assert cnpj_utils is not None
        assert cpf_utils is not None
    except ImportError:
        pytest.skip("Dependencies not installed")
