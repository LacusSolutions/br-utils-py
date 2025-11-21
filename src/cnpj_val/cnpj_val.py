from .cnpj_validator import CnpjValidator

__all__ = ["cnpj_val"]


def cnpj_val(cnpj_string: str) -> bool:
    return CnpjValidator().is_valid(cnpj_string)
