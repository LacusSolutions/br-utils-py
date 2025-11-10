"""
Testes unitários para lacus-cnpj-val.
"""

from lacus.cnpj_val import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cnpj-val!"
