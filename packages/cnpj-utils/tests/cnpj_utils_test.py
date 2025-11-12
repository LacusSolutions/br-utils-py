"""Unit tests for cnpj-utils."""

import pytest
from cnpj_utils import cnpj_utils


def test_cnpj_utils():
    """Test cnpj_utils function."""
    assert cnpj_utils() == "Hello, 'cnpj-utils'!"


def test_dependencies_available():
    """Test if dependencies are available."""
    try:
        import cnpj_fmt
        import cnpj_gen
        import cnpj_val

        assert cnpj_fmt is not None
        assert cnpj_gen is not None
        assert cnpj_val is not None
    except ImportError:
        pytest.skip("Dependencies not installed")
