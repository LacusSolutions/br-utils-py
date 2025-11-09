"""Test commands for packages."""

__all__ = ["test_package", "test_all"]

import sys
from .common import PACKAGES, PACKAGES_DIR, run_command


def test_package(pkg_path):
    """Run tests for an specific package."""
    print(f"Running tests for {pkg_path.name}...")

    return run_command([sys.executable, "-m", "pytest"], cwd=pkg_path)


def test_all():
    """Run tests for all packages."""
    print("Running tests for all packages...")
    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not test_package(pkg_path):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Tests failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
