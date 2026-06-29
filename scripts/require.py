"""Install development and package dependencies."""

__all__ = ["install_dev_dependencies", "install_packages", "require", "setup_commands"]

import subprocess
import sys
from argparse import ArgumentParser

from .common import PACKAGES, PACKAGES_DIR, ROOT_DIR
from .discover import get_dependency_closure, get_sorted_packages

REQUIREMENTS_DEV_FILE = ROOT_DIR / "requirements-dev.txt"


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for installing dependencies."""
    require_parser = parser.add_parser(
        "require",
        help="Install development and monorepo package dependencies",
    )
    require_parser.add_argument(
        "package",
        nargs="?",
        help="Specific package (leave empty for all monorepo packages)",
    )
    require_parser.add_argument(
        "--dev-only",
        action="store_true",
        help="Install development dependencies only",
    )


def _run_pip_install(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", *args],
        capture_output=True,
        text=True,
    )


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

    if package not in PACKAGES:
        print(f"Error: Package '{package}' not found.")
        print(f"Available packages: {', '.join(PACKAGES)}")
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
