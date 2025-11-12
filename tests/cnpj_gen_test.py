"""Unit tests for cnpj-gen."""

from cnpj_gen import cnpj_gen


def test_cnpj_gen():
    """Test cnpj_gen function."""
    assert cnpj_gen() == "Hello, 'cnpj-gen'!"
