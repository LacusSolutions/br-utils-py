# cpf-gen

## 1.0.1

- 344fbe7: Migrate internal dependency from `cpf-cd` to `cpf-dv` to calculate check digits.
- Dropped dependencies
  - `cpf-cd`
- Added dependencies
  - `cpf-dv` (1.0.0)

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to generate valid CPF (Brazilian personal ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CpfGenerator`) and function-based (`cpf_gen`) usage
- **Valid check digits**: automatically calculates and appends correct check digits using the official CPF algorithm
- **Prefix support**: generate CPFs starting with a custom prefix (up to 9 digits)
- **Optional formatting**: output with standard CPF format (dots and dash) or unformatted
- **Repeated digits validation**: prevents generating invalid CPFs with all repeated digits (e.g., `111.111.111-11`)
- **Zero external dependencies**: only relies on `cpf-cd` from the same package family
- **Lightweight**: only requires `cpf-cd`, from the same initiative, for check digit calculation

For detailed usage and API reference, see the [README](./README.md).
