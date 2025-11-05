"""
Testes unitários para lacus-cnpj-fmt.
"""

import pytest
from lacus.cnpj_fmt import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cnpj-fmt!"
