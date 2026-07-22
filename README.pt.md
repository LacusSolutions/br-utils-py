![cpf-gen para Python](https://br-utils.vercel.app/img/cover_cpf-gen.jpg)

> 🌎 [Access documentation in English](./README.md)

Utilitário em Python para gerar CPFs válidos (Cadastro de Pessoa Física).

## Recursos

- ✅ **Prefixo opcional**: Informe de 0 a 9 dígitos para fixar o início do CPF e gerar o restante com dígitos verificadores válidos
- ✅ **Formatação**: Opção de retornar a string no formato padrão (`000.000.000-00`)
- ✅ **Gerador reutilizável**: Classe `CpfGenerator` com opções padrão e sobrescritas por chamada
- ✅ **Type hints**: Desenvolvido para Python 3.10+ com anotações de tipo completas
- ✅ **Dependências mínimas**: Apenas pacotes internos `lacus.utils` e `cpf-dv` para geração de sequência aleatória e cálculo dos dígitos verificadores
- ✅ **Tratamento de erros**: Erros de tipo e exceções específicas para opções inválidas

## Instalação

```bash
$ pip install cpf-gen
```

## Início rápido

```python
from cpf_gen import cpf_gen
```

Uso básico:

```python
cpf_gen()                    # ex.: '47844241055' (11 dígitos numéricos)

cpf_gen(format=True)         # ex.: '005.265.352-88'

cpf_gen(prefix='528250911')  # ex.: '52825091138'
cpf_gen(                     # ex.: '528.250.911-38'
    prefix='528250911',
    format=True,
)
```

As opções também podem ser passadas como um mapeamento:

```python
cpf_gen({'format': True, 'prefix': '528250911'})
```

## Utilização

### Opções do gerador

Todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | Se `True`, retorna o CPF gerado no formato padrão (`000.000.000-00`). Valores não booleanos são convertidos com `bool()`. |
| `prefix` | `str` | `''` | String inicial parcial (0–9 dígitos). Apenas dígitos são mantidos; os caracteres faltantes são gerados aleatoriamente e os dígitos verificadores são calculados. Prefixos com mais de 9 dígitos são truncados silenciosamente. |

Regras do prefixo: a base (primeiros 9 dígitos) não pode ser toda zerada; 9 dígitos repetidos (ex.: `999999999`) não são permitidos.

### `cpf_gen` (função auxiliar)

Gera uma string de CPF válida. Sem opções, retorna um CPF numérico de 11 dígitos. É um atalho para `CpfGenerator(options, ...).generate()`.

- **`options`** (opcional): `CpfGeneratorOptionsInput` — instância de `CpfGeneratorOptions`, mapeamento parcial ou `None`. Veja [Opções do gerador](#opções-do-gerador).
- **`format`**, **`prefix`** (somente por palavra-chave): Sobrescritas por opção quando `options` é omitido ou para compor sobre um mapeamento.

### `CpfGenerator` (classe)

Para padrões reutilizáveis ou sobrescritas por chamada, use a classe:

```python
from cpf_gen import CpfGenerator

generator = CpfGenerator(format=True)

generator.generate()                  # ex.: '005.265.352-88'
generator.generate(prefix='123456')   # sobrescrita apenas nesta chamada
generator.options                   # opções padrão atuais (CpfGeneratorOptions)
```

- **`__init__(options=None, *, format=None, prefix=None)`**: Opções padrão opcionais (mapeamento simples, instância de `CpfGeneratorOptions` ou argumentos nomeados).
- **`generate(options=None, *, format=None, prefix=None)`**: Retorna um CPF válido; opções por chamada sobrescrevem os padrões da instância apenas naquela chamada.
- **`options`**: Propriedade que retorna as opções padrão usadas quando não há opções por chamada (mesma instância usada internamente; mutá-la afeta futuras chamadas de `generate`).

Opções padrão na instância; sobrescritas por chamada:

```python
generator = CpfGenerator(format=True)

generator.generate()              # CPF formatado
generator.generate(format=False)  # somente nesta chamada: sem formato
generator.generate()              # volta ao padrão da instância
```

### `CpfGeneratorOptions` (classe)

Armazena opções (`format`, `prefix`) com validação e suporte a mesclagem:

```python
from cpf_gen import CpfGeneratorOptions

options = CpfGeneratorOptions(
    prefix='123456',
    format=True,
)
options.prefix   # '123456'
options.format   # True
options.set({'format': False})  # mescla e retorna self
options.all      # snapshot imutável e superficial das opções atuais
```

- **`__init__(options=None, *extra_overrides, format=None, prefix=None)`**: Opções mescladas em ordem (as últimas sobrescritas prevalecem).
- **`format`**, **`prefix`**: Propriedades com setters; `prefix` é validado (base inelegível, dígitos repetidos).
- **`set(options)`**: Atualiza várias opções de uma vez; campos omitidos mantêm o valor atual; retorna `self`.
- **`all`**: Snapshot somente leitura das opções atuais (`MappingProxyType`).
- **`DEFAULT_FORMAT`**, **`DEFAULT_PREFIX`**: Constantes de padrão no nível da classe.

## API

### Exportações

- **`cpf_gen`**: `(options=None, *, format=None, prefix=None) -> str`
- **`CpfGenerator`**: Classe para gerar CPF com opções padrão e sobrescritas por chamada.
- **`CpfGeneratorOptions`**: Classe que armazena opções (`format`, `prefix`) com validação e mesclagem.
- **`CPF_LENGTH`**: `11` (constante).
- **`CPF_PREFIX_MAX_LENGTH`**: `9` (constante).
- **Tipos**: `CpfGeneratorOptionsInput`, `CpfGeneratorOptionsType`.
- **Exceções**: `CpfGeneratorTypeError`, `CpfGeneratorOptionsTypeError`, `CpfGeneratorException`, `CpfGeneratorOptionPrefixInvalidException`.

### Erros e exceções

Este pacote usa subclasses de **TypeError** para tipos de opção inválidos e subclasses de **Exception** para valores de opção inválidos (ex.: `prefix`). Você pode capturar classes específicas ou os tipos base.

- **CpfGeneratorTypeError** — base para erros de tipo de opção
- **CpfGeneratorOptionsTypeError** — uma opção tem o tipo errado (ex.: `prefix` não é string)
- **CpfGeneratorException** — base para exceções de valor de opção
- **CpfGeneratorOptionPrefixInvalidException** — prefixo inválido (ex.: base zerada, dígitos repetidos)

```python
from cpf_gen import (
    cpf_gen,
    CpfGeneratorOptionsTypeError,
    CpfGeneratorOptionPrefixInvalidException,
    CpfGeneratorException,
)

# Tipo de opção (ex.: `prefix` deve ser string)
try:
    cpf_gen(prefix=123)
except CpfGeneratorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Prefixo inválido (ex.: base zerada)
try:
    cpf_gen(prefix='000000000')
except CpfGeneratorOptionPrefixInvalidException as e:
    print(e.reason, e.actual_input)

# Qualquer exceção do pacote
try:
    cpf_gen(prefix='999999999')
except CpfGeneratorException as e:
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
