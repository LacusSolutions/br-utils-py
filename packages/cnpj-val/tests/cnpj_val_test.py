"""Unit tests for cnpj-val."""

from cnpj_val import cnpj_val


def test_cnpj_val():
    """Test cnpj_val function."""
    assert cnpj_val() == "Hello, 'cnpj-val'!"
