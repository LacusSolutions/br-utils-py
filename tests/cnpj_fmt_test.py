"""Unit tests for cnpj-fmt."""

from cnpj_fmt import cnpj_fmt


def test_cnpj_fmt():
    """Test cnpj_fmt function."""
    assert cnpj_fmt() == "Hello, 'cnpj-fmt'!"
