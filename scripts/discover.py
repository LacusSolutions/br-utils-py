"""Discover packages and resolve dependencies for topological sorting."""

__all__ = ["get_sorted_packages"]

from pathlib import Path
from typing import Dict, List, Set

# Try to import tomllib (Python 3.11+), fallback to tomli
try:
    import tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError
except ImportError:
    try:
        import tomli
        import tomli as tomllib

        TOMLDecodeError = tomli.TOMLDecodeError
    except ImportError:
        raise ImportError(
            "tomli is required for Python < 3.11. Install it with: pip install tomli"
        )


ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"


def discover_packages() -> List[str]:
    packages = []

    if not PACKAGES_DIR.exists():
        return packages

    for item in PACKAGES_DIR.iterdir():
        if item.is_dir() and (item / "pyproject.toml").exists():
            packages.append(item.name)

    return sorted(packages)


def get_package_dependencies(package_name: str) -> List[str]:
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"

    if not pyproject_path.exists():
        return []

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        dependencies = data.get("project", {}).get("dependencies", [])
        all_packages = discover_packages()
        internal_deps = []

        for dep in dependencies:
            dep_name = dep.strip()

            for op in ["~=", ">=", "<=", "==", "!=", "<", ">"]:
                if op in dep_name:
                    dep_name = dep_name.split(op)[0].strip()
                    break

            if "[" in dep_name:
                dep_name = dep_name.split("[")[0].strip()

            if dep_name in all_packages:
                internal_deps.append(dep_name)

        return internal_deps
    except (KeyError, FileNotFoundError, TOMLDecodeError):
        return []


def get_dependency_graph() -> Dict[str, List[str]]:
    packages = discover_packages()
    graph = {}

    for pkg in packages:
        graph[pkg] = get_package_dependencies(pkg)

    return graph


def topological_sort(packages: List[str], graph: Dict[str, List[str]]) -> List[str]:
    in_degree = {pkg: 0 for pkg in packages}
    reverse_graph: Dict[str, List[str]] = {pkg: [] for pkg in packages}

    for pkg, deps in graph.items():
        for dep in deps:
            if dep in reverse_graph:
                reverse_graph[dep].append(pkg)
                in_degree[pkg] += 1

    queue = [pkg for pkg in packages if in_degree[pkg] == 0]
    result = []

    while queue:
        queue.sort()
        pkg = queue.pop(0)
        result.append(pkg)

        for dependent in reverse_graph[pkg]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    remaining = [pkg for pkg in packages if pkg not in result]
    result.extend(sorted(remaining))

    return result


def get_sorted_packages() -> List[str]:
    """Get all packages sorted topologically (dependencies first)."""
    packages = discover_packages()
    graph = get_dependency_graph()

    return topological_sort(packages, graph)
