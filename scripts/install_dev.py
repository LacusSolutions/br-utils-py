"""Install development dependencies."""

__all__ = ["install_dev"]

import sys
from .common import PACKAGES, PACKAGES_DIR, ROOT_DIR, run_command


def install_dev():
    """Install development dependencies."""
    print("Installing development dependencies...")

    run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(ROOT_DIR / "requirements-dev.txt"),
        ]
    )

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg
        req_file = pkg_path / "requirements-dev.txt"

        if req_file.exists():
            print(f"Installing development dependencies for {pkg}...")
            run_command(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                check=False,
            )

    run_command([sys.executable, "-m", "pip", "install", "build", "twine"])
