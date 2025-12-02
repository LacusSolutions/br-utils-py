"""Publish commands for packages."""

__all__ = ["publish_all", "publish_package"]

import sys
from argparse import ArgumentParser

from .common import PACKAGES, PACKAGES_DIR, run_command


def setup_commands(parser: ArgumentParser):
    """Setup CLI arguments for publishing packages."""
    publish_parser = parser.add_parser("publish", help="Publish package(s) to PyPI")
    publish_parser.add_argument("package", help="Specific package")


def publish_package(pkg_path) -> bool:
    """Publish a specific package to PyPI."""
    print(f"Publishing {pkg_path.name}...")

    dist_dir = pkg_path / "dist"

    if not dist_dir.exists():
        print(f"Error: No distribution files found for {pkg_path.name}")
        print("       The 'dist/' directory does not exist.")
        print(f"       Please run 'python run build {pkg_path.name}' first.")
        return False

    dist_files = list(dist_dir.glob("*"))

    if not dist_files:
        print(f"Error: No distribution files found for {pkg_path.name}")
        print("       The 'dist/' directory is empty.")
        print(f"       Please run 'python run build {pkg_path.name}' first.")
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
