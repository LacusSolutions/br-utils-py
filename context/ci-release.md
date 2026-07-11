---
id: ci-release
title: CI and release awareness
scope: .github/workflows/
triggers:
  - editing CI or release workflow files
  - understanding the build and test pipeline
  - verifying local changes before claiming done
  - investigating a CI failure
---

# ci-release

This harness documents CI and release workflows for awareness. Agents do **not** run releases or publish. All paths are relative to the repo root.

## Repository constraints

- **Do not run** `python run release`, `python run publish`, create GitHub Releases, or push git tags. Only the developer (via the release workflow) does that.
- CI workflow edits must stay within `.github/workflows/`.
- Do not add secrets, tokens, or credentials to workflow files.
- Before claiming any implementation task is done, validate locally with the commands in [Local validation](#local-validation-commands).

## CI workflow (`.github/workflows/ci.yml`)

Triggered on every push to any branch and on `workflow_dispatch`.

### Discovery step

CI first **dynamically discovers** packages by scanning `packages/*/`:

- A package joins the **lint** matrix if it has a `run` script.
- A package joins the **test** matrix if it has both a `run` script and a `tests/` directory.

Adding a new package is picked up automatically once it has a `run` script (and `tests/` for the test matrix).

### Matrix jobs

Two reusable workflows run in parallel after discovery:

| Job | Workflow | Matrix |
|-----|----------|--------|
| Lint | `.github/workflows/.lint.yml` | `packages × Python [3.10, 3.11, 3.12, 3.13, 3.14]` |
| Test | `.github/workflows/.test.yml` | `packages × Python [3.10, 3.11, 3.12, 3.13, 3.14]` |

The test workflow receives `api-url` (from the `BR_UTILS_API_URL` repo variable) and `api-token` (from the `BR_UTILS_API_TOKEN` secret) for suites that hit a remote validation API. Do not add new external-API test dependencies without developer approval.

## Release workflow (`.github/workflows/release.yml`)

Triggered by **manual `workflow_dispatch`** only. Inputs: `package` (required — the folder name), `version` (optional — defaults to the latest section in `CHANGELOG.md`).

Steps:
1. Run lint + test for the package (reusable workflows).
2. Prepare release notes from `packages/<pkg>/CHANGELOG.md` via `python run release`; read the PyPI name from `pyproject.toml`.
3. Validate git state: the tag `<pypi-name>@X.Y.Z` must not already exist, and a `<pkg>/main` branch must exist.
4. Build and publish to PyPI (`python run build -v <version>` then `python run publish`).
5. Create a GitHub Release with tag `<pypi-name>@X.Y.Z` (marked pre-release for `.dev`/`.alpha`/`.beta`/`.rc` versions).

Agents never trigger or simulate this workflow. If you need to release a package, ask the developer.

## Other workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `subtrees-sync.yml` | push to `main` | Sync each package to its `<pkg>/main` branch and standalone repo `br-utils-py_<pkg>` |
| `license-update.yml` | LICENSE change | Propagate root `LICENSE` to packages |
| `pr-author-assign.yml` | PR opened | Auto-assign the PR author |

Agents do not interact with these directly.

## Local validation commands

Run these from the repo root before declaring any implementation task complete:

```bash
# One package — CI-equivalent
python run lint <pkg>
python run test <pkg>

# Everything
python run lint
python run test
```

If any command fails, fix the issue before marking the task done.

## When to edit workflow files

Edit `.github/workflows/*.yml` only when:
- Adding a new job or check required by a tooling decision.
- Bumping a pinned action version (actions are pinned by SHA) after developer approval.
- Fixing a broken workflow step.

Workflow file changes are dev-only and do **not** require a CHANGELOG entry.

## Reference

| Concern | Path |
|---------|------|
| CI entry | `.github/workflows/ci.yml` |
| Reusable lint workflow | `.github/workflows/.lint.yml` |
| Reusable test workflow | `.github/workflows/.test.yml` |
| Release workflow | `.github/workflows/release.yml` |
| Subtree sync | `.github/workflows/subtrees-sync.yml` |
| CLI router | `run` (`python run lint`, `python run test`, `python run release`, …) |
| Changelog harness | [`context/changelogs.md`](changelogs.md) |
