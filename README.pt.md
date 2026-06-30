![cnpj-val para Python](https://br-utils.vercel.app/img/cover_cnpj-val.jpg)

> 🚀 **Suporte total ao [novo formato alfanumérico de CNPJ](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-val/README.md)

Utilitário em Python para validar CNPJ (Cadastro Nacional da Pessoa Jurídica).

## Recursos

- ✅ **CNPJ alfanumérico**: Valida CNPJ de 14 caracteres no formato numérico ou alfanumérico
- ✅ **Entrada flexível**: Aceita `str` ou sequência de `str`; elementos da sequência são concatenados na ordem
- ✅ **Agnóstico ao formato**: Remove caracteres não alfanuméricos (ou não numéricos quando `type` é `numeric`) e opcionalmente converte para maiúsculas antes de validar
- ✅ **Sensibilidade a maiúsculas opcional**: Com `case_sensitive` em `False`, letras minúsculas são aceitas para CNPJ alfanumérico
- ✅ **Sobrescrita por chamada**: Padrões da instância podem ser sobrescritos apenas naquela chamada a `is_valid()`
- ✅ **Validação tipada de opções**: Subclasses de `TypeError` / `Exception` para uso inválido de opções ou entrada
- ✅ **Dependências mínimas**: [`cnpj-dv`](https://pypi.org/project/cnpj-dv/) para cálculo dos dígitos verificadores e [`lacus.utils`](https://pypi.org/project/lacus.utils/) para descrição de tipos nas mensagens de erro
- ✅ **API dupla**: Orientada a objetos (`CnpjValidator`) e funcional (`cnpj_val()`)

## Instalação

```bash
$ pip install cnpj-val
```

## Importação

```python
from cnpj_val import CnpjValidator, CnpjValidatorOptions, cnpj_val
```

## Início rápido

```python
from cnpj_val import CnpjValidator

validator = CnpjValidator()

validator.is_valid('98765432000198')       # True
validator.is_valid('98.765.432/0001-98')   # True
validator.is_valid('98765432000199')       # False

validator.is_valid('1QB5UKALPYFP59')                         # True (alfanumérico)
validator.is_valid('1QB5UKALpyfp59')                         # False (padrão é case-sensitive)
validator.is_valid('1QB5UKALpyfp59', case_sensitive=False)   # True

validator.is_valid('96206256120884')              # True (numérico)
validator.is_valid('1QB5UKALPYFP59', type='numeric')   # False (letras removidas → comprimento ≠ 14)
```

Helper funcional:

```python
from cnpj_val import cnpj_val

cnpj_val('98765432000198')      # True
cnpj_val('98.765.432/0001-98')  # True
cnpj_val('98765432000199')      # False
```

## Utilização

Os pontos principais são a classe `CnpjValidator`, a classe de opções `CnpjValidatorOptions` e o helper `cnpj_val()`.

### `CnpjValidator`

- **`__init__`**: Opções padrão de validação. O primeiro parâmetro pode ser `None`, um mapeamento de chaves de opção ou uma instância de `CnpjValidatorOptions` (essa instância é armazenada; alterações posteriores afetam chamadas a `is_valid()` que não passarem opções por chamada). Também é possível passar campos como argumentos nomeados exclusivos (`case_sensitive`, `type`). Exemplo: `CnpjValidator(type='numeric', case_sensitive=False)`.
- **`options`**: Propriedade que retorna o `CnpjValidatorOptions` da instância (o mesmo objeto usado internamente).
- **`is_valid(cnpj_input, options=None, *, case_sensitive=None, type=None)`**: Valida um valor CNPJ.

  A entrada é normalizada para string (sequências de strings são concatenadas). Quando `case_sensitive` é `False`, a string é convertida para maiúsculas antes da sanitização. Caracteres são removidos conforme `type`. Se o comprimento após sanitização não for exatamente **14**, se os dois últimos caracteres não forem dígitos ou se os dígitos verificadores não coincidirem (`CnpjCheckDigits` de **`cnpj-dv`**), o método retorna `False` — nenhuma exceção é lançada por falha de validação.

  Se a entrada não for `str` nem sequência de `str`, é lançada **`CnpjValidatorInputTypeError`**.

  As opções por chamada são mescladas sobre os padrões da instância apenas naquela chamada (os padrões da instância não mudam). É possível passar uma instância de `CnpjValidatorOptions` ou um mapeamento como segundo argumento, além de argumentos nomeados exclusivos; quando ambos forem fornecidos, o argumento `options` prevalece.

```python
from cnpj_val import CnpjValidator

validator = CnpjValidator(type='numeric')

validator.is_valid('98.765.432/0001-98')   # True
validator.is_valid('1QB5UKALPYFP59')       # False (letras removidas → comprimento ≠ 14)
validator.is_valid('1QB5UKALpyfp59', type='alphanumeric', case_sensitive=False)  # True
```

Padrões na instância; sobrescrita por chamada:

```python
validator = CnpjValidator(case_sensitive=False)

validator.is_valid('1qb5ukalpyfp59')                  # True (padrões da instância)
validator.is_valid('1qb5ukalpyfp59', case_sensitive=True)  # só nesta chamada: False
validator.is_valid('1qb5ukalpyfp59')                  # True de novo
```

### `CnpjValidatorOptions`

Armazena configurações do validador (`case_sensitive`, `type`). Construa com um mapeamento opcional ou instância de `CnpjValidatorOptions`, objetos extras de sobrescrita (mesclados em ordem) e/ou argumentos nomeados exclusivos. Expõe propriedades: `case_sensitive`, `type`.

- **`all`**: Retorna um snapshot superficial imutável de todas as opções atuais (`MappingProxyType`).
- **`set(options)`**: Atualiza vários campos de uma vez; retorna `self`. Aceita um mapeamento ou outra instância de `CnpjValidatorOptions`.

```python
from cnpj_val import CnpjValidatorOptions

options = CnpjValidatorOptions(case_sensitive=False, type='numeric')
options.case_sensitive   # False
options.type             # 'numeric'
options.set({'type': 'alphanumeric'})  # mescla e retorna self
options.all              # snapshot imutável das opções atuais
```

### Helper funcional

`cnpj_val()` instancia um novo `CnpjValidator` com os mesmos parâmetros do construtor e chama `is_valid(cnpj_input)` uma vez. Use argumentos nomeados exclusivos, um mapeamento ou uma instância de `CnpjValidatorOptions` para as opções:

```python
from cnpj_val import cnpj_val

cnpj_val('98765432000198')                              # True
cnpj_val('1QB5UKALpyfp59', case_sensitive=False)        # True
cnpj_val('1QB5UKALPYFP59', type='numeric')              # False
cnpj_val('1QB5UKALpyfp59', {                            # forma com mapeamento
    'type': 'alphanumeric',
    'case_sensitive': False,
})                                                      # True
```

### Formatos de entrada

**String:** Dígitos e/ou letras brutos, ou CNPJ já formatado (ex.: `98.765.432/0001-98`, `1Q.B5U.KAL/PYFP-59`). Caracteres são removidos conforme `type`; quando `case_sensitive` é `False`, letras são convertidas para maiúsculas antes da validação alfanumérica.

**Sequência de strings:** Cada elemento deve ser `str`; os valores são concatenados (ex.: por dígito, segmentos agrupados ou misturados com pontuação). Elementos que não sejam string lançam **`CnpjValidatorInputTypeError`**.

```python
from cnpj_val import cnpj_val

cnpj_val(['1', 'Q', 'B', '5', 'U', 'K', 'A', 'L', 'P', 'Y', 'F', 'P', '5', '9'])  # True
cnpj_val(['1Q.B5U', 'KAL', 'PYFP-59'])  # True
```

### Opções de validação

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `type` | `'alphanumeric'` \| `'numeric'` \| `None` | `'alphanumeric'` | Conjunto de caracteres após sanitização: alfanumérico (`0`–`9`, `A`–`Z`, `a`–`z`) ou apenas numérico (`0`–`9`) |
| `case_sensitive` | `bool \| None` | `True` | Se `False`, letras minúsculas são convertidas para maiúsculas antes da validação alfanumérica |

CNPJ inválido (comprimento errado após sanitização, dígitos verificadores inválidos, base/filial inelegíveis `00000000` / `0000`, dígitos repetidos, caracteres não numéricos nos verificadores) retorna **`False`** — nenhuma exceção é lançada por falha de validação.

Exemplo com todas as opções:

```python
from cnpj_val import cnpj_val

cnpj_val(
    '1QB5UKALpyfp59',
    type='alphanumeric',
    case_sensitive=False,
)
```

### Erros e exceções

Este pacote usa **TypeError** para tipos inválidos de opção/entrada e **Exception** para valores inválidos de opção. Falhas de validação retornam `False`.

- **Tipo de entrada incorreto** (não `str` nem sequência de `str`): **`CnpjValidatorInputTypeError`** — estende **`CnpjValidatorTypeError`** (estende `TypeError` nativo).
- **Tipos de opção inválidos ao construir ou mesclar opções**: **`CnpjValidatorOptionsTypeError`**.
- **Valor inválido de `type`** (não `alphanumeric` / `numeric`): **`CnpjValidatorOptionTypeInvalidException`** — estende **`CnpjValidatorException`**.

```python
from cnpj_val import (
    CnpjValidator,
    CnpjValidatorException,
    CnpjValidatorInputTypeError,
    CnpjValidatorOptionsTypeError,
    CnpjValidatorOptionTypeInvalidException,
    cnpj_val,
)

# Tipo de entrada (ex.: inteiro não permitido)
try:
    cnpj_val(12345678000198)
except CnpjValidatorInputTypeError as e:
    print(e)  # CNPJ input must be of type string or string[]. Got integer number.

# Tipo de opção (ex.: `type` deve ser string)
try:
    cnpj_val('98765432000198', type=123)
except CnpjValidatorOptionsTypeError as e:
    print(e.option_name, e.expected_type, e.actual_type)

# Valor inválido de type
try:
    cnpj_val('98765432000198', type='invalid')
except CnpjValidatorOptionTypeInvalidException as e:
    print(e.expected_values, e.actual_input)

# Qualquer exceção do pacote
try:
    CnpjValidator(type='invalid')
except CnpjValidatorException as e:
    pass  # tratar
```

## API

### Exportações

Todos os símbolos públicos estão disponíveis no pacote `cnpj_val`:

- **`cnpj_val`**: `(cnpj_input: CnpjInput, options=None, *, case_sensitive=None, type=None) -> bool` — helper de conveniência.
- **`CnpjValidator`**: Classe para validar CNPJ com opções padrão opcionais; aceita `CnpjInput` em `is_valid()`.
- **`CnpjValidatorOptions`**: Classe que armazena opções; suporta mesclagem via construtor, `set()` e argumentos nomeados exclusivos.
- **`CNPJ_LENGTH`**: `14` (constante).
- **`CnpjInput`**: Alias de tipo — `str | Sequence[str]`.
- **`CnpjType`**: Alias de tipo — `Literal["alphanumeric", "numeric"]`.
- **`CnpjValidatorOptionsInput`**, **`CnpjValidatorOptionsType`**: Auxiliares de tipagem de opções.
- **Exceções**: `CnpjValidatorTypeError`, `CnpjValidatorInputTypeError`, `CnpjValidatorOptionsTypeError`, `CnpjValidatorException`, `CnpjValidatorOptionTypeInvalidException`.

### Outros recursos disponíveis

- **`CnpjValidatorOptions.CNPJ_LENGTH`**: `14`.
- **`CnpjValidatorOptions.DEFAULT_CASE_SENSITIVE`**: `True`.
- **`CnpjValidatorOptions.DEFAULT_TYPE`**: `'alphanumeric'`.

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela ao repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Consulte o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-val/CHANGELOG.md) para histórico de versões e alterações.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
