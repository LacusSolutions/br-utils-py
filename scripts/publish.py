"""Publish commands for packages."""

__all__ = ["publish_all", "publish_package"]

import sys
from argparse import ArgumentParser

from .build import build_package
from .common import PACKAGES, PACKAGES_DIR, run_command


def setup_commands(parser: ArgumentParser):
    """Setup CLI arguments for publishing packages."""
    publish_parser = parser.add_parser("publish", help="Publish package(s) to PyPI")
    publish_parser.add_argument("package", help="Specific package")


def publish_package(pkg_path) -> bool:
    """Publish a specific package to PyPI."""
    print(f"Publishing {pkg_path.name}...")

    if not build_package(pkg_path):
        print(f"Error: Failed to build {pkg_path.name}")
        return False

    return run_command(
        [sys.executable, "-m", "twine", "upload", "dist/*"], cwd=pkg_path
    )


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
        print(
            f"\n⚠️  Publication failed for the following packages: {', '.join(failed)}"
        )
        sys.exit(1)

    print("\n✅ All packages published successfully!")
