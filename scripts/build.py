"""Build commands for packages."""

__all__ = ["build_all", "build_package"]

import shutil
import sys

from .common import PACKAGES, PACKAGES_DIR, run_command


def build_package(pkg_path, install_afterwards=False):
    """Build an specific package."""
    print(f"Building {pkg_path.name}...")

    if not run_command([sys.executable, "-m", "build"], cwd=pkg_path):
        return False

    if install_afterwards:
        dist_dir = pkg_path / "dist"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        else:
            print(f"Error: dist/ directory not found in {pkg_path.name}")
            return False

        # Find the most recent .whl file
        whl_files = list(dist_dir.glob("*.whl"))
        if not whl_files:
            print(f"Error: No .whl file found in dist/ for {pkg_path.name}")
            return False

        # Sort by modification time, most recent first
        whl_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        whl_file = whl_files[0]

        print(f"Installing {whl_file.name}...")
        if not run_command(
            [sys.executable, "-m", "pip", "install", "--force-reinstall", str(whl_file)]
        ):
            print(f"Error: Failed to install {whl_file.name}")
            return False

        print(f"✅ Successfully installed {pkg_path.name}")

    return True


def build_all(install_afterwards=False):
    """Build all packages."""
    print("Building all packages...")
    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not build_package(pkg_path, install_afterwards=install_afterwards):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Build failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✅ All packages built successfully!")
