"""Common utilities and constants for monorepo management scripts."""

__all__ = ["PACKAGES", "PACKAGES_DIR", "ROOT_DIR", "run_command"]

import subprocess
from pathlib import Path

from .discover import get_sorted_packages

ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"
PACKAGES = get_sorted_packages()


def run_command(cmd, cwd=None, check=True):
    """Run a system command and return the result."""
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, cwd=cwd, check=check)

        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
