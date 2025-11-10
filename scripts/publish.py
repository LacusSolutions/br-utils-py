"""Publish commands for packages."""

__all__ = ["publish_all", "publish_package"]

import sys

from .build import build_package
from .common import PACKAGES, PACKAGES_DIR, run_command


def publish_package(pkg_path):
    """Publish an specific package to PyPI."""
    print(f"Publishing {pkg_path.name}...")

    if not build_package(pkg_path):
        print(f"Error: Failed to build {pkg_path.name}")
        return False

    return run_command([sys.executable, "-m", "twine", "upload", "dist/*"], cwd=pkg_path)


def publish_all():
    """Publish all packages to PyPI."""
    print("Publishing all packages...")
    print("⚠️  Make sure PyPI credentials are configured!")
    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not publish_package(pkg_path):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Publication failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✅ All packages published successfully!")
