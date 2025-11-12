"""Unit tests for cpf-utils."""

import pytest
from cpf_utils import cpf_utils


def test_cpf_utils():
    """Test cpf_utils function."""
    assert cpf_utils() == "Hello, 'cpf-utils'!"


def test_dependencies_available():
    """Test if dependencies are available."""
    try:
        import cpf_fmt
        import cpf_gen
        import cpf_val

        assert cpf_fmt is not None
        assert cpf_gen is not None
        assert cpf_val is not None
    except ImportError:
        pytest.skip("Dependencies not installed")
