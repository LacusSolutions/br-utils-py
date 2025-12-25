"""Pytest configuration to import directly from source code."""

import sys
from pathlib import Path

package_root = Path(__file__).parent.parent
packages_root = package_root.parent
src_path = package_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

for dep in ["cpf-fmt", "cpf-gen", "cpf-val"]:
    dep_src_path = packages_root / dep / "src"

    if dep_src_path.exists() and str(dep_src_path) not in sys.path:
        sys.path.insert(0, str(dep_src_path))
