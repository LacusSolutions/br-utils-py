---
id: domain-parity
title: CPF ↔ CNPJ domain parity
scope: packages/cpf-*/src/, packages/cnpj-*/src/
triggers:
  - porting a CPF feature to CNPJ (or vice versa)
  - reviewing a PR that touches cpf-* and cnpj-* symmetrically
  - checking whether a CNPJ counterpart exists for a CPF change
  - deciding whether a divergence is intentional
---

# domain-parity

Use this harness when a change touches CPF packages and you need to determine whether the symmetric CNPJ package requires the same change, or vice versa. All paths are relative to the repo root.

## Repository constraints

- **Same generation.** Unlike the PHP subrepo, CPF and CNPJ packages in Python are at the **same generation** — both use options classes with property setters, full exception hierarchies, and `pytest-describe` specs. There is no migration asymmetry; parity is the default expectation.
- **Always check the counterpart.** When you change a `cpf-*` package, verify whether the `cnpj-*` counterpart needs the same change (and vice versa).
- Do **not** silently skip the counterpart — either apply the symmetric change or document why it doesn't apply.
- Intentional divergences are cataloged below; they are not bugs.

## Package pairing

| CPF package | CNPJ counterpart |
|-------------|------------------|
| `cpf-dv` | `cnpj-dv` |
| `cpf-fmt` | `cnpj-fmt` |
| `cpf-gen` | `cnpj-gen` |
| `cpf-val` | `cnpj-val` |
| `cpf-utils` | `cnpj-utils` |

`utils` and `br-utilities` are shared/aggregate — no counterpart check needed.

## Intentional divergences (not bugs)

| Area | CPF | CNPJ |
|------|-----|------|
| **Input character set** | Digits only (0–9) | Alphanumeric (digits + uppercase A–Z) |
| **Identifier length** | 11 characters | 14 characters |
| **`*_LENGTH` constant** | `CPF_LENGTH = 11` | `CNPJ_LENGTH = 14` |
| **Formatter mask** | `000.000.000-00` | `00.000.000/0000-00` |
| **Formatter `slash_key` option** | Not present | Present (separates base ID and branch suffix) |
| **Generator options** | `format`, `prefix` | `format`, `prefix`, `type` (`"numeric"` \| `"alphabetic"` \| `"alphanumeric"`) |
| **Validator options** | None — `cpf-val` has no options module | `cnpj-val` has a `CnpjValidatorOptions` class with `type` (`"numeric"` \| `"alphanumeric"`) and `case_sensitive` |
| **Prefix validation** | Zeroed base ID check (9 chars) | Zeroed base ID (8) + branch ID (4) + repeated-digit checks |
| **DV algorithm** | Numeric modulo-11 per digit | Weighted sum using character-code values |
| **`CnpjType` literal** | Not applicable | Exported (`alphanumeric` / `alphabetic` / `numeric`) |

Do not "fix" these toward one domain's behavior without explicit product intent.

## Parity workflow

When changing a `cpf-*` or `cnpj-*` package:

1. Identify the counterpart from the pairing table.
2. Check if the same issue or feature applies to the counterpart (same archetype, same `src/` structure per [`context/package-arch.md`](package-arch.md)).
3. If parity applies → open or note a corresponding change for the counterpart.
4. If divergence is intentional (table above) → no action needed; note it in the CHANGELOG body if user-visible.
5. If unsure → ask the developer.

## Symmetry checklist

When a feature or fix is applied to one domain, verify the following in the counterpart:

- [ ] Same change in the main class if logic is symmetric
- [ ] Same change in the options class if a new option is added (respecting divergences)
- [ ] Same new exception class in `exceptions.py` if a new failure case is introduced
- [ ] Same `Raises:` section in docstrings per [`context/docstrings.md`](docstrings.md)
- [ ] Same spec cases per [`context/unit-tests.md`](unit-tests.md)
- [ ] Both packages in the CHANGELOG entries if user-facing per [`context/changelogs.md`](changelogs.md)
- [ ] Both READMEs updated per [`context/readme-docs.md`](readme-docs.md) if options or defaults change

## Key files for comparison

| Concern | CPF | CNPJ |
|---------|-----|------|
| DV algorithm | `packages/cpf-dv/src/cpf_dv/cpf_check_digits.py` | `packages/cnpj-dv/src/cnpj_dv/cnpj_check_digits.py` |
| Formatter | `packages/cpf-fmt/src/cpf_fmt/cpf_formatter.py` | `packages/cnpj-fmt/src/cnpj_fmt/cnpj_formatter.py` |
| Formatter options | `packages/cpf-fmt/src/cpf_fmt/cpf_formatter_options.py` | `packages/cnpj-fmt/src/cnpj_fmt/cnpj_formatter_options.py` |
| Generator options | `packages/cpf-gen/src/cpf_gen/cpf_generator_options.py` | `packages/cnpj-gen/src/cnpj_gen/cnpj_generator_options.py` |
| Validator | `packages/cpf-val/src/cpf_val/cpf_validator.py` (no options module) | `packages/cnpj-val/src/cnpj_val/cnpj_validator.py` + `cnpj_validator_options.py` |
| Aggregator class | `packages/cpf-utils/src/cpf_utils/cpf_utils.py` | `packages/cnpj-utils/src/cnpj_utils/cnpj_utils.py` |

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).
