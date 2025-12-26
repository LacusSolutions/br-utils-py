from cnpj_utils import CnpjUtils
from cpf_utils import CpfUtils


class BrUtils:
    """Class to consolidate Brazilian utilities for CPF and CNPJ manipulation."""

    __slots__ = ("cnpj", "cpf")

    def __init__(self):
        self.cpf = CpfUtils()
        self.cnpj = CnpjUtils()
