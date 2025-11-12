"""Linting and formatting commands for packages."""

__all__ = [
    "lint",
    "lint_all",
    "lint_files",
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
    """Run linting and formatting on a specific directory or the entire repository."""
    if pkg_path is None:
        pkg_path = ROOT_DIR

    print(f"Running linting for {pkg_path.name}...")
    ruff_cmd = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        "--fix-only",
        str(pkg_path),
    ]

    if not run_command(ruff_cmd, cwd=ROOT_DIR):
        return False

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


def lint_files(paths: list[Path]) -> bool:
    """Run linting and formatting on a list of files or directories."""
    failed = []
    python_extensions = {".py"}

    for path in paths:
        # Skip non-Python files (only lint .py files or directories)
        if path.is_file() and path.suffix not in python_extensions:
            continue

        if not lint(path):
            failed.append(str(path))

    if failed:
        print(f"\n⚠️  Linting failed for: {', '.join(failed)}")
        return False

    print("\n✅ All linting passed!")
    return True


def lint_all() -> bool:
    """Run linting and formatting on all packages and root."""
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
