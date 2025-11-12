"""Unit tests for cpf-gen."""

from cpf_gen import cpf_gen


def test_cpf_gen():
    """Test cpf_gen function."""
    assert cpf_gen() == "Hello, 'cpf-gen'!"
