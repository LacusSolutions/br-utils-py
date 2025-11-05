"""
Testes unitários para lacus-cpf-gen.
"""

import pytest
from lacus.cpf_gen import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cpf-gen!"
