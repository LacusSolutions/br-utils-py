"""Pytest configuration to import directly from source code."""

import sys
from pathlib import Path

package_root = Path(__file__).parent.parent
src_path = package_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
