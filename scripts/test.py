"""Test commands for packages."""

__all__ = ["setup_commands", "test_all", "test_package", "test_watch"]

import sys
import time
from argparse import ArgumentParser
from pathlib import Path

from .common import PACKAGES, PACKAGES_DIR, run_command


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for running unit tests."""
    test_parser = parser.add_parser("test", help="Run tests for package(s)")
    test_parser.add_argument(
        "package", nargs="?", help="Specific package (leave empty for all)"
    )
    test_parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="Run tests continuously (watch mode)",
    )
    test_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Quiet mode: show less output",
    )
    test_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose mode: show more output",
    )


def test_package(pkg_path: Path, quiet: bool, verbose: bool):
    """Run tests for a specific package."""
    if not quiet:
        print(f"Running tests for {pkg_path.name}...")

    pytest_args = [sys.executable, "-m", "pytest"]

    if quiet:
        pytest_args.extend(["-q", "--tb=short", "--no-header"])
    elif verbose:
        pytest_args.append("-v")
    else:
        pytest_args.append("--tb=short")

    return run_command(pytest_args, cwd=pkg_path)


def test_all(quiet: bool, verbose: bool):
    """Run tests for all packages."""
    print("Running tests for all packages...")

    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not test_package(pkg_path, quiet=quiet, verbose=verbose):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Tests failed for the following packages: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")


def test_watch(package: str | None, quiet: bool, verbose: bool):
    """Run tests continuously in watch mode."""
    print("🔄 Watch mode: Tests will run continuously...", flush=True)
    print("Press Ctrl+C to stop\n", flush=True)

    pkg_path = None

    if package:
        if package not in PACKAGES:
            print(f"Error: Package '{package}' not found.")
            sys.exit(1)

        pkg_path = PACKAGES_DIR / package

    try:
        iteration = 0

        while True:
            iteration += 1
            print(f"\n{'=' * 60}", flush=True)
            print(f"🔄 Iteration {iteration} - {time.strftime('%H:%M:%S')}", flush=True)
            print(f"{'=' * 60}\n", flush=True)

            if pkg_path:
                test_package(pkg_path, quiet=quiet, verbose=verbose)
            else:
                test_all(quiet=quiet, verbose=verbose)

            print("\n⏳ Waiting 2 seconds before next run...", flush=True)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n👋 Watch mode stopped by user.", flush=True)
        sys.exit(0)
