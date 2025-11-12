"""`p`re-commit` hooks management."""

__all__ = ["install_hooks", "run_hooks", "uninstall_hooks", "update_hooks"]

import subprocess
import sys

from .common import ROOT_DIR


def install_hooks() -> bool:
    """Install pre-commit hooks."""
    print("Installing pre-commit hooks...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pre_commit", "install"],
            cwd=ROOT_DIR,
            check=True,
        )

        print("\n✅ Pre-commit hooks installed successfully!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing pre-commit hooks: {e}")

        return False
    except FileNotFoundError:
        print("Error: pre-commit is not installed.")
        print("Install it with: pip install pre-commit")

        return False


def uninstall_hooks() -> bool:
    """Uninstall pre-commit hooks."""
    print("Uninstalling pre-commit hooks...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pre_commit", "uninstall"],
            cwd=ROOT_DIR,
            check=True,
        )

        print("\n✅ Pre-commit hooks uninstalled successfully!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error uninstalling pre-commit hooks: {e}")

        return False
    except FileNotFoundError:
        print("Error: pre-commit is not installed.")

        return False


def update_hooks() -> bool:
    """Update pre-commit hooks to latest versions."""
    print("Updating pre-commit hooks...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pre_commit", "autoupdate"],
            cwd=ROOT_DIR,
            check=True,
        )

        print("\n✅ Pre-commit hooks updated successfully!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error updating pre-commit hooks: {e}")

        return False
    except FileNotFoundError:
        print("Error: pre-commit is not installed.")

        return False


def run_hooks() -> bool:
    """Run pre-commit hooks on all files."""
    print("Running pre-commit hooks on all files...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pre_commit", "run", "--all-files"],
            cwd=ROOT_DIR,
            check=True,
        )

        print("\n✅ All pre-commit hooks passed!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Some pre-commit hooks failed: {e}")

        return False
    except FileNotFoundError:
        print("Error: pre-commit is not installed.")

        return False
