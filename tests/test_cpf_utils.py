"""
Testes unitários para lacus-cpf-utils.
"""

import pytest
from lacus.cpf_utils import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cpf-utils!"


def test_dependencies_available():
    """Testa se as dependências estão disponíveis."""
    try:
        from lacus import cpf_fmt, cpf_gen, cpf_val
        assert cpf_fmt is not None
        assert cpf_gen is not None
        assert cpf_val is not None
    except ImportError:
        pytest.skip("Dependências não instaladas")
