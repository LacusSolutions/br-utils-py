![cnpj-utils para Python](https://br-utils.vercel.app/img/cover_cnpj-utils.jpg)

> 🚀 **Suporte total ao [novo formato alfanumérico de CNPJ](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Access documentation in English](./README.md)

Utilitários para lidar com CNPJ (Cadastro Nacional da Pessoa Jurídica). Este pacote envolve [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt), [`cnpj-gen`](https://pypi.org/project/cnpj-gen) e [`cnpj-val`](https://pypi.org/project/cnpj-val) em uma única API e reexporta os recursos públicos deles.

## Recursos

- ✅ **API unificada**: Uma instância padrão com `format`, `generate` e `is_valid`; ou uso direto dos helpers `cnpj_fmt`, `cnpj_gen` e `cnpj_val`
- ✅ **CNPJ alfanumérico**: Formatar, gerar e validar CNPJ de 14 caracteres numérico ou alfanumérico
- ✅ **Instância reutilizável**: Classe `CnpjUtils` com configurações padrão opcionais (opções ou instâncias do formatador, gerador e validador)
- ✅ **Reexportações completas**: Todas as classes, opções e exceções do formatador, gerador e validador dos três pacotes componentes
- ✅ **Type hints**: Desenvolvido para Python 3.10+ com anotações de tipo completas
- ✅ **Entrada flexível**: `format()` e `is_valid()` aceitam `str` ou sequência de `str` (elementos concatenados em ordem)
- ✅ **Sobrescritas por chamada**: Padrões da instância mais sobrescritas por palavra-chave ou mapeamento em cada chamada de método
- ✅ **Tratamento de erros**: Mesmos erros de tipo e exceções dos pacotes subjacentes

## Instalação

```bash
$ pip install cnpj-utils
```

Isso instala **`cnpj-utils`** junto com [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt), [`cnpj-gen`](https://pypi.org/project/cnpj-gen) e [`cnpj-val`](https://pypi.org/project/cnpj-val). Você **não** precisa de chamadas `pip install` separadas para os pacotes componentes ao usar **`cnpj-utils`**.

## Início rápido

```python
from cnpj_utils import CnpjUtils, cnpj_fmt, cnpj_gen, cnpj_val, cnpj_utils
```

Uso básico com o singleton padrão:

```python
from cnpj_utils import cnpj_utils

cnpj = '03603568000195'

cnpj_utils.format(cnpj)                # '03.603.568/0001-95'
cnpj_utils.format(cnpj, hidden=True)   # '03.603.***/****-**'
cnpj_utils.format(                     # '03603568|0001_95'
    cnpj,
    dot_key='',
    slash_key='|',
    dash_key='_',
)

cnpj_utils.generate()                    # ex.: 'AB123CDE000155' (14 caracteres alfanuméricos)
cnpj_utils.generate(format=True)         # ex.: 'AB.123.CDE/0001-55'
cnpj_utils.generate(prefix='45623767')   # ex.: '45623767000296'
cnpj_utils.generate(type='numeric')      # ex.: '65453043000178' (apenas dígitos)

cnpj_utils.is_valid('98765432000198')       # True
cnpj_utils.is_valid('98.765.432/0001-98')   # True
cnpj_utils.is_valid('1QB5UKALPYFP59')       # True (alfanumérico)
cnpj_utils.is_valid('98765432000199')       # False
```

## Utilização

Você pode trabalhar de três formas equivalentes:

1. **`cnpj_utils`** — singleton pré-construído para chamadas rápidas.
2. **`CnpjUtils`** — instância configurável com padrões compartilhados entre formatar, gerar e validar.
3. **Classes componentes e helpers** — `CnpjFormatter`, `CnpjGenerator`, `CnpjValidator` e `cnpj_fmt()`, `cnpj_gen()`, `cnpj_val()` (as mesmas classes usadas internamente por `CnpjUtils`).

As três abordagens expõem as mesmas opções e comportamento. Para tabelas de opções exaustivas e detalhes específicos de cada componente, consulte o README de cada [pacote incluído](#pacotes-incluidos).

### Opções do formatador

Em `format(cnpj_input, options=None, …)`, todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `hidden` | `bool` | `False` | Se `True`, mascara caracteres entre `hidden_start` e `hidden_end` com `hidden_key` |
| `hidden_key` | `str` | `'*'` | Caractere(s) usados para substituir os caracteres mascarados |
| `hidden_start` | `int` | `5` | Índice inicial (0–13, inclusivo) do intervalo a ocultar |
| `hidden_end` | `int` | `13` | Índice final (0–13, inclusivo) do intervalo a ocultar |
| `dot_key` | `str` | `'.'` | Delimitador de ponto (ex.: em `12.345.678`) |
| `slash_key` | `str` | `'/'` | Delimitador de barra (ex.: antes da filial `…/0001-90`) |
| `dash_key` | `str` | `'-'` | Delimitador de hífen (ex.: antes dos dígitos verificadores `…-90`) |
| `escape` | `bool` | `False` | Se `True`, escapa caracteres especiais HTML no resultado |
| `encode` | `bool` | `False` | Se `True`, codifica o resultado para URL (similar ao `encodeURIComponent` do JavaScript) |
| `on_fail` | `Callable` | retorna `''` | Callback quando o tamanho da entrada sanitizada ≠ 14; o retorno é usado como resultado |

### Opções do gerador

Em `generate(options=None, …)`, todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | Se `True`, retorna o CNPJ gerado no formato padrão (`00.000.000/0000-00`) |
| `prefix` | `str` | `''` | String inicial parcial (0–12 caracteres alfanuméricos). Os caracteres faltantes são gerados e os dígitos verificadores calculados. |
| `type` | `'numeric'` \| `'alphabetic'` \| `'alphanumeric'` | `'alphanumeric'` | Conjunto de caracteres da parte gerada aleatoriamente. **Os dígitos verificadores são sempre numéricos.** |

Regras do prefixo: a base (primeiros 8 caracteres) e a filial (caracteres 9–12) não podem ser todos zeros; 12 dígitos repetidos (ex.: `111111111111`) também não são permitidos.

### Opções do validador

Em `is_valid(cnpj_input, options=None, …)`, todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `case_sensitive` | `bool` | `True` | Se `False`, letras minúsculas são aceitas para CNPJ alfanumérico (a entrada é convertida para maiúsculas antes da validação). |
| `type` | `'numeric'` \| `'alphanumeric'` | `'alphanumeric'` | `'numeric'`: apenas dígitos (0–9); `'alphanumeric'`: dígitos e letras (0–9, A–Z). |

### `cnpj_utils` (instância padrão)

O `cnpj_utils` em nível de módulo é uma instância pré-construída de `CnpjUtils`. Use-o para chamadas rápidas:

- **`format(cnpj_input, options=None, …)`**: Formata uma string CNPJ ou sequência de strings. Delega ao formatador interno. A entrada deve ter 14 caracteres alfanuméricos (após sanitização); caso contrário, `on_fail` é usado.
- **`generate(options=None, …)`**: Gera um CNPJ válido. Delega ao gerador interno.
- **`is_valid(cnpj_input, options=None, …)`**: Retorna `True` se o CNPJ for válido. Delega ao validador interno.

### `CnpjUtils` (classe)

Para formatador, gerador ou validador padrão personalizados, crie sua própria instância:

```python
from cnpj_utils import CnpjUtils

utils = CnpjUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'type': 'numeric', 'format': True},
    validator={'type': 'numeric', 'case_sensitive': False},
)

utils.format('RK0CMT3W000100')         # 'RK.0CM.###/####-##'
utils.generate()                       # ex.: '73.008.535/0005-06'
utils.is_valid('98.765.432/0001-98')   # True

# Acessar ou substituir instâncias internas
utils.formatter  # CnpjFormatter
utils.generator  # CnpjGenerator
utils.validator  # CnpjValidator
```

- **`__init__(*, formatter=None, generator=None, validator=None)`**: Cada palavra-chave pode ser um mapeamento de opções, uma instância de `CnpjFormatterOptions` / `CnpjGeneratorOptions` / `CnpjValidatorOptions` (armazenada por referência — mutá-la depois afeta chamadas subsequentes sem sobrescrita por chamada), uma instância de componente ou omitida para os padrões. Passar `None` para um componente cria uma nova instância com opções padrão.
- **`format(cnpj_input, options=None, …)`**: Igual à instância padrão; opções por chamada sobrescrevem os padrões do formatador apenas nessa chamada.
- **`generate(options=None, …)`**: Igual à instância padrão; opções por chamada sobrescrevem os padrões do gerador.
- **`is_valid(cnpj_input, options=None, …)`**: Igual à instância padrão; opções por chamada sobrescrevem os padrões do validador.
- **`formatter`**, **`generator`**, **`validator`**: Propriedades com getters e setters para o formatador, gerador e validador internos. Os setters aceitam as mesmas formas do construtor. Para alterar uma única opção sem substituir a instância, mute as opções do componente (ex.: `utils.formatter.options.hidden = True`).

Padrões da instância e sobrescritas por chamada:

```python
utils = CnpjUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True},
    validator={'type': 'numeric'},
)

cnpj = '03603568000195'

utils.format(cnpj)                 # mascarado (padrões do formatador da instância)
utils.format(cnpj, hidden=False)   # só nesta chamada: sem máscara
utils.generate(format=False)       # só nesta chamada: saída compacta
utils.is_valid('1QB5UKALPYFP59')   # False (validador da instância é só numérico)
utils.is_valid(                    # True nesta chamada
    '1QB5UKALPYFP59',
    type='alphanumeric',
)
```

As opções também podem ser passadas como mapeamento em cada método:

```python
utils.format(cnpj, {'slash_key': '|'})
utils.generate({'prefix': '12345', 'type': 'numeric'})
utils.is_valid('1QB5UKALPYFP59', {'case_sensitive': False})
```

### Usando os helpers e classes subjacentes

Você pode usar o formatador, gerador e validador reexportados diretamente:

```python
from cnpj_utils import (
    cnpj_fmt,
    CnpjFormatter,
    cnpj_gen,
    CnpjGenerator,
    cnpj_val,
    CnpjValidator,
)

cnpj_fmt('01ABC234000X56', slash_key='|')   # '01.ABC.234|000X-56'
cnpj_gen(type='numeric')                    # ex.: '65453043000178'
cnpj_val('9JN7MGLJZXIO50')                  # True

formatter = CnpjFormatter({'hidden': True})
formatter.format('AB123XYZ000123')          # 'AB.123.***/****-**'
```

Consulte [`cnpj-fmt`](./../cnpj-fmt/README.pt.md), [`cnpj-gen`](./../cnpj-gen/README.pt.md) e [`cnpj-val`](./../cnpj-val/README.pt.md) para detalhes completos de opções e erros.

## API

### Exportações

- **`cnpj_utils`**: Instância pré-construída de `CnpjUtils` com `format`, `generate` e `is_valid`.
- **`CnpjUtils`**: Classe para criar uma instância com configurações padrão opcionais de formatador, gerador e validador.
- **Formatador**: `cnpj_fmt`, `CnpjFormatter`, `CnpjFormatterOptions` e exceções do formatador (veja [cnpj-fmt](./../cnpj-fmt/README.pt.md)).
- **Gerador**: `cnpj_gen`, `CnpjGenerator`, `CnpjGeneratorOptions` e exceções do gerador (veja [cnpj-gen](./../cnpj-gen/README.pt.md)).
- **Validador**: `cnpj_val`, `CnpjValidator`, `CnpjValidatorOptions` e exceções do validador (veja [cnpj-val](./../cnpj-val/README.pt.md)).

### Erros e exceções

`CnpjUtils` não define seus próprios tipos de exceção; propaga erros dos pacotes incluídos:

- **Formatação**: `CnpjFormatterInputTypeError`, `CnpjFormatterOptionsTypeError`, `CnpjFormatterOptionsHiddenRangeInvalidException`, `CnpjFormatterOptionsForbiddenKeyCharacterException` e classes relacionadas.
- **Geração**: `CnpjGeneratorOptionsTypeError`, `CnpjGeneratorOptionPrefixInvalidException`, `CnpjGeneratorOptionTypeInvalidException` e classes relacionadas.
- **Validação**: `CnpjValidatorInputTypeError`, `CnpjValidatorOptionsTypeError`, `CnpjValidatorOptionTypeInvalidException` e classes relacionadas.

Tipos de opção inválidos são subclasses de **`TypeError`**; valores de opção inválidos são subclasses de **`Exception`**. Falha de validação retorna `False`; falha de comprimento na formatação é tratada por **`on_fail`** (padrão retorna string vazia).

```python
from cnpj_utils import CnpjUtils, cnpj_fmt
from cnpj_fmt import CnpjFormatterInputTypeError
from cnpj_val import CnpjValidatorInputTypeError

try:
    CnpjUtils().format(12345)
except CnpjFormatterInputTypeError as e:
    print(e)

try:
    CnpjUtils().is_valid(12345678000198)
except CnpjValidatorInputTypeError as e:
    print(e)

# on_fail personalizado para comprimento inválido
def custom_fail(value, exception=None):
    return f'CNPJ inválido: {value}'

cnpj_fmt('123', on_fail=custom_fail)  # 'CNPJ inválido: 123'
cnpj_fmt('123')                       # '' (on_fail padrão)
```

### Pacotes incluídos

| Pacote | Principais recursos | README |
|---------|----------------|--------|
| [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt) | `CnpjFormatter`, `CnpjFormatterOptions`, `cnpj_fmt()` | [docs](./../cnpj-fmt/README.pt.md) |
| [`cnpj-gen`](https://pypi.org/project/cnpj-gen) | `CnpjGenerator`, `CnpjGeneratorOptions`, `cnpj_gen()` | [docs](./../cnpj-gen/README.pt.md) |
| [`cnpj-val`](https://pypi.org/project/cnpj-val) | `CnpjValidator`, `CnpjValidatorOptions`, `cnpj_val()` | [docs](./../cnpj-val/README.pt.md) |

Todos os pacotes acima são instalados como dependências de **`cnpj-utils`**. Para tabelas de opções exaustivas, listas de exceções e comportamento em casos extremos, consulte o README de cada pacote.

## Contribuição e suporte

Contribuições são bem-vindas! Consulte nossas [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) para detalhes. Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela ao repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a Licença MIT — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) para detalhes.

## Changelog

Consulte o [CHANGELOG](./CHANGELOG.md) para a lista de alterações e histórico de versões.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
