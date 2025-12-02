"""Build commands for packages."""

__all__ = ["build_all", "build_package", "setup_commands"]

import sys
from argparse import ArgumentParser
from shutil import rmtree

from .common import PACKAGES, PACKAGES_DIR, Spinner, run_command
from .version import VersionContext


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for building packages."""
    build_parser = parser.add_parser("build", help="Build package(s)")
    build_parser.add_argument(
        "package", nargs="?", help="Specific package (leave empty for all)"
    )
    build_parser.add_argument(
        "--install-afterwards",
        "-i",
        action="store_true",
        help="Install the package locally via pip after building",
    )
    build_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Quiet mode: show less output",
    )
    build_parser.add_argument(
        "-v",
        "--version",
        help="Set the version of the package being built",
    )


def build_package(pkg_path, install_afterwards=False, quiet=False, version=None):
    """Build a specific package."""
    if version:
        if not quiet:
            print(f"Setting version to {version} for {pkg_path.name}...")
        try:
            with VersionContext(pkg_path, version):
                return _build_package_impl(pkg_path, install_afterwards, quiet)
        except (FileNotFoundError, ValueError, Exception):
            return False
    else:
        return _build_package_impl(pkg_path, install_afterwards, quiet)


def _build_package_impl(pkg_path, install_afterwards=False, quiet=False):
    """Internal implementation of package building."""
    if not quiet:
        print(f"Building {pkg_path.name}...")

    dist_dir = pkg_path / "dist"

    if install_afterwards and dist_dir.exists():
        rmtree(dist_dir)

    build_cmd = [sys.executable, "-m", "build"]

    if quiet:
        success, _ = run_command(build_cmd, cwd=pkg_path, silent=True)

        if not success:
            return False
    else:
        if not run_command(build_cmd, cwd=pkg_path):
            return False

    if install_afterwards:
        if not dist_dir.exists():
            print(f"Error: dist/ directory not found in {pkg_path.name}")
            return False

        whl_files = sorted(
            dist_dir.glob("*.whl"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not whl_files:
            print(f"Error: No .whl file found in dist/ for {pkg_path.name}")
            return False

        whl_file = whl_files[0]

        if not quiet:
            print(f"Installing {whl_file.name}...")

        install_cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--force-reinstall",
            str(whl_file),
        ]

        if quiet:
            success, _ = run_command(install_cmd, silent=True)

            if not success:
                print(f"Error: Failed to install {whl_file.name}")
                return False
        else:
            if not run_command(install_cmd):
                print(f"Error: Failed to install {whl_file.name}")
                return False

        if not quiet:
            print(f"✅ Successfully installed {pkg_path.name}")

    return True


def build_all(install_afterwards=False, quiet=False, version=None):
    """Build all packages."""
    if version:
        print(
            "Warning: --version option is only supported when building a specific package"
        )
        print("         Ignoring version option for build all")

    if not quiet:
        print("Building all packages...")

    failed = []
    succeeded = []

    def _clear_spinner_line(message: str) -> None:
        """Clear spinner line before printing status."""
        max_length = max(len(message) + 10, 100)
        print("\r" + " " * max_length + "\r", end="", flush=True)

    if quiet:
        with Spinner("Building packages") as spinner:
            for pkg in PACKAGES:
                spinner.update_message(f"Building packages: {pkg}")
                pkg_path = PACKAGES_DIR / pkg

                if build_package(
                    pkg_path,
                    install_afterwards=install_afterwards,
                    quiet=quiet,
                ):
                    succeeded.append(pkg)
                    _clear_spinner_line(f"Building packages: {pkg}")
                    print(f"✅ {pkg}")
                else:
                    failed.append(pkg)
                    _clear_spinner_line(f"Building packages: {pkg}")
                    print(f"❌ {pkg}")
    else:
        for pkg in PACKAGES:
            pkg_path = PACKAGES_DIR / pkg

            if build_package(
                pkg_path, install_afterwards=install_afterwards, quiet=quiet
            ):
                succeeded.append(pkg)
            else:
                failed.append(pkg)

    if failed:
        print(f"\n⚠️  Build failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        if quiet:
            print(f"\n✅ Built {len(succeeded)} package(s) successfully")
        else:
            print("\n✅ All packages built successfully!")
