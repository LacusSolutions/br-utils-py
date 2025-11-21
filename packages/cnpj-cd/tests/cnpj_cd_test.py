"""Unit tests for cnpj-cd."""

import pytest
from cnpj_cd import cnpj_cd


def test_cnpj_cd():
    """Test cnpj_cd function."""
    assert cnpj_cd() == "Hello, 'cnpj-cd'!"


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
