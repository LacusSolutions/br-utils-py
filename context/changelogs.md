---
id: changelogs
title: Changelog entries
scope: packages/*/CHANGELOG.md
triggers:
  - creating or editing a CHANGELOG.md entry
  - deciding whether a change needs a changelog entry
  - choosing a SemVer bump level
  - reviewing changelog entries before release
---

# changelogs

Maintain `packages/<pkg>/CHANGELOG.md` files following the rules below. All `git tag` and SemVer lookups must run from inside the Python subrepo (`cd python/`) — the workspace root is not a Git repo.

> A Cursor workspace hook (`.cursor/rules/python/changelog-keeper.mdc` and `changelog-package.mdc`) automates this at the end of turns that touch `python/`. This harness is the tool-agnostic version of those rules; keep the two consistent.

## Repository constraints

- `packages/<pkg>/CHANGELOG.md` files are the **only** files agents create or edit in this workflow.
- Do **not** run `python run release`, `python run publish`, create GitHub Releases, or push git tags. Only the developer does that.
- Do **not** edit released sections — once tagged, history is immutable.
- Do **not** edit the top-level `# <dist-name>` heading.

## Naming: heading and tag prefix

The `CHANGELOG.md` heading and the git tag prefix both use the **PyPI distribution name** from `pyproject.toml` `[project].name`. This equals the package folder name for every package except two:

| Folder | Heading / tag prefix |
|--------|----------------------|
| `cnpj-gen` (and most) | `cnpj-gen` |
| `utils` | `lacus.utils` |
| `br-utilities` | `br-utilities` |

## Step 1 — Determine the latest released version

```bash
cd python && git tag -l '<dist-name>@*' | grep -vE '(rc|beta|alpha|dev)' | sort -V | tail -n 3
```

The last line is the latest released stable version. Strip the `<dist-name>@` prefix to get the bare SemVer (e.g. `2.0.3`). Treat tags containing `rc`, `beta`, `alpha`, or `dev` as pre-releases and ignore them unless they are the only tags.

If no stable tag exists, the package has never been released — the first proposed version is `1.0.0`.

## Step 2 — Inspect the top of `CHANGELOG.md`

The file always starts with `# <dist-name>` followed by version blocks. Look at the **top-most** `## x.y.z` heading:

- If it **equals** the latest released tag → the section is released. **Prepend a new section** with a freshly proposed version above it.
- If it is **greater** than the latest released tag → the section is the current in-progress version. **Append or refine** that section instead of creating a new one. If a new change is more severe than the proposed bump (e.g. a breaking change arrives when the section was a patch), **promote** the heading (`## 1.0.1` → `## 2.0.0`) and reorganize the bullets.

## Step 3 — Skip dev-only changes

The changelog is for **end users** of the package on PyPI. If every in-scope change is purely internal and invisible to consumers, do **not** add an entry.

### Dev-only (skip):

- Tests, fixtures, `conftest.py` — anything under `tests/`.
- Coverage tooling, `.coverage*`, `.pytest_cache/`, `.ruff_cache/`, `htmlcov/`.
- Linter / formatter configs — `.ruff.toml`, `setup.cfg`, `.pre-commit-config.yaml`.
- CI workflows under `.github/` and helper scripts under `scripts/` or the top-level `run` / `require`.
- `pyproject.toml` edits touching only `[tool.*]` blocks, dev-extras, or `[dependency-groups]` dev groups.
- Dev-only requirement files — `requirements-dev.txt`.
- Build artifacts under `dist/`, `build/`, `*.egg-info/`.
- Repo hygiene — `.gitignore`, `.gitattributes`, `.editorconfig`.

### User-facing (entry needed):

If even one in-scope change is user-facing, add an entry documenting **only** the user-facing parts:

- Anything under `src/`.
- `pyproject.toml` `[project]` runtime `dependencies`, `name`, `version`, or `requires-python`.
- A public `README.md` correction.

## Step 4 — Choose the next version using SemVer

Based on all user-facing changes since the latest released tag (cumulative — not just this turn):

| Level | When to use |
|-------|-------------|
| **major** | Removal or rename of a public class/function; signature change that breaks callers; raising the minimum Python version; behavior change that breaks existing usage; internal-dependency major bump surfacing through the public API |
| **minor** | New public class, function, keyword argument, exception type, or feature behind an existing entry point |
| **patch** | Bug fix in `src/`; runtime dependency bump that does not surface; internal-dependency patch propagated as "Updated dependencies"; user-visible `README.md` fix |

If the in-progress section already proposes a higher bump, **do not downgrade** it.

## Step 5 — Format

Match the style already used in this repo (see `packages/cnpj-gen/CHANGELOG.md`, `packages/cpf-utils/CHANGELOG.md`, `packages/br-utilities/CHANGELOG.md`). Top-level template:

```markdown
# <dist-name>

## <next-version>

### <Section heading>

- **<Topic>** — one-sentence description.

## <previous-version>

...
```

Common section headings, in this order when present:

- `### 🚀 Stable Version Released!` — only for the very first `1.0.0` release; followed by a 4–8 bullet feature overview and the line `For detailed usage and API reference, see the [README](./README.md).`
- `### 🎉 v<N> at a glance 🎊` — only for new major releases beyond `1.0.0`.
- `### BREAKING CHANGES` — required when bumping major. One bullet per break.
- `### New features` (or `### New Features`)
- `### Improvements`
- `### Bug fixes`
- `### Patch Changes` — one bullet per change. End with an `Updated dependencies` group when internal deps changed:

```markdown
### Patch Changes

- Updated dependencies
  - `cpf-gen`: 1.0.0 → 1.0.1
  - `cpf-val`: 1.0.0 → 1.0.1
```

Bullets may lead with a commit short-SHA when the change maps to a specific commit (`cafaf27: **Type hints** — …`).

## Step 6 — Conciseness rules (strict)

- **One sentence per bullet.** Two short sentences only when the second is a brief migration tip.
- **Lead with a bold topic** (`**`-wrapped, 1–4 words) OR a commit short-SHA, then an em-dash or colon, then the description.
- **No expository prose.** Don't explain motivation, internals, or test details. Link to docs instead of recapping them.
- **Use backticks** for every class, function, module, argument, file path, and CLI flag mentioned.
- **Prefer the smallest accurate description.** "Fix `cpf_val` ignoring leading zeros." beats a paragraph.
- **Limit each version section to ≤ 8 bullets total** across all sub-headings.

## Examples

Minimal patch:

```markdown
# cnpj-fmt

## 2.0.1

### Bug fixes

- **Array input** — Fix off-by-one in `CnpjFormatter.format()` when input is a list of strings.
```

Minor addition:

```markdown
## 2.1.0

### New features

- **`strict` option** — `CnpjValidator` now accepts a `strict` option that rejects numeric-only CNPJs when `type` is `"alphanumeric"`.
```

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Path |
|---------|------|
| Format reference | `packages/cnpj-gen/CHANGELOG.md` |
| Aggregator format reference | `packages/br-utilities/CHANGELOG.md` |
| Tag lookup | `cd python && git tag -l '<dist-name>@*' \| sort -V` |
