![cpf-fmt para Python](https://br-utils.vercel.app/img/cover_cpf-fmt.jpg)

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-fmt/README.md)

Utilitário em Python para formatar CPF (Cadastro de Pessoa Física) como valor numérico de 11 dígitos, com opções de máscara, escape HTML e codificação para URL.

## Recursos

- ✅ **Entrada flexível**: Aceita `str` ou sequência de `str`; elementos da sequência são concatenados na ordem
- ✅ **Agnóstico ao formato**: Remove caracteres não numéricos antes de formatar
- ✅ **Delimitadores personalizáveis**: `dot_key` e `dash_key` podem ser vazios ou strings de um ou vários caracteres
- ✅ **Mascaramento**: Ocultação opcional de um intervalo de índices com string de substituição configurável (`hidden`, `hidden_key`, `hidden_start`, `hidden_end`)
- ✅ **Saída HTML e URL**: `escape` opcional (entidades HTML) e `encode` opcional (codificação tipo componente de URI, semelhante ao `encodeURIComponent` do JavaScript)
- ✅ **Erro de tamanho sem exceção**: Comprimento inválido após sanitização é tratado via `on_fail` (o padrão retorna string vazia)
- ✅ **Dependências mínimas**: Apenas [`lacus.utils`](https://pypi.org/project/lacus.utils/)
- ✅ **Tratamento de erros**: Erros de tipo para uso incorreto da API; validação de opções com exceções específicas

## Instalação

```bash
$ pip install cpf-fmt
```

## Importação

```python
from cpf_fmt import CpfFormatter, CpfFormatterOptions, cpf_fmt
```

## Início rápido

```python
from cpf_fmt import CpfFormatter

formatter = CpfFormatter()

formatter.format('03603568195')      # '036.035.681-95'
formatter.format('123.456.789-10')   # '123.456.789-10'
formatter.format('12345678910')      # '123.456.789-10'
```

## Utilização

Os pontos principais são a classe `CpfFormatter`, a classe de opções `CpfFormatterOptions` e o helper `cpf_fmt()`.

### `CpfFormatter`

- **`__init__`**: Opções padrão de formatação. O primeiro parâmetro pode ser `None`, um mapeamento de chaves de opção ou uma instância de `CpfFormatterOptions` (essa instância é armazenada; alterações posteriores afetam chamadas a `format()` que não passarem opções por chamada). Também é possível passar campos como argumentos nomeados (`hidden`, `hidden_key`, `dot_key`, …). Exemplo: `CpfFormatter(hidden=True, dash_key='_')`.
- **`options`**: Propriedade que retorna o `CpfFormatterOptions` da instância (o mesmo objeto usado internamente).
- **`format(cpf_input, options=None, …)`**: Formata um valor CPF.

  A entrada é normalizada removendo caracteres não numéricos. Se o comprimento após sanitização não for exatamente **11**, o callback **`on_fail`** é chamado com a entrada original e uma `CpfFormatterInputLengthException`; o valor de retorno do callback é o resultado (nada é lançado por comprimento).

  Se a entrada não for `str` nem sequência de `str`, é lançada **`CpfFormatterInputTypeError`**.

  As opções por chamada são mescladas sobre os padrões da instância apenas naquela chamada (os padrões da instância não mudam). É possível passar uma instância de `CpfFormatterOptions` ou um mapeamento como segundo argumento, além de argumentos nomeados; quando ambos forem fornecidos, o argumento `options` prevalece.

### `CpfFormatterOptions`

Armazena todas as configurações do formatador. Construa com um mapeamento opcional ou instância de `CpfFormatterOptions`, objetos extras de sobrescrita (mesclados em ordem) e/ou argumentos nomeados. Expõe propriedades: `hidden`, `hidden_key`, `hidden_start`, `hidden_end`, `dot_key`, `dash_key`, `escape`, `encode`, `on_fail`.

- **`all`**: Retorna uma cópia superficial de todas as opções atuais.
- **`copy()`**: Retorna uma cópia superficial desta instância de opções.
- **`set(options)`**: Atualiza vários campos de uma vez; retorna `self`. Aceita um mapeamento ou outra instância de `CpfFormatterOptions`.
- **`set_hidden_range(hidden_start, hidden_end)`**: Valida índices em **`[0, 10]`** (inclusivos); se `hidden_start > hidden_end`, os valores são trocados. Argumentos `None` usam os padrões (`DEFAULT_HIDDEN_START` / `DEFAULT_HIDDEN_END`).

**`hidden_start` / `hidden_end`**: Os índices referem-se à **string CPF normalizada de 11 dígitos** (antes de inserir pontuação). O intervalo inclusivo é substituído internamente por placeholders e depois por `hidden_key` (permite chaves com vários caracteres ou string vazia).

**Opções de chave** (`hidden_key`, `dot_key`, `dash_key`): Devem ser strings e não podem conter caracteres em `CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS` (reservados para a lógica interna).

### Helper funcional

`cpf_fmt()` instancia um novo `CpfFormatter` com os mesmos parâmetros do construtor e chama `format(cpf_input)` uma vez. Use argumentos nomeados, um mapeamento ou uma instância de `CpfFormatterOptions` para as opções:

```python
from cpf_fmt import cpf_fmt

cpf = '03603568195'

cpf_fmt(cpf)                # '036.035.681-95'
cpf_fmt(cpf, hidden=True)   # mascarado com padrões
cpf_fmt(                    # '036035681_95'
    cpf,
    dot_key='',
    dash_key='_',
)
cpf_fmt(cpf, {              # forma com mapeamento
    'hidden': True,
    'hidden_key': '#',
})
```

### Exemplos orientados a objeto

```python
from cpf_fmt import CpfFormatter

formatter = CpfFormatter()
cpf = '12345678910'

formatter.format(cpf)   # '123.456.789-10'
formatter.format(       # '123.###.###-##'
    cpf,
    hidden=True,
    hidden_key='#',
    hidden_start=3,
    hidden_end=10,
)
```

Padrões na instância; sobrescritas por chamada:

```python
formatter = CpfFormatter(hidden=True)

formatter.format(cpf)                 # usa mascaramento da instância
formatter.format(cpf, hidden=False)   # só nesta chamada: sem máscara
formatter.format(cpf)                 # volta aos padrões da instância
```

Entrada em sequência:

```python
formatter.format([                   # '123.456.789-10'
    '123',
    '456',
    '789',
    '10',
])
```

### Formatos de entrada

**String:** Dígitos brutos ou CPF já formatado (ex.: `123.456.789-10`, `123 456 789 10`). Caracteres não numéricos são removidos; zeros à esquerda são preservados.

**Sequência de strings:** Cada elemento deve ser `str`; os valores são concatenados (ex.: por dígito, segmentos agrupados ou misturados com pontuação — tudo que não for dígito é removido na normalização). Elementos que não sejam string não são permitidos.

### Opções de formatação

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `hidden` | `bool \| None` | `False` | Se `True`, substitui o intervalo inclusivo `[hidden_start, hidden_end]` na string normalizada de 11 dígitos antes de aplicar pontuação |
| `hidden_key` | `str \| None` | `'*'` | Substituição de cada posição oculta (pode ter vários caracteres ou ser vazia); não pode usar caracteres proibidos nas chaves |
| `hidden_start` | `int \| None` | `3` | Índice inicial `0`–`10` (inclusivo) |
| `hidden_end` | `int \| None` | `10` | Índice final `0`–`10` (inclusivo); se `hidden_start > hidden_end`, são trocados |
| `dot_key` | `str \| None` | `'.'` | Separador após o 3º e o 6º dígitos |
| `dash_key` | `str \| None` | `'-'` | Separador após o 9º dígito |
| `escape` | `bool \| None` | `False` | Se `True`, escapa HTML na string final |
| `encode` | `bool \| None` | `False` | Se `True`, codifica a string final para URL (semelhante a `encodeURIComponent`) |
| `on_fail` | `Callable \| None` | veja abaixo | `(value, exception) -> str` — usado quando o comprimento sanitizado ≠ 11 |

O **`on_fail`** padrão retorna string vazia. A exceção passada em falhas de comprimento é **`CpfFormatterInputLengthException`** (`actual_input`, `evaluated_input`, `expected_length`).

Exemplo com todas as opções:

```python
from cpf_fmt import cpf_fmt

cpf = '12345678910'

cpf_fmt(
    cpf,
    hidden=True,
    hidden_key='#',
    hidden_start=3,
    hidden_end=9,
    dot_key=' ',
    dash_key='_-_',
    escape=True,
    encode=True,
    on_fail=lambda value, exception: str(value),
)
```

### Erros e exceções

- **Tipo de entrada incorreto** (não `str` nem sequência de `str`): **`CpfFormatterInputTypeError`** — estende **`CpfFormatterTypeError`** (estende `TypeError` nativo).
- **Tipos ou valores de opção inválidos ao construir ou mesclar opções**: **`CpfFormatterOptionsTypeError`**, **`CpfFormatterOptionsHiddenRangeInvalidException`**, **`CpfFormatterOptionsForbiddenKeyCharacterException`** — estendem **`CpfFormatterTypeError`** ou **`CpfFormatterException`** conforme o caso.

Diferença de comprimento **não** lança exceção em `format()`; trate dentro de **`on_fail`**.

```python
from cpf_fmt import (
    CpfFormatter,
    CpfFormatterInputLengthException,
    CpfFormatterInputTypeError,
)

try:
    CpfFormatter().format(12345)
except CpfFormatterInputTypeError as e:
    e  # tratar erro de tipo

CpfFormatter().format(
    'short',
    on_fail=lambda value, exception: 'invalid',
)  # 'invalid'
```

## API

### Exportações

Todos os símbolos públicos estão disponíveis no pacote `cpf_fmt`:

- **`cpf_fmt`**: `(cpf_input: CpfInput, options=None, **kwargs) -> str` — helper de conveniência.
- **`CpfFormatter`**: Classe para formatar CPF com opções padrão opcionais; aceita `CpfInput` em `format()`.
- **`CpfFormatterOptions`**: Classe que armazena opções; suporta mesclagem via construtor, `set()` e argumentos nomeados.
- **`CPF_LENGTH`**: `11` (constante).
- **`CpfInput`**: Alias de tipo — `str | Sequence[str]`.
- **Exceções**: `CpfFormatterTypeError`, `CpfFormatterInputTypeError`, `CpfFormatterOptionsTypeError`, `CpfFormatterException`, `CpfFormatterInputLengthException`, `CpfFormatterOptionsHiddenRangeInvalidException`, `CpfFormatterOptionsForbiddenKeyCharacterException`.

### Outros recursos disponíveis

- **`CpfFormatterOptions.CPF_LENGTH`**: `11`.
- **`CpfFormatterOptions.DISALLOWED_KEY_CHARACTERS`**: Caracteres proibidos em `hidden_key`, `dot_key`, `dash_key`.
- **`CpfFormatterOptions.DEFAULT_*`**: Valores padrão de cada opção.

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela ao repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Consulte o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-fmt/CHANGELOG.md) para histórico de versões e alterações.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
