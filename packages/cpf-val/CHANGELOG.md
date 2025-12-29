# cpf-val

## 1.0.1

- 8d48436: Migrate internal dependency from `cpf-cd` to `cpf-dv` to calculate check digits.
- Dropped dependencies
  - `cpf-cd`
- Added dependencies
  - `cpf-dv` (1.0.0)

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to validate CPF (Brazilian personal ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CpfValidator`) and function-based (`cpf_val`) usage
- **Format agnostic**: accepts CPF with or without formatting (dots, dashes)
- **Strict validation**: validates both check digits according to the official Brazilian CPF algorithm
- **Type safety**: built with Python 3.10+ type hints
- **Lightweight**: only requires `cpf-cd`, from the same initiative, for check digit calculation
- **Graceful error handling**: returns `False` for invalid inputs without raising exceptions

For detailed usage and API reference, see the [README](./README.md).
