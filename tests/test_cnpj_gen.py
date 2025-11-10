"""
Testes unitários para lacus-cnpj-gen.
"""

from lacus.cnpj_gen import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cnpj-gen!"
