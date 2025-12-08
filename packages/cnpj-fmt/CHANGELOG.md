# cnpj-fmt

## 1.0.0

### 🚀 Stable Version Released!

Utility function/class to format CNPJ (Brazilian legal entity ID) strings. Main features:

- **Multiple interfaces**: supports both class-based (`CnpjFormatter`) and function-based (`cnpj_fmt`) usage
- **Format agnostic**: automatically strips non-numeric characters from input
- **Customizable output**: configurable delimiters (dot, slash, dash) for flexible formatting
- **Privacy masking**: hide sensitive digits with configurable range and mask character
- **HTML escaping**: built-in support for safe HTML output
- **Graceful error handling**: customizable fallback via `on_fail` callback for invalid inputs
- **Zero dependencies**: no external packages required

For detailed usage and API reference, see the [README](./README.md).
