---
id: lint-config
title: Lint and format configuration
scope: .ruff.toml, setup.cfg, run, scripts/lint.py, .pre-commit-config.yaml
triggers:
  - changing the shared Ruff configuration
  - changing the shared Black configuration
  - modifying the lint script or run command
  - understanding how lint runs per-package vs root
  - editing pre-commit hooks
---

# lint-config

Manage the lint and format setup for br-utils-py packages. All paths are relative to the repo root.

## Repository constraints

- **Do not duplicate lint config in packages.** Shared config lives in root `.ruff.toml` and `setup.cfg`; the lint logic lives in `scripts/lint.py`. Packages invoke it via `python run lint`.
- **Do not add per-package Ruff or Black config files.** Every package shares the root config.
- Lint and format config changes are **dev-only** — they do not require a CHANGELOG entry.

## Shared lint/format setup

Linting and formatting run **three tools in order** on each file (`scripts/lint.py`):

1. **Ruff check** — `ruff check --fix` (auto-fixes lint violations)
2. **Ruff format** — `ruff format`
3. **Black** — `black`

### Ruff (`.ruff.toml`)

- `line-length = 100`, `target-version = "py310"`.
- Selected rule families: `E`, `W`, `F`, `I` (isort), `B` (bugbear), `C4`, `UP` (pyupgrade), `ARG`, `SIM`, `SLF`, `TCH` (type-checking), `PIE`, `PT` (pytest-style), `RET`, `RUF`.
- Ignored: `E501` (handled by the formatter), `B008`, `C901`.
- Per-file ignores: `__init__.py` → `F401` (re-exports are intentional); `tests/**/*.py` → `ARG`.
- Formatter: double quotes, space indent, magic trailing comma respected.

### Black (`setup.cfg`)

- `line-length = 100`; runs after Ruff format as a final pass.

### What gets linted

`scripts/lint.py` scans for `*.py` files plus the executable `run` and `require` scripts (which are Python without a `.py` suffix). Running from the root lints the whole tree; passing a package or path scopes it down.

## Running lint

From the **python/** repository root:

```bash
python run lint               # lint + format everything under python/
python run lint cnpj-gen      # a single package (folder name)
python run lint packages/cnpj-gen/src/cnpj_gen/cnpj_generator.py  # a single file
python run lint path/to/dir   # any directory
```

From a package directory (`packages/<pkg>/`): `python run lint` delegates to the root CLI with the package name.

## Per-package `run` script

Each package has a thin `run` script that forwards `lint`, `test`, `build`, `clean`, and `publish` to the monorepo root `run` with the package name pre-filled. Do not add package-specific lint logic there — it only routes to the shared commands.

## Git hooks (pre-commit)

Config: `.pre-commit-config.yaml`. Install with `python run hooks install`. Stages:

| Hook | Stage | What it does |
|------|-------|--------------|
| pre-commit-hooks (YAML/TOML/JSON checks, trailing whitespace, EOF, private-key, etc.) | pre-commit | File hygiene |
| `sync-license` | pre-commit | Propagates root `LICENSE` to all packages |
| `lint` (`python run lint`) | pre-commit | Lint + format staged source |
| `conventional-pre-commit` | commit-msg | Validates conventional commit message + scope |
| `test-all` (`python run test`) | pre-push | Runs the full test suite before pushing |

> The `check-docstring-first` hook is intentionally **not** enabled — it false-positives on PEP 257 attribute docstrings (`CONST = ...` followed by `"""..."""`), which this codebase uses (see [`context/docstrings.md`](docstrings.md#attribute-docstrings-on-constants-and-defaults)).

## When to edit the shared config

- **Edit `.ruff.toml` / `setup.cfg` / `scripts/lint.py`** only when the change applies to **all** packages (e.g. adding a Ruff rule family, changing line length).
- **Add a package-level override** only when a package genuinely cannot follow the root config — document the reason in the package's `AGENTS.md`.

## Checklist

- [ ] No per-package `.ruff.toml`, `ruff.toml`, or Black config added
- [ ] `python run lint <pkg>` passes from the root
- [ ] Config change applies uniformly to all packages
- [ ] No CHANGELOG entry added for lint/format config changes

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Path |
|---------|------|
| Ruff config | `.ruff.toml` |
| Black config | `setup.cfg` |
| Lint implementation | `scripts/lint.py` |
| CLI entry | `run` (`python run lint`) |
| Git hook config | `.pre-commit-config.yaml` |
| Per-package router | `packages/<pkg>/run` |
