"""Version management utilities for packages."""

__all__ = ["VersionContext"]

import re
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]


def _find_init_file(pkg_path: Path) -> Path:
    """Resolve the __init__.py path from pyproject.toml's dynamic version attr.

    Reads ``[tool.setuptools.dynamic.version] attr`` (e.g. ``lacus.utils.__version__``),
    strips the trailing ``.__version__``, converts dots to path separators, and
    returns ``<pkg_path>/src/<module/path>/__init__.py``.
    """
    pyproject = pkg_path / "pyproject.toml"

    with open(pyproject, "rb") as f:
        data = tomllib.load(f)

    attr = (
        data.get("tool", {})
        .get("setuptools", {})
        .get("dynamic", {})
        .get("version", {})
        .get("attr", "")
    )

    if not attr or not attr.endswith(".__version__"):
        # Fallback: derive from directory name (legacy behaviour)
        module_name = pkg_path.name.replace("-", "_").replace("utilities", "utils")

        return pkg_path / "src" / module_name / "__init__.py"

    module_path = attr[: -len(".__version__")].replace(".", "/")

    return pkg_path / "src" / module_path / "__init__.py"


class VersionContext:
    """Context manager to temporarily update __version__ and restore it afterwards."""

    def __init__(self, pkg_path: Path, version: str):
        self.pkg_path = pkg_path
        self.version = version
        self.init_file = None
        self.original_content = None

    def __enter__(self):
        """Update the version and save original content."""
        self.init_file = _find_init_file(self.pkg_path)

        if not self.init_file.exists():
            print(f"Error: __init__.py not found at {self.init_file}")
            raise FileNotFoundError(f"__init__.py not found at {self.init_file}")

        try:
            self.original_content = self.init_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error: Failed to read {self.init_file}: {e}")
            raise

        pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'

        if not re.search(pattern, self.original_content):
            print(f"Error: __version__ variable not found in {self.init_file}")
            raise ValueError(f"__version__ variable not found in {self.init_file}")

        new_content = re.sub(
            pattern, f'__version__ = "{self.version}"', self.original_content
        )

        try:
            self.init_file.write_text(new_content, encoding="utf-8")
        except Exception as e:
            print(f"Error: Failed to write {self.init_file}: {e}")
            raise

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore the original content."""
        if self.original_content is not None and self.init_file is not None:
            try:
                self.init_file.write_text(self.original_content, encoding="utf-8")
            except Exception as e:
                print(
                    f"Warning: Failed to restore original content in {self.init_file}: {e}"
                )

        return False  # Don't suppress exceptions
