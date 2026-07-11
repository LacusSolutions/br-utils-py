# AGENTS.md

This file is the **primary entry point** for AI agents working in the Python subrepo. Read this file first. It provides baseline rules for every task and links to the specialized harnesses in [`context/`](context/) for task-specific instructions.

**Reference standard:** all packages follow a single, current generation — there is no legacy/migration split. `packages/cnpj-*` and `packages/cpf-*` are symmetric modern implementations (options classes with property setters, full exception hierarchies, `pytest-describe` specs). Use `packages/cnpj-gen` and `packages/cnpj-utils` as canonical references for new or updated packages.

## Instruction precedence

When instructions conflict, **the more specific scope wins**:

1. **`packages/<pkg>/context/`** — package-level harness (if present)
2. **`packages/<pkg>/AGENTS.md`** — package-level agent rules (if present)
3. **Repository root** — [`context/`](context/) harnesses, then this file

Apply every layer relevant to your task. Where a package-level `AGENTS.md` or `context/` entry contradicts or overrides root-level guidance, follow the package-level instruction.

---

## Root-level guidelines

### Runtime and package manager

The project uses **Python** (`>=3.10,<4.0`, CI tests 3.10 through 3.14) and **pip**. Each package has its own `pyproject.toml` — there is no hoisted monorepo install. Install dev tooling and all packages editable-from-source with the root helper:

```bash
python require                 # dev tools + all packages (editable)
python require cnpj-gen        # dev tools + one package's dependency closure
python require --dev-only      # dev tools only
```

Do not assume a global install covers package dependencies. Prefer pip over any other Python package manager, and work inside a virtualenv (`.venv`).

### Dependencies

See [`context/dependencies.md`](context/dependencies.md) for the full policy (approval, PyPI versioning, internal dep direction, dependency closure inspection).

### Project structure

The repository is a monorepo with 12 independent packages under `packages/*`. Source is shipped as installed wheels/sdists built by setuptools; source lives under `src/<import_namespace>/`.

```
packages/
  utils/           # Shared helpers (PyPI: lacus.utils, import: lacus.utils)
  cpf-dv/          # CPF check digits
  cpf-fmt/         # CPF formatter
  cpf-gen/         # CPF generator
  cpf-val/         # CPF validator
  cpf-utils/       # CPF domain aggregator
  cnpj-dv/         # CNPJ check digits
  cnpj-fmt/        # CNPJ formatter
  cnpj-gen/        # CNPJ generator
  cnpj-val/        # CNPJ validator
  cnpj-utils/      # CNPJ domain aggregator
  br-utilities/    # Top-level CPF + CNPJ aggregator (PyPI: br-utilities, import: br_utils)
```

Two package folders do **not** match their import name: `utils` → `lacus.utils`, `br-utilities` → `br_utils`. All others match (`cnpj-gen` → `cnpj_gen`).

### Configurations

Shared tooling lives at the Python subrepo root:

- `run` — monorepo dev CLI (`python run <command> [args...]`)
- `require` — editable install helper (`python require [pkg]`)
- `.ruff.toml` — shared Ruff lint + format config (line length 100)
- `setup.cfg` — shared Black config (line length 100)
- `.pre-commit-config.yaml` — git hooks (pre-commit, commit-msg, pre-push)
- `requirements-dev.txt` — shared dev tooling versions
- `scripts/` — dev CLI implementation (`build.py`, `lint.py`, `test.py`, `discover.py`, etc.)

Prefer changing these only when necessary and in line with existing patterns. Do not add per-package Ruff or Black config files.

### Package strategy

Packages are split by domain (`utils`, `cpf-*`, `cnpj-*`, `br-utilities`). Follow the existing dependency direction:

```
utils → {cpf,cnpj}-dv → {cpf,cnpj}-{fmt,gen,val} → {cpf,cnpj}-utils → br-utilities
```

Upstream packages must not import downstream ones.

### Lint and format

Linting and formatting run **Ruff** (check + format) then **Black**, in that order, on each file. Run from the subrepo root:

```bash
python run lint               # lint + format all packages
python run lint cnpj-gen      # a single package
python run lint path/to/file  # a package, path, or single file
```

From inside a package directory (`packages/<pkg>/`): `python run lint`.

See [`context/lint-config.md`](context/lint-config.md) for the full setup and the rule against per-package config files.

### Commit and standards

**pre-commit** git hooks and **conventional-pre-commit** enforce conventional commits on every commit. Use the package folder name as the scope when changes are isolated to one package: `<type>(<pkg-name>): <message>` (e.g. `fix(cnpj-val): correct check digit`). Use `br-utils` (not `br-utilities`) as the scope for the `br-utilities` package. Valid scopes: `br-utils`, `cnpj-fmt`, `cnpj-dv`, `cnpj-gen`, `cnpj-val`, `cnpj-utils`, `cpf-fmt`, `cpf-dv`, `cpf-gen`, `cpf-val`, `cpf-utils`, `utils`, `internal`.

Install hooks with `python run hooks install`.

### CI

See [`context/ci-release.md`](context/ci-release.md) for the full pipeline (matrix Python versions, reusable lint and test workflows, what agents must not run, local validation commands).

---

## Package-specific guidelines

### Python version and typing

- Require `requires-python = ">=3.10,<4.0"` in every package `pyproject.toml`.
- Use **type hints** for all parameters and return types.
- Use `from __future__ import annotations` in modules that benefit from forward references, and `typing.TYPE_CHECKING` for type-only imports.

### Lint / format (DRY)

See [`context/lint-config.md`](context/lint-config.md) for the shared config, run flow, and the rule against adding per-package lint config files.

### Source layout

- Source must live under `src/<import_namespace>/`.
- Public API is exported from the package `__init__.py` via `__all__`.
- Specs live under `tests/` (not under `src/`).

### Docstrings

See [`context/docstrings.md`](context/docstrings.md) for conventions (PEP 257, class/method docs, `Raises:`, attribute docstrings on constants, cross-references, tone).

### Commit scope

If a commit touches only one package directory (`packages/<pkg-name>/`), use the package folder name as the conventional commit scope (see [Commit and standards](#commit-and-standards)).

### Changelog

See [`context/changelogs.md`](context/changelogs.md) for the full workflow (when to add an entry, SemVer bump decision, format, section headings, conciseness rules). Agents **do** edit `packages/<pkg>/CHANGELOG.md` directly — changelogs are managed manually.

### API and docs

Use [`context/public-api.md`](context/public-api.md) as the coordination checklist for any public API change (new class, function signature, option, exception, or export). It links to the specialized harnesses for source, docstrings, tests, README, and changelog. All README rules are in [`context/readme-docs.md`](context/readme-docs.md).

### CHANGELOG.md

Edit `packages/<pkg>/CHANGELOG.md` following the rules in [`context/changelogs.md`](context/changelogs.md). Do **not** run `python run release` or `python run publish` — those prepare release notes and publish to PyPI, and are the developer's responsibility.

---

## Agent harnesses

Task-specific instructions live in [`context/`](context/). The harness catalog — IDs, files, and triggers — is [`context/README.md`](context/README.md). Read and follow the matching harness file **in full** before starting the task.

A package may define its own `packages/<pkg>/context/` or `packages/<pkg>/AGENTS.md`; those override conflicting root harness or README rules for that package (see [Instruction precedence](#instruction-precedence) above).

### Skill ↔ harness mapping

Cursor agents may load these workspace skills as a shortcut; each skill is a thin pointer to the canonical harness:

| Cursor skill | Harness file | When triggered |
|--------------|-------------|----------------|
| `readme-py` | [`context/readme-docs.md`](context/readme-docs.md) | Writing or reviewing `README.md` / `README.pt.md` |
| `unit-tests-py` | [`context/unit-tests.md`](context/unit-tests.md) | Writing, reviewing, or running tests |
| `changelogs-py` | [`context/changelogs.md`](context/changelogs.md) | Editing `CHANGELOG.md`; choosing a SemVer bump |
| `package-arch-py` | [`context/package-arch.md`](context/package-arch.md) | Adding or changing `src/` code |
| `public-api-py` | [`context/public-api.md`](context/public-api.md) | Any public API change |
| `new-package-py` | [`context/new-package.md`](context/new-package.md) | Scaffolding a new package |
| `lint-config-py` | [`context/lint-config.md`](context/lint-config.md) | Editing lint/format config |
| `docstrings-py` | [`context/docstrings.md`](context/docstrings.md) | Adding or reviewing docstrings |
| `packaging-py` | [`context/packaging.md`](context/packaging.md) | Editing `pyproject.toml`, build, or publish |
| `domain-parity-py` | [`context/domain-parity.md`](context/domain-parity.md) | CPF ↔ CNPJ parity check |
| `aggregator-package-py` | [`context/aggregator-package.md`](context/aggregator-package.md) | Working on `cpf-utils`, `cnpj-utils`, or `br-utilities` |
| `ci-release-py` | [`context/ci-release.md`](context/ci-release.md) | Editing CI workflows; local validation |
| `dependencies-py` | [`context/dependencies.md`](context/dependencies.md) | Adding or changing dependencies |

---

## Key paths

| Purpose | Path |
|---------|------|
| Agent harnesses (catalog) | `context/` |
| Shared Ruff config | `.ruff.toml` |
| Shared Black config | `setup.cfg` |
| Dev CLI entry | `run` (`python run lint`, `python run test`, etc.) |
| Editable install helper | `require` (`python require [pkg]`) |
| Dev CLI implementation | `scripts/` (`build.py`, `lint.py`, `test.py`, `discover.py`, …) |
| Internal dependency resolver | `scripts/discover.py` |
| Dev tooling versions | `requirements-dev.txt` |
| Git hook config | `.pre-commit-config.yaml` |
| CI / release workflows | `.github/workflows/` |
| Package config | `packages/*/pyproject.toml` |
| Package changelogs | `packages/*/CHANGELOG.md` |
