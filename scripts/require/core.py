"""Install development and monorepo package dependencies.

This module is intentionally free of imports from other ``scripts`` packages so
``python/require`` can bootstrap a fresh environment (including Python 3.10,
where ``tomli`` is not installed until ``requirements-dev.txt`` is applied).
"""

from __future__ import annotations

import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"
REQUIREMENTS_DEV_FILE = ROOT_DIR / "requirements-dev.txt"

_DEPENDENCY_OPERATORS = ["~=", ">=", "<=", "==", "!=", "<", ">"]


def _run_pip_install(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", *args],
        capture_output=True,
        text=True,
    )


def _load_tomllib():
    try:
        import tomllib

        return tomllib
    except ImportError:
        result = _run_pip_install(["tomli"])

        if result.returncode != 0:
            print('❌ Failed to install "tomli" (required on Python < 3.11).')
            if result.stderr:
                print(result.stderr)
            sys.exit(result.returncode)

        import tomli

        return tomli


def discover_packages() -> list[str]:
    packages = []

    if not PACKAGES_DIR.exists():
        return packages

    for item in PACKAGES_DIR.iterdir():
        if item.is_dir() and (item / "pyproject.toml").exists():
            packages.append(item.name)

    return sorted(packages)


def _parse_dependency_name(dependency: str) -> str:
    dep_name = dependency.strip()

    for operator in _DEPENDENCY_OPERATORS:
        if operator in dep_name:
            dep_name = dep_name.split(operator)[0].strip()
            break

    if "[" in dep_name:
        dep_name = dep_name.split("[")[0].strip()

    return dep_name


def _read_pyproject(package_name: str) -> dict:
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"
    tomllib = _load_tomllib()

    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def get_distribution_name(package_name: str) -> str | None:
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"

    if not pyproject_path.exists():
        return None

    try:
        data = _read_pyproject(package_name)
        return data.get("project", {}).get("name")
    except (KeyError, OSError, ValueError):
        return None


def build_distribution_map() -> dict[str, str]:
    distribution_map: dict[str, str] = {}

    for package_name in discover_packages():
        distribution_name = get_distribution_name(package_name)

        if distribution_name:
            distribution_map[distribution_name] = package_name

        distribution_map[package_name] = package_name

    return distribution_map


def get_package_dependencies(package_name: str) -> list[str]:
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"

    if not pyproject_path.exists():
        return []

    try:
        data = _read_pyproject(package_name)
        dependencies = data.get("project", {}).get("dependencies", [])
        distribution_map = build_distribution_map()
        internal_deps = []

        for dep in dependencies:
            dep_name = _parse_dependency_name(dep)

            if dep_name in distribution_map:
                internal_deps.append(distribution_map[dep_name])

        return internal_deps
    except (KeyError, OSError, ValueError):
        return []


def get_dependency_graph() -> dict[str, list[str]]:
    return {pkg: get_package_dependencies(pkg) for pkg in discover_packages()}


def topological_sort(packages: list[str], graph: dict[str, list[str]]) -> list[str]:
    in_degree = dict.fromkeys(packages, 0)
    reverse_graph: dict[str, list[str]] = {pkg: [] for pkg in packages}

    for pkg, deps in graph.items():
        for dep in deps:
            if dep in reverse_graph:
                reverse_graph[dep].append(pkg)
                in_degree[pkg] += 1

    queue = sorted(pkg for pkg in packages if in_degree[pkg] == 0)
    result = []

    while queue:
        pkg = queue.pop(0)
        result.append(pkg)

        for dependent in reverse_graph[pkg]:
            in_degree[dependent] -= 1

            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()

    remaining = sorted(pkg for pkg in packages if pkg not in result)
    result.extend(remaining)

    return result


def get_sorted_packages() -> list[str]:
    packages = discover_packages()
    graph = get_dependency_graph()

    return topological_sort(packages, graph)


def get_dependency_closure(package_name: str) -> list[str]:
    if package_name not in discover_packages():
        return []

    graph = get_dependency_graph()
    closure: set[str] = set()

    def collect(pkg: str) -> None:
        if pkg in closure:
            return

        for dep in graph.get(pkg, []):
            collect(dep)

        closure.add(pkg)

    collect(package_name)

    subgraph = {pkg: graph[pkg] for pkg in closure}

    return topological_sort(sorted(closure), subgraph)


def install_dev_dependencies() -> None:
    """Install dependencies from requirements-dev.txt."""
    if not REQUIREMENTS_DEV_FILE.exists():
        print(f'⚠️  "{REQUIREMENTS_DEV_FILE.name}" not found. Skipping...')
        return

    result = _run_pip_install(["--upgrade", "-r", str(REQUIREMENTS_DEV_FILE)])

    if result.returncode == 0:
        print(f'✅ "{REQUIREMENTS_DEV_FILE.name}" dependencies installed successfully.')
        return

    print(f'❌ "{REQUIREMENTS_DEV_FILE.name}" failed to install dependencies.')
    if result.stderr:
        print(result.stderr)
    sys.exit(result.returncode)


def install_packages(packages: list[str]) -> None:
    """Install monorepo packages as editable installs in dependency order."""
    if not packages:
        return

    for package_name in packages:
        package_path = PACKAGES_DIR / package_name

        if not package_path.exists():
            print(f"Error: Package '{package_name}' not found.")
            sys.exit(1)

        print(f'Installing "{package_name}" in editable mode...')
        result = _run_pip_install(["--no-deps", "-e", str(package_path)])

        if result.returncode == 0:
            print(f'✅ "{package_name}" installed successfully.')
            continue

        print(f'❌ "{package_name}" failed to install.')
        if result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)


def require(package: str | None = None, *, dev_only: bool = False) -> None:
    """Install development and monorepo package dependencies."""
    print("Installing dependencies...")
    install_dev_dependencies()

    if dev_only:
        return

    if package is None:
        install_packages(get_sorted_packages())
        return

    if package not in discover_packages():
        print(f"Error: Package '{package}' not found.")
        print(f"Available packages: {', '.join(discover_packages())}")
        sys.exit(1)

    install_packages(get_dependency_closure(package))


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint for installing dependencies."""
    parser = ArgumentParser(description="Install monorepo dependencies")
    parser.add_argument(
        "package",
        nargs="?",
        help="Specific package (leave empty for all monorepo packages)",
    )
    parser.add_argument(
        "--dev-only",
        action="store_true",
        help="Install development dependencies only",
    )
    args = parser.parse_args(argv)

    require(args.package, dev_only=args.dev_only)
