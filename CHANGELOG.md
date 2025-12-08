# cnpj-cd

## 1.0.1

### Patch Changes

- fb8af97: Create copy of digits list when calculating check digits to avoid mutating it unexpectedly.
- c7693cf: Fix documentation hero image source.

## 1.0.0

### 🚀 Stable Version Released!

Utility class to calculate check digits on CNPJ (Brazilian legal entity ID). Main features:

- **Multiple input formats**: accepts strings, lists of strings, or lists of integers
- **Format agnostic**: automatically strips non-numeric characters from input
- **Lazy evaluation**: check digits are calculated only when accessed
- **Zero dependencies**: no external packages required
- **Comprehensive error handling**: specific exceptions for different error scenarios

For detailed usage and API reference, see the [README](./README.md).
