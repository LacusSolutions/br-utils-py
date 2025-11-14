"""Unit tests for cpf-fmt."""

from cpf_fmt import cpf_fmt


def test_cpf_fmt():
    """Test cpf_fmt function."""
    assert cpf_fmt() == "Hello, 'cpf-fmt'!"
