"""
Testes unitários para lacus-cnpj-utils.
"""

import pytest
from lacus.cnpj_utils import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from lacus-cnpj-utils!"


def test_dependencies_available():
    """Testa se as dependências estão disponíveis."""
    try:
        from lacus import cnpj_fmt, cnpj_gen, cnpj_val
        assert cnpj_fmt is not None
        assert cnpj_gen is not None
        assert cnpj_val is not None
    except ImportError:
        pytest.skip("Dependências não instaladas")
