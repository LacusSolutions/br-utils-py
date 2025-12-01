"""Linting and formatting commands for packages."""

__all__ = [
    "lint_all",
    "lint_files",
    "lint_package",
    "setup_commands",
]

import sys
from argparse import ArgumentParser
from pathlib import Path

from .common import (
    ROOT_DIR,
    Spinner,
    run_command,
)

PATTERNS_TO_LINT = [
    "require",
    "run",
    "*.py",
]


def setup_commands(parser: ArgumentParser):
    """Setup CLI arguments for linting and formatting."""
    lint_parser = parser.add_parser("lint", help="Run linting and formatting")
    lint_parser.add_argument("package", nargs="*", help="Specific package (optional)")


def lint_path(path: Path) -> tuple[bool, list[str]]:
    """Run linting and formatting on a file or directory.

    Returns:
        Tuple of (success, list of error messages)
    """
    succeeded = True
    errors = []
    files = set()

    for pattern in PATTERNS_TO_LINT:
        if pattern.endswith(".py"):
            files.update(path.rglob(pattern))
        else:
            for found_path in path.rglob(pattern):
                if found_path.is_file() and found_path.name == pattern:
                    files.add(found_path)

    if not files:
        return True, []

    def _check_error(success: bool, output: str, tool_name: str) -> bool:
        """Check if command output indicates an error."""
        if not success and output:
            if tool_name == "ruff check":
                if "All checks passed!" not in output:
                    return True
            elif "error" in output.lower() or "failed" in output.lower():
                return True
        return False

    with Spinner("Linting files") as spinner:
        for file in sorted(files):  # Sort for consistent processing order
            try:
                relative_path = file.relative_to(ROOT_DIR)
            except ValueError:
                relative_path = file

            spinner.update_message(f"Linting files: {relative_path}")
            success, output = run_command(
                [sys.executable, "-m", "ruff", "check", "--fix", str(file)],
                cwd=ROOT_DIR,
                silent=True,
            )

            if _check_error(success, output, "ruff check"):
                errors.append(f"ruff linting failed for {file!s}:\n{output}")
                succeeded = False

            success, output = run_command(
                [sys.executable, "-m", "ruff", "format", str(file)],
                cwd=ROOT_DIR,
                silent=True,
            )

            if _check_error(success, output, "ruff format"):
                errors.append(f"ruff formatting failed for {file!s}:\n{output}")
                succeeded = False

            success, output = run_command(
                [sys.executable, "-m", "black", str(file)],
                cwd=ROOT_DIR,
                silent=True,
            )

            if _check_error(success, output, "black"):
                errors.append(f"black formatting failed for {file!s}:\n{output}")
                succeeded = False

    return succeeded, errors


def lint_files(paths: list[Path]) -> bool:
    """Run linting and formatting on a list of files or directories."""
    all_errors = []

    for path in paths:
        succeeded, errors = lint_path(path)
        if not succeeded:
            all_errors.extend(errors)

    if not all_errors:
        print("✅ All linting passed!")
        return True

    print("\n".join(all_errors))

    return False


def _print_lint_result(succeeded: bool, errors: list[str]) -> bool:
    """Print linting result and return success status."""
    if succeeded:
        print("✅ All linting passed!")
        return True

    print("\n".join(errors))

    return False


def lint_package(pkg_path: Path = ROOT_DIR) -> bool:
    """Run linting and formatting on a specific directory or the entire repository."""
    succeeded, errors = lint_path(pkg_path)

    return _print_lint_result(succeeded, errors)


def lint_all() -> bool:
    """Run linting and formatting on entire project."""
    succeeded, errors = lint_path(ROOT_DIR)

    return _print_lint_result(succeeded, errors)
