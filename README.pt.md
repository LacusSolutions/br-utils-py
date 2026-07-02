![cpf-dv para Python](https://br-utils.vercel.app/img/cover_cpf-dv.jpg)

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-dv/README.md)

Utilitário em Python para calcular os dígitos verificadores de CPF (Cadastro de Pessoa Física).

## Recursos

- ✅ **Entrada flexível**: Aceita `str` ou `list[str]`
- ✅ **Agnóstico ao formato**: Remove caracteres não numéricos da entrada em string
- ✅ **Junção em lista**: Strings com vários caracteres em listas são concatenadas e interpretadas como uma única sequência
- ✅ **Validação de entrada**: Rejeita CPFs inelegíveis (9 dígitos idênticos na base — padrão de repetição)
- ✅ **Avaliação lazy**: Dígitos verificadores são calculados apenas quando acessados (via propriedades)
- ✅ **Cache**: Valores calculados são armazenados em cache para acessos subsequentes
- ✅ **Anotações de tipo**: Construído com type hints para Python 3.10+
- ✅ **Dependências mínimas**: Apenas [`lacus.utils`](https://pypi.org/project/lacus.utils)
- ✅ **Tratamento de erros**: Tipos específicos para tipo, tamanho e CPF inválido (semântica `TypeError` vs `Exception`)

## Instalação

```bash
$ pip install cpf-dv
```

## Início rápido

```python
from cpf_dv import CpfCheckDigits
```

Uso básico:

```python
check_digits = CpfCheckDigits("054496519")

check_digits.first   # '1'
check_digits.second  # '0'
check_digits.both    # '10'
check_digits.cpf     # '05449651910'
```

## Utilização

O principal recurso deste pacote é a classe `CpfCheckDigits`. Por meio da instância, você acessa as informações dos dígitos verificadores do CPF:

- **`__init__`**: `CpfCheckDigits(str | list[str])` — 9–11 dígitos após a sanitização (formatação removida em strings). Apenas os **primeiros 9** dígitos entram como base; com 10 ou 11 dígitos (ex.: CPF completo com DV anteriores), os dígitos 10 e 11 são **ignorados** e os dígitos verificadores são recalculados.
- **`first`**: Primeiro dígito verificador (10º dígito do CPF completo). Lazy, em cache.
- **`second`**: Segundo dígito verificador (11º dígito do CPF completo). Lazy, em cache.
- **`both`**: Ambos os dígitos verificadores concatenados em uma string.
- **`cpf`**: O CPF completo como string de 11 dígitos (9 da base + 2 dígitos verificadores).

### Formatos de entrada

A classe `CpfCheckDigits` aceita múltiplos formatos de entrada:

**String:** dígitos crus ou CPF formatado (ex.: `054.496.519-10`, `123.456.789`). Caracteres não numéricos são removidos. Zeros à esquerda são preservados.

**Lista de strings:** cada elemento deve ser string; os valores são concatenados e interpretados como uma única string (ex.: `["0","5","4",…]`, `["054","496","519"]`, `["054496519"]`). Elementos que não são strings não são permitidos.

```python
# String — crua, formatada ou com DV existentes (apenas os 9 primeiros dígitos são usados)
CpfCheckDigits("054496519")
CpfCheckDigits("054.496.519-10")
CpfCheckDigits("05449651910")

# Lista de strings — elementos de um ou vários caracteres
CpfCheckDigits(["0", "5", "4", "4", "9", "6", "5", "1", "9"])
CpfCheckDigits(["054", "496", "519"])
CpfCheckDigits(["054496519"])
```

### Erros e exceções

Este pacote usa a distinção **TypeError vs Exception**: *erros de tipo* indicam uso incorreto da API (ex.: tipo errado); *exceções* indicam dados inválidos ou inelegíveis (ex.: tamanho ou regras de negócio). Você pode capturar classes específicas ou as classes base.

- **CpfCheckDigitsTypeError** — classe base para erros de tipo; estende o `TypeError` do Python
- **CpfCheckDigitsInputTypeError** — entrada não é `str` nem `list[str]` (ou a lista contém elemento que não é string)
- **CpfCheckDigitsException** — classe base para exceções de dados/fluxo; estende `Exception`
- **CpfCheckDigitsInputLengthException** — tamanho após sanitização não é 9–11
- **CpfCheckDigitsInputInvalidException** — os 9 primeiros dígitos são idênticos (padrão de repetição)

```python
from cpf_dv import (
    CpfCheckDigits,
    CpfCheckDigitsException,
    CpfCheckDigitsInputInvalidException,
    CpfCheckDigitsInputLengthException,
    CpfCheckDigitsInputTypeError,
)

# Tipo de entrada (ex.: inteiro não permitido)
try:
    CpfCheckDigits(12345678901)
except CpfCheckDigitsInputTypeError as e:
    print(e)  # CPF input must be of type string or string[]. Got integer number.

# Tamanho (deve ser 9–11 dígitos após sanitização)
try:
    CpfCheckDigits("12345678")
except CpfCheckDigitsInputLengthException as e:
    print(e)  # CPF input "12345678" does not contain 9 to 11 digits. Got 8.

# Inválido (ex.: dígitos repetidos)
try:
    CpfCheckDigits(["999", "999", "999"])
except CpfCheckDigitsInputInvalidException as e:
    print(e)  # CPF input ["999","999","999"] is invalid. Repeated digits are not considered valid.

# Qualquer exceção de dados do pacote
try:
    CpfCheckDigits(["999", "999", "999"])
except CpfCheckDigitsException as e:
    print(e)
```

### Outros recursos disponíveis

Importe de `cpf_dv`:

- **`CPF_MIN_LENGTH`**: `9`
- **`CPF_MAX_LENGTH`**: `11`
- **`CpfInput`**: alias de tipo (`str | list[str]`)
- **Exceções**: veja acima

## Algoritmo de cálculo

O pacote calcula os dígitos verificadores do CPF com o algoritmo oficial brasileiro de módulo 11:

1. **Primeiro dígito verificador (10ª posição):** aplicar aos **primeiros 9** dígitos da base; pesos **10, 9, 8, 7, 6, 5, 4, 3, 2** (da esquerda para a direita); seja `resto = 11 - (soma(dígito × peso) % 11)`. O dígito é `0` se `resto > 9`, senão `resto`.
2. **Segundo dígito verificador (11ª posição):** aplicar aos 9 primeiros dígitos da base **mais** o primeiro dígito verificador; pesos **11, 10, 9, 8, 7, 6, 5, 4, 3, 2** (da esquerda para a direita); mesma fórmula para `resto`.

## Dependências

- **Python**: >= 3.10, < 4.0
- **[lacus.utils](https://pypi.org/project/lacus.utils)**: >= 1.0.0, < 2.0.0

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se o projeto for útil para você, considere:

- ⭐ Dar uma estrela no repositório
- 🤝 Contribuir com código
- 💡 [Sugerir novas funcionalidades](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Veja o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-dv/CHANGELOG.md) para alterações e histórico de versões.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
