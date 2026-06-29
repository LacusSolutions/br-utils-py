"""Prepare release notes from package CHANGELOG."""

__all__ = [
    "prepare_release_notes",
    "setup_commands",
]

import re
import sys
from argparse import ArgumentParser
from pathlib import Path

try:
    import tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError
except ImportError:
    import tomli as tomllib

    TOMLDecodeError = tomllib.TOMLDecodeError

from .common import PACKAGES, PACKAGES_DIR, ROOT_DIR

VERSION_HEADING_PATTERN = re.compile(
    r"^## (\d+\.\d+\.\d+(?:\.(?:dev|alpha|beta|rc)\d+)?)\s*\r?\n"
    r"(.*?)(?=^## \d+\.\d+\.\d+(?:\.(?:dev|alpha|beta|rc)\d+)?\s*\r?\n|\Z)",
    re.MULTILINE | re.DOTALL,
)
VERSION_FORMAT = re.compile(r"^\d+\.\d+\.\d+(?:\.(?:dev|alpha|beta|rc)\d+)?$")


def setup_commands(parser: ArgumentParser) -> None:
    """Setup CLI arguments for preparing release notes."""
    release_parser = parser.add_parser(
        "release",
        help="Prepare release notes from a package CHANGELOG (developer/CI only)",
    )
    release_parser.add_argument("package", help="Package folder name")
    release_parser.add_argument(
        "--version",
        "-v",
        help="Release version (X.Y.Z or X.Y.Z.{dev,alpha,beta,rc}N)",
    )


def extract_changelog_bodies(markdown: str) -> dict[str, str]:
    """Extract version sections from a package CHANGELOG."""
    bodies: dict[str, str] = {}

    for match in VERSION_HEADING_PATTERN.finditer(markdown):
        bodies[match.group(1)] = match.group(2).rstrip()

    return bodies


def get_pypi_name(package: str) -> str:
    """Read the PyPI distribution name from a package pyproject.toml."""
    pyproject_path = PACKAGES_DIR / package / "pyproject.toml"

    with open(pyproject_path, "rb") as file:
        data = tomllib.load(file)

    name = data.get("project", {}).get("name")

    if not isinstance(name, str) or not name:
        raise ValueError(f"Could not read PyPI package name from {pyproject_path}")

    return name


def prepare_release_notes(package: str, requested_version: str | None = None) -> Path:
    """Write release notes for a package version to .release/."""
    if package not in PACKAGES:
        available = ", ".join(PACKAGES)
        raise ValueError(f"Invalid package: {package}. Available packages: {available}")

    if requested_version is not None and not VERSION_FORMAT.fullmatch(
        requested_version
    ):
        raise ValueError(
            "Invalid version format: "
            f"{requested_version}. Expected X.Y.Z or X.Y.Z.{{dev,alpha,beta,rc}}N"
        )

    changelog_path = PACKAGES_DIR / package / "CHANGELOG.md"

    if not changelog_path.is_file():
        raise FileNotFoundError(f"Changelog not found: {changelog_path}")

    version_bodies = extract_changelog_bodies(
        changelog_path.read_text(encoding="utf-8")
    )

    if not version_bodies:
        raise ValueError(f"No version sections found in changelog: {changelog_path}")

    if requested_version is not None:
        if requested_version not in version_bodies:
            available = ", ".join(version_bodies.keys())
            raise ValueError(
                f"Version not found in changelog: {requested_version}. "
                f"Available versions: {available}"
            )
        version = requested_version
    else:
        version = next(iter(version_bodies))

    release_directory = ROOT_DIR / ".release"
    release_directory.mkdir(parents=True, exist_ok=True)

    output_path = release_directory / f"{package}@{version}.md"
    output_path.write_text(f"{version_bodies[version]}\n", encoding="utf-8")

    return output_path


def main(package: str, requested_version: str | None = None) -> int:
    """CLI entrypoint for preparing release notes."""
    try:
        output_path = prepare_release_notes(package, requested_version)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(output_path)
    return 0
