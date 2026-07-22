![cpf-utils para Python](https://br-utils.vercel.app/img/cover_cpf-utils.jpg)

> 🌎 [Access documentation in English](./README.md)

Utilitários para lidar com CPF (Cadastro de Pessoa Física). Este pacote envolve [`cpf-fmt`](https://pypi.org/project/cpf-fmt), [`cpf-gen`](https://pypi.org/project/cpf-gen) e [`cpf-val`](https://pypi.org/project/cpf-val) em uma única API e reexporta os recursos públicos deles.

## Recursos

- ✅ **API unificada**: Uma instância padrão com `format`, `generate` e `is_valid`; ou uso direto dos helpers `cpf_fmt`, `cpf_gen` e `cpf_val`
- ✅ **Instância reutilizável**: Classe `CpfUtils` com configurações padrão opcionais (opções ou instâncias do formatador, gerador e validador)
- ✅ **Reexportações completas**: Todas as classes, opções e exceções do formatador, gerador e validador dos três pacotes componentes
- ✅ **Type hints**: Desenvolvido para Python 3.10+ com anotações de tipo completas
- ✅ **Entrada flexível**: `format()` e `is_valid()` aceitam `str` ou sequência de `str` (elementos concatenados em ordem)
- ✅ **Sobrescritas por chamada**: Padrões da instância mais sobrescritas por palavra-chave ou mapeamento em cada chamada de método
- ✅ **Tratamento de erros**: Mesmos erros de tipo e exceções dos pacotes subjacentes

## Instalação

```bash
$ pip install cpf-utils
```

Isso instala **`cpf-utils`** junto com [`cpf-fmt`](https://pypi.org/project/cpf-fmt), [`cpf-gen`](https://pypi.org/project/cpf-gen) e [`cpf-val`](https://pypi.org/project/cpf-val). Você **não** precisa de chamadas `pip install` separadas para os pacotes componentes ao usar **`cpf-utils`**.

## Início rápido

```python
from cpf_utils import CpfUtils, cpf_fmt, cpf_gen, cpf_val, cpf_utils
```

Uso básico com o singleton padrão:

```python
from cpf_utils import cpf_utils

cpf = '12345678909'

cpf_utils.format(cpf)                # '123.456.789-09'
cpf_utils.format(cpf, hidden=True)   # '123.***.***-**'
cpf_utils.format(                     # '123456789_09'
    cpf,
    dot_key='',
    dash_key='_',
)

cpf_utils.generate()                   # ex.: '47844241055' (11 dígitos numéricos)
cpf_utils.generate(format=True)        # ex.: '478.442.410-55'
cpf_utils.generate(prefix='528250911') # ex.: '52825091138'

cpf_utils.is_valid('12345678909')      # True
cpf_utils.is_valid('123.456.789-09')   # True
cpf_utils.is_valid('12345678900')      # False
```

## Utilização

Você pode trabalhar de três formas equivalentes:

1. **`cpf_utils`** — singleton pré-construído para chamadas rápidas.
2. **`CpfUtils`** — instância configurável com padrões compartilhados entre formatar, gerar e validar.
3. **Classes componentes e helpers** — `CpfFormatter`, `CpfGenerator`, `CpfValidator` e `cpf_fmt()`, `cpf_gen()`, `cpf_val()` (as mesmas classes usadas internamente por `CpfUtils`).

As três abordagens expõem as mesmas opções e comportamento. Para tabelas de opções exaustivas e detalhes específicos de cada componente, consulte o README de cada [pacote incluído](#pacotes-incluidos).

### Opções do formatador

Em `format(cpf_input, options=None, …)`, todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `hidden` | `bool` | `False` | Se `True`, mascara dígitos entre `hidden_start` e `hidden_end` com `hidden_key` |
| `hidden_key` | `str` | `'*'` | Caractere(s) usados para substituir os dígitos mascarados |
| `hidden_start` | `int` | `3` | Índice inicial (0–10, inclusivo) do intervalo a ocultar |
| `hidden_end` | `int` | `10` | Índice final (0–10, inclusivo) do intervalo a ocultar |
| `dot_key` | `str` | `'.'` | Delimitador de ponto (ex.: em `123.456.789`) |
| `dash_key` | `str` | `'-'` | Delimitador de hífen (ex.: antes dos dígitos verificadores `…-09`) |
| `escape` | `bool` | `False` | Se `True`, escapa caracteres especiais HTML no resultado |
| `encode` | `bool` | `False` | Se `True`, codifica o resultado para URL (similar ao `encodeURIComponent` do JavaScript) |
| `on_fail` | `Callable` | retorna `''` | Callback quando o tamanho da entrada sanitizada ≠ 11; o retorno é usado como resultado |

### Opções do gerador

Em `generate(options=None, …)`, todas as opções são opcionais:

| Opção | Tipo | Padrão | Descrição |
|--------|------|---------|-------------|
| `format` | `bool` | `False` | Se `True`, retorna o CPF gerado no formato padrão (`000.000.000-00`) |
| `prefix` | `str` | `''` | String inicial parcial (0–9 dígitos). Caracteres não numéricos são removidos; os faltantes são gerados e os dígitos verificadores calculados. Prefixos com mais de 9 dígitos são truncados silenciosamente. |

Regras do prefixo: a base (9 primeiros dígitos) não pode ser só zeros; 9 dígitos repetidos (ex.: `999999999`) não são permitidos.

### `cpf_utils` (instância padrão)

O `cpf_utils` em nível de módulo é uma instância pré-construída de `CpfUtils`. Use-o para chamadas rápidas:

- **`format(cpf_input, options=None, …)`**: Formata uma string CPF ou sequência de strings. Delega ao formatador interno. A entrada deve ter 11 dígitos (após sanitização); caso contrário, `on_fail` é usado.
- **`generate(options=None, …)`**: Gera um CPF válido. Delega ao gerador interno.
- **`is_valid(cpf_input)`**: Retorna `True` se o CPF for válido. Delega ao validador interno. Sem opções por chamada — o validador de CPF não possui nenhuma.

### `CpfUtils` (classe)

Para formatador, gerador ou validador padrão personalizados, crie sua própria instância:

```python
from cpf_utils import CpfUtils

utils = CpfUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True, 'prefix': '123'},
)

utils.format('47844241055')        # '478.###.###-##'
utils.generate()                   # ex.: '005.265.352-88'
utils.is_valid('123.456.789-09')   # True

# Acessar ou substituir instâncias internas
utils.formatter  # CpfFormatter
utils.generator  # CpfGenerator
utils.validator  # CpfValidator
```

- **`__init__(*, formatter=None, generator=None, validator=None)`**: Cada palavra-chave pode ser um mapeamento de opções, uma instância de `CpfFormatterOptions` / `CpfGeneratorOptions` (armazenada por referência — mutá-la depois afeta chamadas subsequentes sem sobrescrita por chamada), uma instância de componente ou omitida para os padrões. Passar `None` para um componente cria uma nova instância com opções padrão.
- **`format(cpf_input, options=None, …)`**: Igual à instância padrão; opções por chamada sobrescrevem os padrões do formatador apenas nessa chamada.
- **`generate(options=None, …)`**: Igual à instância padrão; opções por chamada sobrescrevem os padrões do gerador.
- **`is_valid(cpf_input)`**: Igual à instância padrão. Sem opções por chamada.
- **`formatter`**, **`generator`**, **`validator`**: Propriedades com getters e setters para o formatador, gerador e validador internos. Os setters aceitam as mesmas formas do construtor. Para alterar uma única opção sem substituir a instância, mute as opções do componente (ex.: `utils.formatter.options.hidden = True`).

Padrões da instância e sobrescritas por chamada:

```python
utils = CpfUtils(
    formatter={'hidden': True, 'hidden_key': '#'},
    generator={'format': True},
)

cpf = '12345678909'

utils.format(cpf)                 # mascarado (padrões do formatador da instância)
utils.format(cpf, hidden=False)   # só nesta chamada: sem máscara
utils.generate(format=False)      # só nesta chamada: saída compacta
```

As opções também podem ser passadas como mapeamento em cada método:

```python
utils.format(cpf, {'dot_key': '|'})
utils.generate({'prefix': '123456', 'format': True})
```

### Usando os helpers e classes subjacentes

Você pode usar o formatador, gerador e validador reexportados diretamente:

```python
from cpf_utils import (
    cpf_fmt,
    CpfFormatter,
    cpf_gen,
    CpfGenerator,
    cpf_val,
    CpfValidator,
)

cpf_fmt('47844241055', dash_key='_')   # '478.442.410_55'
cpf_gen(prefix='123456')               # ex.: '12345678901'
cpf_val('123.456.789-09')              # True

formatter = CpfFormatter({'hidden': True})
formatter.format('47844241055')        # '478.***.***-**'
```

Consulte [`cpf-fmt`](./../cpf-fmt/README.pt.md), [`cpf-gen`](./../cpf-gen/README.pt.md) e [`cpf-val`](./../cpf-val/README.pt.md) para detalhes completos de opções e erros.

## API

### Exportações

- **`cpf_utils`**: Instância pré-construída de `CpfUtils` com `format`, `generate` e `is_valid`.
- **`CpfUtils`**: Classe para criar uma instância com configurações padrão opcionais de formatador, gerador e validador.
- **Formatador**: `cpf_fmt`, `CpfFormatter`, `CpfFormatterOptions` e exceções do formatador (veja [cpf-fmt](./../cpf-fmt/README.pt.md)).
- **Gerador**: `cpf_gen`, `CpfGenerator`, `CpfGeneratorOptions` e exceções do gerador (veja [cpf-gen](./../cpf-gen/README.pt.md)).
- **Validador**: `cpf_val`, `CpfValidator` e exceções do validador (veja [cpf-val](./../cpf-val/README.pt.md)).

### Erros e exceções

`CpfUtils` não define seus próprios tipos de exceção; propaga erros dos pacotes incluídos:

- **Formatação**: `CpfFormatterInputTypeError`, `CpfFormatterOptionsTypeError`, `CpfFormatterOptionsHiddenRangeInvalidException`, `CpfFormatterOptionsForbiddenKeyCharacterException` e classes relacionadas.
- **Geração**: `CpfGeneratorOptionsTypeError`, `CpfGeneratorOptionPrefixInvalidException` e classes relacionadas.
- **Validação**: `CpfValidatorInputTypeError` e classes relacionadas.

Tipos de opção inválidos são subclasses de **`TypeError`**; valores de opção inválidos são subclasses de **`Exception`**. Falha de validação retorna `False`; falha de comprimento na formatação é tratada por **`on_fail`** (padrão retorna string vazia).

```python
from cpf_utils import CpfUtils, cpf_fmt
from cpf_fmt import CpfFormatterInputTypeError
from cpf_val import CpfValidatorInputTypeError

try:
    CpfUtils().format(12345)
except CpfFormatterInputTypeError as e:
    print(e)

try:
    CpfUtils().is_valid(12345678909)
except CpfValidatorInputTypeError as e:
    print(e)

# on_fail personalizado para comprimento inválido
def custom_fail(value, exception=None):
    return f'CPF inválido: {value}'

cpf_fmt('123', on_fail=custom_fail)  # 'CPF inválido: 123'
cpf_fmt('123')                       # '' (on_fail padrão)
```

### Pacotes incluídos

| Pacote | Principais recursos | README |
|---------|----------------|--------|
| [`cpf-fmt`](https://pypi.org/project/cpf-fmt) | `CpfFormatter`, `CpfFormatterOptions`, `cpf_fmt()` | [docs](./../cpf-fmt/README.pt.md) |
| [`cpf-gen`](https://pypi.org/project/cpf-gen) | `CpfGenerator`, `CpfGeneratorOptions`, `cpf_gen()` | [docs](./../cpf-gen/README.pt.md) |
| [`cpf-val`](https://pypi.org/project/cpf-val) | `CpfValidator`, `cpf_val()` | [docs](./../cpf-val/README.pt.md) |

Todos os pacotes acima são instalados como dependências de **`cpf-utils`**. Para tabelas de opções exaustivas, listas de exceções e comportamento em casos extremos, consulte o README de cada pacote.

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
