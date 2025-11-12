"""Linting and formatting commands for packages."""

__all__ = [
    "format",
    "format_all",
    "lint",
    "lint_all",
]

import sys
from pathlib import Path

from .common import (
    PACKAGES,
    PACKAGES_DIR,
    ROOT_DIR,
    SCRIPTS_DIR,
    run_command,
)


def lint(pkg_path: Path | None = None) -> bool:
    """Run linting on a specific directory or the entire repository."""
    if pkg_path is None:
        pkg_path = ROOT_DIR

    print(f"Running linting for {pkg_path.name}...")
    ruff_cmd = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        str(pkg_path),
    ]

    return run_command(ruff_cmd, cwd=ROOT_DIR)


def lint_all() -> bool:
    """Run linting on all packages and root."""
    print("Running linting for all packages...")
    failed = []

    if not lint(SCRIPTS_DIR):
        failed.append("scripts")

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not lint(pkg_path):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Linting failed for: {', '.join(failed)}")

        return False

    print("\n✅ All linting passed!")

    return True


def format(pkg_path: Path | None = None) -> bool:
    """Format code for a specific directory or the entire repository."""
    if pkg_path is None:
        pkg_path = ROOT_DIR

    print(f"Formatting code for {pkg_path.name}...")
    ruff_format_cmd = [
        sys.executable,
        "-m",
        "ruff",
        "format",
        str(pkg_path),
    ]

    if not run_command(ruff_format_cmd, cwd=ROOT_DIR):
        return False

    black_cmd = [
        sys.executable,
        "-m",
        "black",
        str(pkg_path),
    ]

    return run_command(black_cmd, cwd=ROOT_DIR)


def format_all() -> bool:
    """Format code for all packages and root."""
    print("Formatting code for all packages...")
    failed = []

    if not format(SCRIPTS_DIR):
        failed.append("scripts")

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg

        if not format(pkg_path):
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Formatting failed for: {', '.join(failed)}")

        return False
    print("\n✅ All formatting completed!")

    return True
