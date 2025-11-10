"""Build commands for packages."""

__all__ = ["build_all", "build_package"]

import sys

from .common import PACKAGES, PACKAGES_DIR, run_command


def build_package(pkg_path):
    """Build an specific package."""
    print(f"Building {pkg_path.name}...")

    return run_command([sys.executable, "-m", "build"], cwd=pkg_path)


def build_all():
    """Build all packages."""
    print("Building all packages...")
    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not build_package(pkg_path):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Build failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✅ All packages built successfully!")
