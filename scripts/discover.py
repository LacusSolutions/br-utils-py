"""Discover packages and resolve dependencies for topological sorting."""

__all__ = [
    "build_distribution_map",
    "discover_packages",
    "get_dependency_closure",
    "get_distribution_name",
    "get_package_dependencies",
    "get_sorted_packages",
]

from pathlib import Path

# Try to import tomllib (Python 3.11+), fallback to tomli
try:
    import tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError
except ImportError:
    import tomli as tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError


ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"

_DEPENDENCY_OPERATORS = ["~=", ">=", "<=", "==", "!=", "<", ">"]


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


def get_distribution_name(package_name: str) -> str | None:
    """Return the PyPI distribution name for a monorepo package folder."""
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"

    if not pyproject_path.exists():
        return None

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        return data.get("project", {}).get("name")
    except (KeyError, FileNotFoundError, TOMLDecodeError):
        return None


def build_distribution_map() -> dict[str, str]:
    """Map PyPI distribution names to monorepo package folder names."""
    distribution_map: dict[str, str] = {}

    for package_name in discover_packages():
        distribution_name = get_distribution_name(package_name)

        if distribution_name:
            distribution_map[distribution_name] = package_name

        distribution_map[package_name] = package_name

    return distribution_map


def _resolve_internal_dependency(
    dependency_name: str,
    distribution_map: dict[str, str],
) -> str | None:
    if dependency_name in distribution_map:
        return distribution_map[dependency_name]

    return None


def get_package_dependencies(package_name: str) -> list[str]:
    pyproject_path = PACKAGES_DIR / package_name / "pyproject.toml"

    if not pyproject_path.exists():
        return []

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        dependencies = data.get("project", {}).get("dependencies", [])
        distribution_map = build_distribution_map()
        internal_deps = []

        for dep in dependencies:
            dep_name = _parse_dependency_name(dep)
            internal_dep = _resolve_internal_dependency(dep_name, distribution_map)

            if internal_dep is not None:
                internal_deps.append(internal_dep)

        return internal_deps
    except (KeyError, FileNotFoundError, TOMLDecodeError):
        return []


def get_dependency_graph() -> dict[str, list[str]]:
    packages = discover_packages()
    graph = {}

    for pkg in packages:
        graph[pkg] = get_package_dependencies(pkg)

    return graph


def topological_sort(packages: list[str], graph: dict[str, list[str]]) -> list[str]:
    """Perform topological sort using Kahn's algorithm."""
    in_degree = dict.fromkeys(packages, 0)
    reverse_graph: dict[str, list[str]] = {pkg: [] for pkg in packages}

    for pkg, deps in graph.items():
        for dep in deps:
            if dep in reverse_graph:
                reverse_graph[dep].append(pkg)
                in_degree[pkg] += 1

    queue = sorted([pkg for pkg in packages if in_degree[pkg] == 0])
    result = []

    while queue:
        pkg = queue.pop(0)
        result.append(pkg)

        for dependent in reverse_graph[pkg]:
            in_degree[dependent] -= 1

            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort()

    remaining = sorted([pkg for pkg in packages if pkg not in result])
    result.extend(remaining)

    return result


def get_sorted_packages() -> list[str]:
    """Get all packages sorted topologically (dependencies first)."""
    packages = discover_packages()
    graph = get_dependency_graph()

    return topological_sort(packages, graph)


def get_dependency_closure(package_name: str) -> list[str]:
    """Return a package and its internal dependencies in topological order."""
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
