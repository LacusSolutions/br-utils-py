![cnpj-fmt para Python](https://br-utils.vercel.app/img/cover_cnpj-fmt.jpg)

> 🚀 **Suporte total ao [novo formato alfanumérico de CNPJ](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-fmt/README.md)

Utilitário em Python para formatar CNPJ (Cadastro Nacional da Pessoa Jurídica) como valor alfanumérico de 14 caracteres, com opções de máscara, escape HTML e codificação para URL.

## Recursos

- ✅ **CNPJ alfanumérico**: Suporte a CNPJ de 14 caracteres alfanuméricos (dígitos e letras, ex.: `RK0CMT3W000100`)
- ✅ **Entrada flexível**: Aceita `str` ou sequência de `str`; elementos da sequência são concatenados na ordem
- ✅ **Agnóstico ao formato**: Remove caracteres não alfanuméricos e converte letras para maiúsculas antes de formatar
- ✅ **Delimitadores personalizáveis**: `dot_key`, `slash_key` e `dash_key` podem ser vazios ou strings de um ou vários caracteres
- ✅ **Mascaramento**: Ocultação opcional de um intervalo de índices com string de substituição configurável (`hidden`, `hidden_key`, `hidden_start`, `hidden_end`)
- ✅ **Saída HTML e URL**: `escape` opcional (entidades HTML) e `encode` opcional (codificação tipo componente de URI, semelhante ao `encodeURIComponent` do JavaScript)
- ✅ **Erro de tamanho sem exceção**: Comprimento inválido após sanitização é tratado via `on_fail` (o padrão retorna string vazia)
- ✅ **Dependências mínimas**: Apenas [`lacus.utils`](https://pypi.org/project/lacus.utils/)
- ✅ **Tratamento de erros**: Erros de tipo para uso incorreto da API; validação de opções com exceções específicas

## Instalação

```bash
$ pip install cnpj-fmt
```

## Importação

```python
from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions, cnpj_fmt
```

## Início rápido

```python
from cnpj_fmt import CnpjFormatter

formatter = CnpjFormatter()

formatter.format('03603568000195')   # '03.603.568/0001-95'
formatter.format('12ABC34500DE99')   # '12.ABC.345/00DE-99'
formatter.format('RK0CMT3W000100')   # 'RK.0CM.T3W/0001-00'
```

## Utilização

Os pontos principais são a classe `CnpjFormatter`, a classe de opções `CnpjFormatterOptions` e o helper `cnpj_fmt()`.

### `CnpjFormatter`

- **`__init__`**: Opções padrão de formatação. O primeiro parâmetro pode ser `None`, um mapeamento de chaves de opção ou uma instância de `CnpjFormatterOptions` (essa instância é armazenada; alterações posteriores afetam chamadas a `format()` que não passarem opções por chamada). Também é possível passar campos como argumentos nomeados (`hidden`, `hidden_key`, `dot_key`, …). Exemplo: `CnpjFormatter(hidden=True, slash_key='|')`.
- **`options`**: Propriedade que retorna o `CnpjFormatterOptions` da instância (o mesmo objeto usado internamente).
- **`format(cnpj_input, options=None, …)`**: Formata um valor CNPJ.

  A entrada é normalizada removendo caracteres não alfanuméricos e convertendo para maiúsculas. Se o comprimento após sanitização não for exatamente **14**, o callback **`on_fail`** é chamado com a entrada original e uma `CnpjFormatterInputLengthException`; o valor de retorno do callback é o resultado (nada é lançado por comprimento).

  Se a entrada não for `str` nem sequência de `str`, é lançada **`CnpjFormatterInputTypeError`**.

  As opções por chamada são mescladas sobre os padrões da instância apenas naquela chamada (os padrões da instância não mudam). É possível passar uma instância de `CnpjFormatterOptions` ou um mapeamento como segundo argumento, além de argumentos nomeados; quando ambos forem fornecidos, o argumento `options` prevalece.

### `CnpjFormatterOptions`

Armazena todas as configurações do formatador, com validação e suporte a mesclagem. Expõe propriedades: `hidden`, `hidden_key`, `hidden_start`, `hidden_end`, `dot_key`, `slash_key`, `dash_key`, `escape`, `encode`, `on_fail`.

- **`__init__(options=None, *extra_overrides, hidden=None, hidden_key=None, hidden_start=None, hidden_end=None, dot_key=None, slash_key=None, dash_key=None, escape=None, encode=None, on_fail=None)`**: Opções padrão opcionais (mapeamento simples, instância de `CnpjFormatterOptions` ou argumentos nomeados), além de objetos extras de sobrescrita mesclados em ordem (as últimas sobrescritas prevalecem).
- **`all`**: Retorna uma cópia superficial de todas as opções atuais.
- **`copy()`**: Retorna uma cópia superficial desta instância de opções.
- **`set(options)`**: Atualiza vários campos de uma vez; retorna `self`. Aceita um mapeamento ou outra instância de `CnpjFormatterOptions`.
- **`set_hidden_range(hidden_start, hidden_end)`**: Valida índices em **`[0, 13]`** (inclusivos); se `hidden_start > hidden_end`, os valores são trocados. Argumentos `None` usam os padrões (`DEFAULT_HIDDEN_START` / `DEFAULT_HIDDEN_END`).

**`hidden_start` / `hidden_end`**: Os índices referem-se à **string CNPJ normalizada de 14 caracteres** (antes de inserir pontuação). O intervalo inclusivo é substituído internamente por placeholders e depois por `hidden_key` (permite chaves com vários caracteres ou string vazia).

**Opções de chave** (`hidden_key`, `dot_key`, `slash_key`, `dash_key`): Devem ser strings e não podem conter caracteres em `CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS` (reservados para a lógica interna).

### Helper funcional

`cnpj_fmt()` instancia um novo `CnpjFormatter` com os mesmos parâmetros do construtor e chama `format(cnpj_input)` uma vez. Use argumentos nomeados, um mapeamento ou uma instância de `CnpjFormatterOptions` para as opções:

```python
from cnpj_fmt import cnpj_fmt

cnpj = '03603568000195'

cnpj_fmt(cnpj)                # '03.603.568/0001-95'
cnpj_fmt(cnpj, hidden=True)   # mascarado com padrões
cnpj_fmt(                     # '03603568|0001_95'
    cnpj,
    dot_key='',
    slash_key='|',
    dash_key='_',
)
cnpj_fmt(cnpj, {              # forma com mapeamento
    'hidden': True,
    'hidden_key': '#',
})

### Exemplos orientados a objeto

```python
from cnpj_fmt import CnpjFormatter

formatter = CnpjFormatter()
cnpj = '03603568000195'

formatter.format(cnpj)   # '03.603.568/0001-95'
formatter.format(        # '03.603.###/####-##'
    cnpj,
    hidden=True,
    hidden_key='#',
    hidden_start=5,
    hidden_end=13,
)
```

Padrões na instância; sobrescritas por chamada:

```python
formatter = CnpjFormatter(hidden=True)

formatter.format(cnpj)                 # usa mascaramento da instância
formatter.format(cnpj, hidden=False)   # só nesta chamada: sem máscara
formatter.format(cnpj)                 # volta aos padrões da instância
```

Entrada alfanumérica e sequência:

```python
formatter.format('RK0CMT3W000100')   # 'RK.0CM.T3W/0001-00'
formatter.format([                   # 'RK.0CM.T3W/0001-00'
    'RK',
    '0CM',
    'T3W',
    '0001',
    '00',
])
```

### Formatos de entrada

**String:** Dígitos e/ou letras brutos, ou CNPJ já formatado (ex.: `12.345.678/0009-10`, `12.ABC.345/00DE-99`). Caracteres não alfanuméricos são removidos; letras minúsculas viram maiúsculas.

**Sequência de strings:** Cada elemento deve ser `str`; os valores são concatenados (ex.: por dígito, segmentos agrupados ou misturados com pontuação — tudo é removido na normalização). Elementos que não sejam string não são permitidos.

### Opções de formatação

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `hidden` | `bool \| None` | `False` | Se `True`, substitui o intervalo inclusivo `[hidden_start, hidden_end]` na string normalizada de 14 caracteres antes de aplicar pontuação |
| `hidden_key` | `str \| None` | `'*'` | Substituição de cada posição oculta (pode ter vários caracteres ou ser vazia); não pode usar caracteres proibidos nas chaves |
| `hidden_start` | `int \| None` | `5` | Índice inicial `0`–`13` (inclusivo) |
| `hidden_end` | `int \| None` | `13` | Índice final `0`–`13` (inclusivo); se `hidden_start > hidden_end`, são trocados |
| `dot_key` | `str \| None` | `'.'` | Separador entre grupos `XX` / `XXX` / `XXX` |
| `slash_key` | `str \| None` | `'/'` | Separador antes do bloco da filial |
| `dash_key` | `str \| None` | `'-'` | Separador antes dos dois últimos caracteres |
| `escape` | `bool \| None` | `False` | Se `True`, escapa HTML na string final |
| `encode` | `bool \| None` | `False` | Se `True`, codifica a string final para URL (semelhante a `encodeURIComponent`) |
| `on_fail` | `Callable \| None` | veja abaixo | `(value, exception) -> str` — usado quando o comprimento sanitizado ≠ 14 |

O **`on_fail`** padrão retorna string vazia. A exceção passada em falhas de comprimento é **`CnpjFormatterInputLengthException`** (`actual_input`, `evaluated_input`, `expected_length`).

Exemplo com todas as opções:

```python
from cnpj_fmt import cnpj_fmt

cnpj = '03603568000195'

cnpj_fmt(
    cnpj,
    hidden=True,
    hidden_key='#',
    hidden_start=5,
    hidden_end=11,
    dot_key=' ',
    slash_key='|',
    dash_key='_-_',
    escape=True,
    encode=True,
    on_fail=lambda value, exception: str(value),
)
```

### Erros e exceções

- **Tipo de entrada incorreto** (não `str` nem sequência de `str`): **`CnpjFormatterInputTypeError`** — estende **`CnpjFormatterTypeError`** (estende `TypeError` nativo).
- **Tipos ou valores de opção inválidos ao construir ou mesclar opções**: **`CnpjFormatterOptionsTypeError`**, **`CnpjFormatterOptionsHiddenRangeInvalidException`**, **`CnpjFormatterOptionsForbiddenKeyCharacterException`** — estendem **`CnpjFormatterTypeError`** ou **`CnpjFormatterException`** conforme o caso.

Diferença de comprimento **não** lança exceção em `format()`; trate dentro de **`on_fail`**.

```python
from cnpj_fmt import (
    CnpjFormatter,
    CnpjFormatterInputLengthException,
    CnpjFormatterInputTypeError,
)

try:
    CnpjFormatter().format(12345)
except CnpjFormatterInputTypeError as e:
    e  # tratar erro de tipo

CnpjFormatter().format(
    'short',
    on_fail=lambda value, exception: 'invalid',
)  # 'invalid'
```

## API

### Exportações

Todos os símbolos públicos estão disponíveis no pacote `cnpj_fmt`:

- **`cnpj_fmt`**: `(cnpj_input: CnpjInput, options=None, **kwargs) -> str` — helper de conveniência.
- **`CnpjFormatter`**: Classe para formatar CNPJ com opções padrão opcionais; aceita `CnpjInput` em `format()`.
- **`CnpjFormatterOptions`**: Classe que armazena opções; suporta mesclagem via construtor, `set()` e argumentos nomeados.
- **`CNPJ_LENGTH`**: `14` (constante).
- **`CnpjInput`**: Alias de tipo — `str | Sequence[str]`.
- **Exceções**: `CnpjFormatterTypeError`, `CnpjFormatterInputTypeError`, `CnpjFormatterOptionsTypeError`, `CnpjFormatterException`, `CnpjFormatterInputLengthException`, `CnpjFormatterOptionsHiddenRangeInvalidException`, `CnpjFormatterOptionsForbiddenKeyCharacterException`.

### Outros recursos disponíveis

- **`CnpjFormatterOptions.CNPJ_LENGTH`**: `14`.
- **`CnpjFormatterOptions.DISALLOWED_KEY_CHARACTERS`**: Caracteres proibidos em `hidden_key`, `dot_key`, `slash_key`, `dash_key`.
- **`CnpjFormatterOptions.DEFAULT_*`**: Valores padrão de cada opção.

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela ao repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Consulte o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-fmt/CHANGELOG.md) para histórico de versões e alterações.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
