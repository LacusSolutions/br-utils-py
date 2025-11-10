"""
Testes unitários para br-utils.
"""

import pytest
from br_utils import hello_world


def test_hello_world():
    """Testa a função hello_world."""
    assert hello_world() == "Hello from br-utils!"


def test_dependencies_available():
    """Testa se as dependências estão disponíveis."""
    try:
        from lacus import cnpj_utils, cpf_utils

        assert cnpj_utils is not None
        assert cpf_utils is not None
    except ImportError:
        pytest.skip("Dependências não instaladas")
