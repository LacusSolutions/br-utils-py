"""
Testes unitários para lacus-cpf-fmt.
"""

import pytest
from lacus.cpf_fmt import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cpf-fmt!"
