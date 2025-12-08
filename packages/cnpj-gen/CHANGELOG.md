# cnpj-gen

## 1.0.1

### Patch Changes

- db1f01b: Fix documentation hero image source.
- Updated dependencies
  - `cnpj-cd`: 1.0.0 → 1.0.1

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to generate valid CNPJ (Brazilian legal entity ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CnpjGenerator`) and function-based (`cnpj_gen`) usage
- **Valid check digits**: automatically calculates and appends correct check digits using the official CNPJ algorithm
- **Prefix support**: generate CNPJs starting with a custom prefix (business ID or partial branch ID)
- **Optional formatting**: output with standard CNPJ format (dots, slash, dash) or unformatted
- **Branch ID validation**: ensures branch ID is never "0000" (invalid per CNPJ rules)
- **Zero external dependencies**: only relies on `cnpj-cd` from the same package family

For detailed usage and API reference, see the [README](./README.md).
