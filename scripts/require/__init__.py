"""Install development and package dependencies (``python run require``)."""

from argparse import ArgumentParser

from .core import install_dev_dependencies, install_packages, main, require

__all__ = [
    "install_dev_dependencies",
    "install_packages",
    "main",
    "require",
    "setup_commands",
]


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for installing dependencies."""
    require_parser = parser.add_parser(
        "require",
        help="Install development and monorepo package dependencies",
    )
    require_parser.add_argument(
        "package",
        nargs="?",
        help="Specific package (leave empty for all monorepo packages)",
    )
    require_parser.add_argument(
        "--dev-only",
        action="store_true",
        help="Install development dependencies only",
    )
