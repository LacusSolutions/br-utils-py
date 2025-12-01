"""Clean build files."""

__all__ = ["clean_all", "clean_package", "setup_commands"]

from argparse import ArgumentParser
from pathlib import Path

from .common import ROOT_DIR, run_command

PATTERNS_TO_REMOVE = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    "build",
    "dist",
    ".coverage",
    ".pytest_cache",
    "htmlcov",
]


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for removing build files."""
    clean_parser = parser.add_parser("clean", help="Remove build files")
    clean_parser.add_argument(
        "package", nargs="?", help="Specific package (leave empty for all)"
    )


def _clean_path(target_path: Path, label: str) -> None:
    """Remove build files from a specific path."""
    print(f"Cleaning {label}...")

    removed_count = 0

    for pattern in PATTERNS_TO_REMOVE:
        for path in target_path.rglob(pattern):
            try:
                relative_path = path.relative_to(ROOT_DIR)
            except ValueError:
                relative_path = path

            if path.is_dir():
                print(f"Removing directory: {relative_path}")
                run_command(["rm", "-rf", str(path)], silent=True)
                removed_count += 1
            elif path.is_file():
                print(f"Removing file: {relative_path}")
                path.unlink()
                removed_count += 1

    print(f"✅ Cleanup completed. {removed_count} items removed.")


def clean_package(pkg_path: Path) -> None:
    """Remove build files for a specific package."""
    _clean_path(pkg_path, pkg_path.name)


def clean_all():
    """Remove build files."""
    _clean_path(ROOT_DIR, "build files")
