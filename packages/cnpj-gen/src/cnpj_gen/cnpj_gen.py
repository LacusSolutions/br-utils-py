from .cnpj_generator import CnpjGenerator


def cnpj_gen(format: bool | None = None, prefix: str | None = None) -> str:
    generator = CnpjGenerator(format, prefix)

    return generator.generate()
