"""Clean build files."""

__all__ = ["clean"]

import subprocess

from .common import ROOT_DIR


def clean():
    """Remove build files."""
    print("Cleaning build files...")

    removed_count = 0
    patterns_to_remove = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.egg-info",
        "build",
        "dist",
        ".pytest_cache",
        "htmlcov",
    ]

    for pattern in patterns_to_remove:
        for path in ROOT_DIR.rglob(pattern):
            if path.is_dir():
                print(f"Removing directory: {path}")
                subprocess.run(["rm", "-rf", str(path)], check=False)
                removed_count += 1
            elif path.is_file():
                print(f"Removing file: {path}")
                path.unlink()
                removed_count += 1

    coverage_file = ROOT_DIR / ".coverage"

    if coverage_file.exists() and coverage_file.is_file():
        print(f"Removing file: {coverage_file}")
        coverage_file.unlink()
        removed_count += 1

    print(f"✅ Cleanup completed. {removed_count} items removed.")
