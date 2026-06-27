![cnpj-dv para Python](https://br-utils.vercel.app/img/cover_cnpj-dv.jpg)

> 🚀 **Suporte total ao [novo formato alfanumérico de CNPJ](https://github.com/user-attachments/files/23937961/calculodvcnpjalfanaumerico.pdf).**

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-dv/README.md)

Utilitário em Python para calcular os dígitos verificadores de CNPJ (Cadastro Nacional da Pessoa Jurídica).

## Recursos

- ✅ **CNPJ alfanumérico**: Suporte completo ao novo formato alfanumérico de CNPJ (a partir de 2026)
- ✅ **Entrada flexível**: Aceita `str` ou `list[str]`
- ✅ **Agnóstico ao formato**: Remove caracteres não alfanuméricos da entrada em string e converte letras para maiúsculas
- ✅ **Junção em lista**: Strings com vários caracteres em listas são concatenadas e interpretadas como uma única sequência
- ✅ **Validação de entrada**: Rejeita CNPJs inelegíveis (base toda zero `00000000`, filial `0000`, ou 12 dígitos numéricos repetidos)
- ✅ **Avaliação lazy**: Dígitos verificadores são calculados apenas quando acessados (via propriedades)
- ✅ **Cache**: Valores calculados são armazenados em cache para acessos subsequentes
- ✅ **Anotações de tipo**: Construído com type hints para Python 3.10+
- ✅ **Dependências mínimas**: Apenas [`lacus.utils`](https://pypi.org/project/lacus.utils)
- ✅ **Tratamento de erros**: Tipos específicos para tipo, tamanho e CNPJ inválido (semântica `TypeError` vs `Exception`)

## Instalação

```bash
$ pip install cnpj-dv
```

## Início rápido

```python
from cnpj_dv import CnpjCheckDigits
```

Uso básico:

```python
check_digits = CnpjCheckDigits("914157320007")

check_digits.first   # '9'
check_digits.second  # '3'
check_digits.both    # '93'
check_digits.cnpj    # '91415732000793'
```

Com CNPJ alfanumérico (novo formato):

```python
check_digits = CnpjCheckDigits("MGKGMJ9X0001")

check_digits.first   # '6'
check_digits.second  # '8'
check_digits.both    # '68'
check_digits.cnpj    # 'MGKGMJ9X000168'
```

## Utilização

O principal recurso deste pacote é a classe `CnpjCheckDigits`. Por meio da instância, você acessa as informações dos dígitos verificadores do CNPJ:

- **`__init__`**: `CnpjCheckDigits(str | list[str])` — 12–14 caracteres alfanuméricos após a sanitização (formatação removida em strings; letras em maiúsculas). Apenas os **primeiros 12** caracteres entram como base; com 13 ou 14 caracteres (ex.: CNPJ completo com DV anteriores), os caracteres 13 e 14 são **ignorados** e os dígitos são recalculados.
- **`first`**: Primeiro dígito verificador (13º caractere do CNPJ completo). Lazy, em cache.
- **`second`**: Segundo dígito verificador (14º caractere do CNPJ completo). Lazy, em cache.
- **`both`**: Ambos os dígitos verificadores concatenados em uma string.
- **`cnpj`**: O CNPJ completo como string de 14 caracteres (12 da base + 2 dígitos verificadores).

### Formatos de entrada

A classe `CnpjCheckDigits` aceita múltiplos formatos de entrada:

**String:** dígitos e/ou letras crus, ou CNPJ formatado (ex.: `91.415.732/0007-93`, `MG.KGM.J9X/0001-68`). Caracteres não alfanuméricos são removidos; letras minúsculas viram maiúsculas.

**Lista de strings:** cada elemento deve ser string; os valores são concatenados e interpretados como uma única string (ex.: `["9","1","4",…]`, `["9141","5732","0007"]`, `["MG","KGM","J9X","0001"]`). Elementos que não são strings não são permitidos.

```python
# String — crua, formatada ou com DV existentes (apenas os 12 primeiros caracteres são usados)
CnpjCheckDigits("914157320007")
CnpjCheckDigits("91.415.732/0007")
CnpjCheckDigits("91415732000793")

# Lista de strings — elementos de um ou vários caracteres
CnpjCheckDigits(["9", "1", "4", "1", "5", "7", "3", "2", "0", "0", "0", "7"])
CnpjCheckDigits(["9141", "5732", "0007"])
CnpjCheckDigits(["MG", "KGM", "J9X", "0001"])
```

### Erros e exceções

Este pacote usa a distinção **TypeError vs Exception**: *erros de tipo* indicam uso incorreto da API (ex.: tipo errado); *exceções* indicam dados inválidos ou inelegíveis (ex.: tamanho ou regras de negócio). Você pode capturar classes específicas ou as classes base.

- **CnpjCheckDigitsTypeError** — classe base para erros de tipo; estende o `TypeError` do Python
- **CnpjCheckDigitsInputTypeError** — entrada não é `str` nem `list[str]` (ou a lista contém elemento que não é string)
- **CnpjCheckDigitsException** — classe base para exceções de dados/fluxo; estende `Exception`
- **CnpjCheckDigitsInputLengthException** — tamanho após sanitização não é 12–14
- **CnpjCheckDigitsInputInvalidException** — base `00000000`, filial `0000`, ou 12 dígitos numéricos idênticos (padrão de repetição)

```python
from cnpj_dv import (
    CnpjCheckDigits,
    CnpjCheckDigitsException,
    CnpjCheckDigitsInputInvalidException,
    CnpjCheckDigitsInputLengthException,
    CnpjCheckDigitsInputTypeError,
)

# Tipo de entrada (ex.: inteiro não permitido)
try:
    CnpjCheckDigits(12345678000100)
except CnpjCheckDigitsInputTypeError as e:
    print(e)  # CNPJ input must be of type string or string[]. Got integer number.

# Tamanho (deve ser 12–14 caracteres alfanuméricos após sanitização)
try:
    CnpjCheckDigits("12345678901")
except CnpjCheckDigitsInputLengthException as e:
    print(e)  # CNPJ input "12345678901" does not contain 12 to 14 digits. Got 11.

# Inválido (ex.: base ou filial zeradas, ou dígitos numéricos repetidos)
try:
    CnpjCheckDigits("000000000001")
except CnpjCheckDigitsInputInvalidException as e:
    print(e)  # CNPJ input "000000000001" is invalid. Base ID "00000000" is not eligible.

# Qualquer exceção de dados do pacote
try:
    CnpjCheckDigits("000000000001")
except CnpjCheckDigitsException as e:
    print(e)
```

### Outros recursos disponíveis

Importe de `cnpj_dv`:

- **`CNPJ_MIN_LENGTH`**: `12`
- **`CNPJ_MAX_LENGTH`**: `14`
- **Exceções**: veja acima

## Algoritmo de cálculo

O pacote calcula os dígitos verificadores com as regras oficiais brasileiras de módulo 11 estendidas a caracteres alfanuméricos:

1. **Valor do caractere:** cada caractere contribui com `ord(caractere) − 48` (assim `0`–`9` permanecem 0–9; letras usam o deslocamento ASCII em relação a `0`).
2. **Pesos:** da **direita para a esquerda**, multiplicar pelos pesos que ciclam **2, 3, 4, 5, 6, 7, 8, 9** e voltam a 2.
3. **Primeiro dígito verificador (13ª posição):** aplicar os itens 1–2 aos **primeiros 12** caracteres da base; seja `r = soma % 11`. O dígito é `0` se `r < 2`, senão `11 − r`.
4. **Segundo dígito verificador (14ª posição):** aplicar os itens 1–2 aos 12 primeiros caracteres **mais** o primeiro dígito verificador; mesma fórmula para `r`.

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

Veja o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-dv/CHANGELOG.md) para alterações e histórico de versões.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
