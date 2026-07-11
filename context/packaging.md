---
id: packaging
title: Packaging, build, and publish
scope: packages/*/pyproject.toml, scripts/build.py, scripts/publish.py, scripts/version.py
triggers:
  - editing a package pyproject.toml
  - changing build-system, setuptools config, or dynamic version
  - building, versioning, or publishing a package
  - configuring pytest or coverage in pyproject.toml
---

# packaging

Manage `pyproject.toml`, builds, versioning, and publishing for br-utils-py packages. All paths are relative to the repo root.

> Python packages **do** have a build step (setuptools → wheel + sdist), unlike the PHP subrepo. But the build is fully driven by `python run build` — do not hand-roll `setup.py` or invoke `setuptools`/`build` directly.

## Repository constraints

- Every package uses the **setuptools** build backend with `src/` layout.
- **Do not run `python run publish`** — publishing to PyPI is the developer's responsibility (see [`context/ci-release.md`](ci-release.md)).
- `[project].version` is **dynamic**, read from the package's `__version__`. Source keeps `__version__ = "0.0.0"`; the real version is injected at build time from the release version. Do not hardcode a real version in source.
- Do not commit build artifacts (`dist/`, `build/`, `*.egg-info/`). They are ignored.

## `pyproject.toml` anatomy

Copy the shape from `packages/cnpj-gen/pyproject.toml`. Required blocks:

```toml
[project]
name = "cnpj-gen"                 # PyPI distribution name (= folder name, except utils/br-utilities)
dynamic = [ "version" ]
description = "..."
license = "MIT"
license-files = [ "LICENSE" ]
keywords = [ ... ]
classifiers = [ ... ]             # include Python :: 3.10 … 3.14 classifiers
requires-python = ">=3.10,<4.0"
dependencies = [                  # runtime deps only — see dependencies.md
  "cnpj-dv>=2.0.0,<2.1.0",
  "lacus.utils>=1.0.0,<2.0.0",
]

  [[project.authors]]
  name = "Julio L. Muller"

  [project.readme]
  file = "README.md"
  content-type = "text/markdown"

  [project.urls]
  Homepage = "..."
  Source = "https://github.com/LacusSolutions/br-utils-py"
  Tracker = "https://github.com/LacusSolutions/br-utils-py/issues"

[build-system]
requires = [ "setuptools>=80.9.0", "wheel" ]
build-backend = "setuptools.build_meta"

[tool.setuptools.dynamic.version]
attr = "cnpj_gen.__version__"     # import namespace + .__version__

[tool.setuptools.packages.find]
where = [ "src/" ]

[tool.pytest.ini_options]
minversion = "9.0"
addopts = [ "--import-mode=importlib" ]
testpaths = [ "tests/" ]
python_files = [ "*.spec.py" ]
python_functions = [ "describe_*", "it_*", "test_*" ]

[tool.coverage.run]
source = [ "src/" ]
omit = [ "tests/*" ]
```

### Public-API-relevant keys

Changes to `name`, `requires-python`, or runtime `dependencies` are **public API** — coordinate through [`context/public-api.md`](public-api.md) and add a CHANGELOG entry. Changes to `[tool.*]` blocks (pytest, coverage) are dev-only.

### Dynamic version target

`[tool.setuptools.dynamic.version].attr` points at `<import_namespace>.__version__`. For the two folders whose namespace differs from the folder, use the import namespace: `lacus.utils.__version__` and `br_utils.__version__`.

## Build / clean commands

```bash
python run build              # build all packages (in dependency order)
python run build cnpj-gen     # build one package → dist/*.whl + *.tar.gz
python run build -i cnpj-gen  # build and install locally afterwards
python run build -v 2.0.1 cnpj-gen  # build with an explicit version
python run clean              # remove build artifacts for all packages
python run clean cnpj-gen     # remove build artifacts for one package
```

The `-v/--version` flag injects the version into `__version__` for the build (used by the release workflow); without it the placeholder `0.0.0` is used, which is fine for local smoke builds.

## Publish (developer only)

`python run publish <pkg>` builds and uploads to PyPI via twine. Agents must **not** run this — it is invoked only by the release workflow or the developer. See [`context/ci-release.md`](ci-release.md).

## Checklist

- [ ] `[project].name` matches the intended PyPI distribution name
- [ ] `dynamic = ["version"]` set; `[tool.setuptools.dynamic.version].attr` points at `<namespace>.__version__`
- [ ] Source `__version__` left as `"0.0.0"` (no hardcoded real version)
- [ ] `requires-python = ">=3.10,<4.0"` and matching `classifiers`
- [ ] `[tool.setuptools.packages.find].where = ["src/"]`
- [ ] Runtime `dependencies` follow [`context/dependencies.md`](dependencies.md); dev tools stay in `requirements-dev.txt`
- [ ] `python run build <pkg>` succeeds; artifacts land in `dist/`
- [ ] Public-API-relevant `pyproject.toml` changes have a CHANGELOG entry

## Package-level overrides

Before applying this harness, check whether the target package defines `packages/<pkg>/AGENTS.md` or `packages/<pkg>/context/`. If either exists and contradicts this file on the same topic, **follow the package-level instruction** (see [`context/README.md`](README.md#instruction-precedence)).

## Reference

| Concern | Path |
|---------|------|
| Canonical leaf config | `packages/cnpj-gen/pyproject.toml` |
| Foundation config (namespace pkg) | `packages/utils/pyproject.toml` |
| Build implementation | `scripts/build.py` |
| Version injection | `scripts/version.py` |
| Publish implementation | `scripts/publish.py` |
| Build/clean commands | `python run build`, `python run clean` |
