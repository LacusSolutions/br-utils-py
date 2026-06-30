![cnpj-gen para Python](https://br-utils.vercel.app/img/cover_cnpj-gen.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-gen)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

> 🚀 **Suporte total ao [novo formato alfanumérico de CNPJ](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Access documentation in English](./README.md)

Utilitário em Python para gerar CNPJs válidos (Cadastro Nacional da Pessoa Jurídica).

## Suporte a Python

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Recursos

- ✅ **CNPJ alfanumérico**: Gera CNPJ de 14 caracteres com conjuntos opcionais numérico, alfabético ou alfanumérico (padrão)
- ✅ **Prefixo opcional**: Informe de 0 a 12 caracteres alfanuméricos para fixar o início do CNPJ (ex.: base) e gerar o restante com dígitos verificadores válidos
- ✅ **Formatação**: Opção de retornar a string no formato padrão (`00.000.000/0000-00`)
- ✅ **Gerador reutilizável**: Classe `CnpjGenerator` com opções padrão e sobrescritas por chamada
- ✅ **Type hints**: Desenvolvido para Python 3.10+ com anotações de tipo completas
- ✅ **Dependências mínimas**: Apenas pacotes internos `lacus.utils` e `cnpj-dv` para geração de sequência aleatória e cálculo dos dígitos verificadores
- ✅ **Tratamento de erros**: Erros de tipo e exceções específicas para opções inválidas

## Instalação

```bash
$ pip install cnpj-gen
```

## Início rápido

```python
from cnpj_gen import cnpj_gen
```

Uso básico:

```python
cnpj_gen()                    # ex.: 'AB123CDE000155' (14 caracteres alfanuméricos)

cnpj_gen(format=True)         # ex.: 'AB.123.CDE/0001-55'

cnpj_gen(prefix='45623767')   # ex.: '45623767ABCD96' (com type alfanumérico padrão)
cnpj_gen(                     # ex.: '45.623.767/ABCD-96'
    prefix='45623767',
    format=True,
)

cnpj_gen(type='numeric')      # ex.: '65453043000178' (apenas dígitos)
cnpj_gen(type='alphabetic')   # ex.: 'ABCDEFGHIJKL80' (apenas letras, exceto dígitos verificadores)
```

As opções também podem ser passadas como um mapeamento:

```python
cnpj_gen({'format': True, 'type': 'numeric'})
```

## Utilização

### Opções do gerador

Todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | Se `True`, retorna o CNPJ gerado no formato padrão (`00.000.000/0000-00`). Valores não booleanos são convertidos com `bool()`. |
| `prefix` | `str` | `''` | String inicial parcial (0–12 caracteres alfanuméricos). Apenas alfanuméricos são mantidos e convertidos para maiúsculas; os caracteres faltantes são gerados aleatoriamente e os dígitos verificadores são calculados. |
| `type` | `'numeric'` \| `'alphabetic'` \| `'alphanumeric'` | `'alphanumeric'` | Conjunto de caracteres da parte gerada aleatoriamente (o `prefix` é mantido após sanitização). **Os dígitos verificadores são sempre numéricos.** |

Regras do prefixo: a base (primeiros 8 caracteres) e a filial (caracteres 9–12) não podem ser todos zeros; 12 dígitos repetidos (ex.: `777777777777`) também não são permitidos.

### `cnpj_gen` (função auxiliar)

Gera uma string de CNPJ válida. Sem opções, retorna um CNPJ alfanumérico de 14 caracteres. É um atalho para `CnpjGenerator(options, ...).generate()`.

- **`options`** (opcional): `CnpjGeneratorOptionsInput` — instância de `CnpjGeneratorOptions`, mapeamento parcial ou `None`. Veja [Opções do gerador](#opções-do-gerador).
- **`format`**, **`prefix`**, **`type`** (somente por palavra-chave): Sobrescritas por opção quando `options` é omitido ou para compor sobre um mapeamento.

### `CnpjGenerator` (classe)

Para padrões reutilizáveis ou sobrescritas por chamada, use a classe:

```python
from cnpj_gen import CnpjGenerator

generator = CnpjGenerator(type='numeric', format=True)

generator.generate()                        # ex.: '73.008.535/0005-06'
generator.generate(prefix='12345678')       # sobrescrita apenas nesta chamada
generator.options                           # opções padrão atuais (CnpjGeneratorOptions)
```

- **`__init__(options=None, *, format=None, prefix=None, type=None)`**: Opções padrão opcionais (mapeamento simples, instância de `CnpjGeneratorOptions` ou argumentos nomeados).
- **`generate(options=None, *, format=None, prefix=None, type=None)`**: Retorna um CNPJ válido; opções por chamada sobrescrevem os padrões da instância apenas naquela chamada.
- **`options`**: Propriedade que retorna as opções padrão usadas quando não há opções por chamada (mesma instância usada internamente; mutá-la afeta futuras chamadas de `generate`).

Opções padrão na instância; sobrescritas por chamada:

```python
generator = CnpjGenerator(format=True)

generator.generate()              # CNPJ formatado
generator.generate(format=False)  # somente nesta chamada: sem formato
generator.generate()              # volta ao padrão da instância
```

### `CnpjGeneratorOptions` (classe)

Armazena opções (`format`, `prefix`, `type`) com validação e suporte a mesclagem:

```python
from cnpj_gen import CnpjGeneratorOptions

options = CnpjGeneratorOptions(
    prefix='AB123XYZ',
    type='numeric',
    format=True,
)
options.prefix   # 'AB123XYZ'
options.type     # 'numeric'
options.format   # True
options.set({'format': False})  # mescla e retorna self
options.all      # snapshot imutável e superficial das opções atuais
```

- **`__init__(default_options=None, *overrides, format=None, prefix=None, type=None)`**: Opções mescladas em ordem (as últimas sobrescritas prevalecem).
- **`format`**, **`prefix`**, **`type`**: Propriedades com setters; `prefix` é validado (base/filial inelegíveis, dígitos repetidos).
- **`set(options)`**: Atualiza várias opções de uma vez; campos omitidos mantêm o valor atual; retorna `self`.
- **`all`**: Snapshot somente leitura das opções atuais (`MappingProxyType`).
- **`DEFAULT_FORMAT`**, **`DEFAULT_PREFIX`**, **`DEFAULT_TYPE`**: Constantes de padrão no nível da classe.

## API

### Exportações

- **`cnpj_gen`**: `(options=None, *, format=None, prefix=None, type=None) -> str`
- **`CnpjGenerator`**: Classe para gerar CNPJ com opções padrão e sobrescritas por chamada.
- **`CnpjGeneratorOptions`**: Classe que armazena opções (`format`, `prefix`, `type`) com validação e mesclagem.
- **`CNPJ_LENGTH`**: `14` (constante).
- **`CNPJ_PREFIX_MAX_LENGTH`**: `12` (constante).
- **Tipos**: `CnpjType`, `CnpjGeneratorOptionsInput`, `CnpjGeneratorOptionsType`.
- **Exceções**: `CnpjGeneratorTypeError`, `CnpjGeneratorOptionsTypeError`, `CnpjGeneratorException`, `CnpjGeneratorOptionPrefixInvalidException`, `CnpjGeneratorOptionTypeInvalidException`.

### Erros e exceções

Este pacote usa subclasses de **TypeError** para tipos de opção inválidos e subclasses de **Exception** para valores de opção inválidos (`prefix` ou `type`). Você pode capturar classes específicas ou os tipos base.

- **CnpjGeneratorTypeError** (_abstrata_) — base para erros de tipo de opção
- **CnpjGeneratorOptionsTypeError** — uma opção tem o tipo errado (ex.: `prefix` não é string)
- **CnpjGeneratorException** (_abstrata_) — base para exceções de valor de opção
- **CnpjGeneratorOptionPrefixInvalidException** — prefixo inválido (ex.: base/filial zerada, dígitos repetidos)
- **CnpjGeneratorOptionTypeInvalidException** — `type` não é um de `'numeric'`, `'alphabetic'`, `'alphanumeric'`

```python
from cnpj_gen import (
    cnpj_gen,
    CnpjGeneratorOptionsTypeError,
    CnpjGeneratorOptionPrefixInvalidException,
    CnpjGeneratorOptionTypeInvalidException,
    CnpjGeneratorException,
)

# Tipo de opção (ex.: `prefix` deve ser string)
try:
    cnpj_gen(prefix=123)
except CnpjGeneratorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Prefixo inválido (ex.: base zerada)
try:
    cnpj_gen(prefix='000000000001')
except CnpjGeneratorOptionPrefixInvalidException as e:
    print(e.reason, e.actual_input)

# Valor de type inválido
try:
    cnpj_gen(type='invalid')
except CnpjGeneratorOptionTypeInvalidException as e:
    print(e.expected_values, e.actual_input)

# Qualquer exceção do pacote
try:
    cnpj_gen(prefix='000000000000')
except CnpjGeneratorException as e:
    print(e)
```

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela no repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Veja o [CHANGELOG](./CHANGELOG.md) para histórico de versões e alterações.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
