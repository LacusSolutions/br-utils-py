"""Internal script to sync LICENSE file to all packages."""

import shutil

from .common import PACKAGES, PACKAGES_DIR, ROOT_DIR


def sync_license() -> bool:
    """Sync LICENSE file from root to all packages."""
    license_file = ROOT_DIR / "LICENSE"

    if not license_file.exists():
        print(f"Error: LICENSE file not found at {license_file}")
        return False

    print("Syncing LICENSE to all packages...")
    failed = []

    for pkg in PACKAGES:
        pkg_path = PACKAGES_DIR / pkg
        dest_license = pkg_path / "LICENSE"

        try:
            pkg_path.mkdir(parents=True, exist_ok=True)
            shutil.copy2(license_file, dest_license)
            print(f"  ✓ Synced LICENSE to {pkg}/")
        except Exception as e:
            print(f"  ✗ Failed to sync LICENSE to {pkg}/: {e}")
            failed.append(pkg)

    if failed:
        print(f"\n⚠️  Failed to sync LICENSE to: {', '.join(failed)}")
        return False

    print(f"\n✅ Successfully synced LICENSE to all {len(PACKAGES)} packages!")

    return True


if __name__ == "__main__":
    import sys

    sys.exit(0 if sync_license() else 1)
