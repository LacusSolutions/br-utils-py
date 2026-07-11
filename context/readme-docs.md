---
id: readme-docs
title: Package README authoring
scope: packages/*/README.md, packages/*/README.pt.md
triggers:
  - creating or updating a package README
  - rewriting or reviewing README.md or README.pt.md
  - editing the root Python repository README
  - PyPI or package documentation
  - translating README to Portuguese (README.pt.md)
---

# readme-docs

Author and maintain `README.md` files under `packages/<pkg>/` following the established br-utils-py conventions. All paths are relative to the repo root.

## Repository constraints

### Root README

The root `README.md` at `python/README.md` documents the `br-utilities` project. Edit it directly.

### Portuguese parity

English `README.md` is the source of truth for structure and content. Any change to a package's `README.md` must be reflected in that package's `README.pt.md` (faithful translation). Most packages have both; `utils` (foundation) has English only.

### Changelog links

Package `CHANGELOG.md` files are edited manually. READMEs link to the changelog in the footer only (`See [CHANGELOG](./CHANGELOG.md) …`). Do not recap changelog content in the README.

### Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Before writing

1. Check for `packages/<pkg>/AGENTS.md` and `packages/<pkg>/context/`; apply overrides when present.
2. Read `packages/<pkg>/pyproject.toml` for the PyPI name and description.
3. Read `src/` (and `__all__`) to list public classes, functions, constants, and types accurately.
4. Skim specs in `tests/` for realistic examples.
5. Identify the **package archetype** (below) — section depth depends on it.
6. Check the counterpart package in the other domain (e.g. `cnpj-gen` when documenting `cpf-gen`).

## Package archetypes

| Archetype | Examples | Distinct traits |
|-----------|----------|-----------------|
| **Foundation** | `utils` | H1 title; per-function API docs; no formatter/generator/validator usage sections |
| **Single-purpose** | `cnpj-fmt`, `cnpj-val`, `cnpj-gen`, `cnpj-dv`, `cpf-*` | Cover image; Usage + API; options tables; class + helper function pattern |
| **Aggregator** | `cnpj-utils`, `cpf-utils` | Cover image; wraps leaf packages; Usage inlines sub-options; links to leaf READMEs |
| **Top aggregator** | `br-utilities` | Cover image; wraps both domains; links to domain aggregator READMEs |

Special sections (only when relevant): `## Calculation algorithm` for DV packages; an announcement blockquote for major features (e.g. alphanumeric CNPJ).

## Section order (mandatory)

```
[Cover image OR H1 title]
[Badges row]
[Optional blockquote callouts]
[One-paragraph description]
## Python Support
## Features
## Installation
## Quick Start
## Usage              ← omit for foundation packages
## API
[## Calculation algorithm]  ← DV packages only
## Contribution & Support
## License
## Changelog
---
Made with ❤️ by Lacus Solutions
```

## Header block

### Cover image (single-purpose & aggregator)

```markdown
![<pkg> for Python](https://br-utils.vercel.app/img/cover_<pkg>.jpg)
```

Use the package folder slug (e.g. `cnpj-gen`). Foundation packages use an H1 instead.

### Badges (six, in this order)

Replace `<pypi-name>` with the PyPI distribution name (`cnpj-gen`, `lacus.utils`, `br-utilities`):

```markdown
[![PyPI Version](https://img.shields.io/pypi/v/<pypi-name>)](https://pypi.org/project/<pypi-name>)
[![PyPI Downloads](https://img.shields.io/pypi/dm/<pypi-name>)](https://pypi.org/project/<pypi-name>)
[![Python Version](https://img.shields.io/pypi/pyversions/<pypi-name>)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)
```

### Optional callouts (before description)

Feature announcement (when applicable) and the Portuguese doc link:

```markdown
> 🚀 **Full support for the [new alphanumeric CNPJ format](...).**

> 🌎 [Acessar documentação em português](./README.pt.md)
```

### Description (one paragraph)

> A Python **{noun}** to **{primary action}** **{subject}** ({expanded name}).

## Python Support

Use the Python version badge table (not plain text). Copy from `packages/cnpj-gen/README.md` and adjust versions to match `requires-python`:

```markdown
## Python Support

| ![Python 3.10](...) | ![Python 3.11](...) | ![Python 3.12](...) | ![Python 3.13](...) | ![Python 3.14](...) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |
```

## Features

```markdown
- ✅ **{Short label}**: {One sentence benefit or capability}
```

Standard features to include when applicable: **Flexible input**, **Alphanumeric CNPJ** (CNPJ only), **Formatting/Masking**, **Reusable instance**, **Type hints** (Python 3.10+), **Minimal dependencies** (name internal deps), **Error handling** (type errors vs exceptions).

## Installation

```markdown
## Installation

```bash
$ pip install <pypi-name>
```
```

## Quick Start

Show the import then 2–5 lines of the most common usage with output in comments:

```python
from cnpj_gen import cnpj_gen

cnpj_gen()                    # e.g. 'AB123CDE000155'
cnpj_gen(format=True)         # e.g. 'AB.123.CDE/0001-55'
cnpj_gen(type='numeric')      # e.g. '65453043000178'
```

Mention that options can also be passed as a mapping (`cnpj_gen({'format': True})`).

## Usage

Structure with `###` subsections. Include an **options table** (Option / Type / Default / Description) whose defaults match the source `DEFAULT_*` constants, then a subsection per public entry point:

- **`{pkg_short}` (helper function)** — one-shot wrapper; document positional `options` and keyword-only overrides.
- **`{ClassName}` (class)** — constructor + methods + `options` property; show reusable-instance and per-call-override examples.
- **`{ClassName}Options` (class)** — `__init__` merge semantics, property setters, `set()`, `all` snapshot, `DEFAULT_*` constants.

## API

List all public symbols under `### Exports` (mirror `__all__`), then an `### Errors & Exceptions` subsection documenting the two-tier model:

- **`*TypeError`** subclasses — option/input has the wrong type (raised).
- **`*Exception`** subclasses — invalid value / business-rule failure (raised); formatters/validators route length failures through `on_fail`.

Include a `try/except` example when ≥2 exception types exist, catching specific classes and the base type.

## Footer sections (copy verbatim, adjust paths)

```markdown
## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](./CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
```

## Writing style

| Rule | Detail |
|------|--------|
| Language | English in `README.md`; mirror structure faithfully in `README.pt.md` |
| Voice | Direct, technical, third-person; present tense |
| Formatting | Backticks for identifiers, options, types; **bold** for symbol names in prose |
| Code | Python fenced blocks; `# 'result'` comments with realistic domain values |
| Links | Relative repo links (`./README.pt.md`, `./CHANGELOG.md`); pypi.org for package links |
| Accuracy | Document actual exports and defaults from source — never invent APIs |

## Workflow checklist

```
- [ ] Archetype identified (foundation / single-purpose / aggregator)
- [ ] PyPI name matches pyproject.toml [project].name
- [ ] All public exports documented under ## API (mirror __all__)
- [ ] Python Support versions match requires-python
- [ ] Installation shows pip install <pypi-name>
- [ ] Quick Start shows the import + realistic output
- [ ] Options table defaults match source DEFAULT_* constants
- [ ] Error behavior (raise vs on_fail) is explicit
- [ ] Leaf README links present (aggregators)
- [ ] CHANGELOG footer links to ./CHANGELOG.md
- [ ] README.pt.md present (except utils) and updated when README.md changes
- [ ] Footer boilerplate unchanged
```

## Reference packages

| Archetype | Canonical example |
|-----------|-------------------|
| Formatter | `packages/cnpj-fmt/README.md` |
| Validator | `packages/cnpj-val/README.md` |
| Generator | `packages/cnpj-gen/README.md` |
| Check digits | `packages/cnpj-dv/README.md` |
| Domain aggregator | `packages/cnpj-utils/README.md` |
| Top-level aggregator | `packages/br-utilities/README.md` |
