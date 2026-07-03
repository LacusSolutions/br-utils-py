![cpf-val para Python](https://br-utils.vercel.app/img/cover_cpf-val.jpg)

> 🌎 [Access documentation in English](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-val/README.md)

Utilitário em Python para validar CPF (Cadastro de Pessoa Física).

## Recursos

- ✅ **CPF de 11 dígitos**: Valida o CPF brasileiro padrão de 11 dígitos pelo algoritmo oficial de módulo 11
- ✅ **Entrada flexível**: Aceita `str` ou sequência de `str`; elementos da sequência são concatenados na ordem
- ✅ **Agnóstico ao formato**: Remove todos os caracteres não numéricos antes de validar
- ✅ **Rejeição de dígitos repetidos**: CPFs com todos os dígitos iguais (ex.: `111.111.111-11`, `00000000000`) são rejeitados
- ✅ **Validação tipada de entrada**: Subclasse dedicada de `TypeError` para tipo de entrada inválido
- ✅ **Dependências mínimas**: [`cpf-dv`](https://pypi.org/project/cpf-dv/) para cálculo dos dígitos verificadores e [`lacus.utils`](https://pypi.org/project/lacus.utils/) para descrição de tipos nas mensagens de erro
- ✅ **API dupla**: Orientada a objetos (`CpfValidator`) e funcional (`cpf_val()`)

## Instalação

```bash
$ pip install cpf-val
```

## Importação

```python
from cpf_val import CpfValidator, cpf_val
```

## Início rápido

```python
from cpf_val import CpfValidator

validator = CpfValidator()

validator.is_valid('12345678909')       # True
validator.is_valid('123.456.789-09')    # True
validator.is_valid('12345678910')       # False (dígitos verificadores inválidos)
validator.is_valid('00000000000')       # False (dígitos repetidos)
```

Helper funcional:

```python
from cpf_val import cpf_val

cpf_val('12345678909')      # True
cpf_val('123.456.789-09')   # True
cpf_val('12345678910')      # False
```

## Utilização

Os pontos principais são a classe `CpfValidator` e o helper `cpf_val()`.

### `CpfValidator`

- **`__init__`**: Não recebe argumentos. A validação de CPF não possui opções de configuração.
- **`is_valid(cpf_input)`**: Valida um valor CPF.

  A entrada é normalizada para string (sequências de strings são concatenadas). Em seguida, todos os caracteres não numéricos são removidos. Se o comprimento após sanitização não for exatamente **11**, se a base for uma sequência de dígitos todos iguais ou se os dígitos verificadores não coincidirem (`CpfCheckDigits` de **`cpf-dv`**), o método retorna `False` — nenhuma exceção é lançada por falha de validação.

  Se a entrada não for `str` nem sequência de `str`, é lançada **`CpfValidatorInputTypeError`**.

```python
from cpf_val import CpfValidator

validator = CpfValidator()

validator.is_valid('123.456.789-09')             # True
validator.is_valid('12345678909')                # True
validator.is_valid(['123', '456', '789', '09'])  # True
validator.is_valid('12345678910')                # False (dígitos verificadores inválidos)
validator.is_valid('11111111111')                # False (dígitos repetidos)
```

### Helper funcional

`cpf_val()` instancia um novo `CpfValidator` e chama `is_valid(cpf_input)` uma vez. Recebe apenas o valor de entrada:

```python
from cpf_val import cpf_val

cpf_val('11144477735')      # True
cpf_val('111.444.777-35')   # True
cpf_val('11144477736')      # False
```

### Formatos de entrada

**String:** Apenas dígitos ou CPF já formatado (ex.: `123.456.789-09`, `499.784.420-90`, `011_258_960_00`). Caracteres não numéricos são removidos antes da validação; o resultado deve ter exatamente 11 dígitos.

**Sequência de strings:** Cada elemento deve ser `str`; os valores são concatenados (ex.: por dígito, segmentos agrupados ou misturados com pontuação). Elementos que não sejam string lançam **`CpfValidatorInputTypeError`**.

```python
from cpf_val import cpf_val

cpf_val(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '9'])  # True
cpf_val(['123.456', '789-09'])  # True
```

### Erros e exceções

Este pacote usa **TypeError** para tipos de entrada inválidos. Falhas de validação (comprimento incorreto, base inelegível como dígitos repetidos, dígitos verificadores inválidos) retornam `False` e não lançam exceção.

- **Tipo de entrada incorreto** (não `str` nem sequência de `str`): **`CpfValidatorInputTypeError`** — estende **`CpfValidatorTypeError`** (estende `TypeError` nativo).
- **`CpfValidatorException`** (_abstrata_): base para erros de regra de negócio (não relacionados a tipo); atualmente sem subclasse concreta neste pacote.

```python
from cpf_val import (
    CpfValidatorInputTypeError,
    CpfValidatorTypeError,
    cpf_val,
)

# Tipo de entrada (ex.: inteiro não permitido)
try:
    cpf_val(12345678909)
except CpfValidatorInputTypeError as e:
    print(e)  # CPF input must be of type string or string[]. Got integer number.

# Qualquer erro de tipo do pacote
try:
    cpf_val(None)
except CpfValidatorTypeError as e:
    pass  # tratar
```

## API

### Exportações

Todos os símbolos públicos estão disponíveis no pacote `cpf_val`:

- **`cpf_val`**: `(cpf_input: CpfInput) -> bool` — helper de conveniência.
- **`CpfValidator`**: Classe para validar CPF (sem opções); aceita `CpfInput` em `is_valid()`.
- **`CPF_LENGTH`**: `11` (constante).
- **`CpfInput`**: Alias de tipo — `str | Sequence[str]`.
- **Exceções**: `CpfValidatorTypeError`, `CpfValidatorInputTypeError`, `CpfValidatorException`.

## Contribuição e suporte

Contribuições são bem-vindas! Consulte as [Diretrizes de contribuição](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md). Se este projeto for útil para você, considere:

- ⭐ Dar uma estrela ao repositório
- 🤝 Contribuir com o código
- 💡 [Sugerir novos recursos](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reportar bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE).

## Changelog

Consulte o [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-val/CHANGELOG.md) para histórico de versões e alterações.

---

Feito com ❤️ por [Lacus Solutions](https://github.com/LacusSolutions)
