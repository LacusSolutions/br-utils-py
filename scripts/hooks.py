"""`pre-commit` hooks management."""

__all__ = [
    "install_hooks",
    "run_hooks",
    "setup_commands",
    "uninstall_hooks",
    "update_hooks",
]

import sys
from argparse import ArgumentParser

from .common import ROOT_DIR, run_command


def setup_commands(parser: ArgumentParser):
    """Setup CLI arguments for pre-commit hooks management."""
    hooks_parser = parser.add_parser("hooks", help="Manage pre-commit hooks")
    hooks_subparsers = hooks_parser.add_subparsers(
        dest="hooks_command", help="Hooks command"
    )
    hooks_subparsers.add_parser("install", help="Install pre-commit hooks")
    hooks_subparsers.add_parser("uninstall", help="Uninstall pre-commit hooks")
    hooks_subparsers.add_parser(
        "update", help="Update pre-commit hooks to latest versions"
    )
    hooks_subparsers.add_parser("run", help="Run pre-commit hooks on all files")


def _run_hook_command(command: list[str], action: str, success_msg: str) -> None:
    """Run a pre-commit hook command with consistent error handling."""
    print(f"{action}...")

    if not run_command([sys.executable, "-m", "pre_commit", *command], cwd=ROOT_DIR):
        if action == "Installing pre-commit hooks":
            print("Install it with: pip install pre-commit")
        else:
            print(f"\n❌ Error {action.lower()}.")
        sys.exit(1)

    print(f"\n✅ {success_msg}!")


def install_hooks():
    """Install pre-commit hooks."""
    _run_hook_command(
        ["install"],
        "Installing pre-commit hooks",
        "Pre-commit hooks installed successfully",
    )


def uninstall_hooks():
    """Uninstall pre-commit hooks."""
    _run_hook_command(
        ["uninstall"],
        "Uninstalling pre-commit hooks",
        "Pre-commit hooks uninstalled successfully",
    )


def update_hooks():
    """Update pre-commit hooks to latest versions."""
    _run_hook_command(
        ["autoupdate"],
        "Updating pre-commit hooks",
        "Pre-commit hooks updated successfully",
    )


def run_hooks():
    """Run pre-commit hooks on all files."""
    _run_hook_command(
        ["run", "--all-files"],
        "Running pre-commit hooks on all files",
        "All pre-commit hooks passed",
    )
