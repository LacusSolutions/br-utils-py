"""Common utilities and constants for monorepo management scripts."""

__all__ = [
    "PACKAGES",
    "PACKAGES_DIR",
    "ROOT_DIR",
    "SCRIPTS_DIR",
    "Spinner",
    "run_command",
]

from pathlib import Path
from subprocess import PIPE, STDOUT, CalledProcessError, run
from threading import Thread
from time import sleep

from .discover import get_sorted_packages

ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"
PACKAGES = get_sorted_packages()
SCRIPTS_DIR = ROOT_DIR / "scripts"


def resolve_path(arg: str) -> Path | None:
    """
    Resolve a path argument to a valid Path object.

    Tries in order:
    1. Check if it's a package name in packages/
    2. Check if it's a relative path from root
    3. Check if it's an absolute path

    Returns Path if valid, None otherwise.
    """
    if arg in PACKAGES:
        pkg_path = PACKAGES_DIR / arg

        if pkg_path.exists():
            return pkg_path

    rel_path = ROOT_DIR / arg

    if rel_path.exists():
        return rel_path

    abs_path = Path(arg)

    if abs_path.is_absolute() and abs_path.exists():
        return abs_path

    return None


class Spinner:
    """Simple spinner animation for long-running operations."""

    def __init__(self, message="Processing"):
        self.message = message
        self.spinner_chars = "|/-\\"
        self.spinner_index = 0
        self.running = False
        self.thread = None
        self.last_length = 0

    def update_message(self, new_message: str):
        """Update the spinner message dynamically."""
        self.message = new_message

    def _spin(self):
        """Run the spinner animation in a separate thread."""
        while self.running:
            char = self.spinner_chars[self.spinner_index]
            current_text = f"{char} {self.message}..."
            current_length = len(current_text)

            if self.last_length > 0:
                print("\r" + " " * self.last_length + "\r", end="", flush=True)

            print(current_text, end="", flush=True)
            self.last_length = current_length
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
            sleep(0.1)

    def __enter__(self):
        """Start the spinner when entering context."""
        self.running = True
        self.thread = Thread(target=self._spin, daemon=True)
        self.thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the spinner when exiting context."""
        self.running = False

        if self.thread:
            self.thread.join(timeout=0.2)

        max_length = max(len(self.message) + 10, 100)
        print("\r" + " " * max_length + "\r", end="", flush=True)


def run_command(cmd, cwd=None, check=True, silent=False, spinner_message=None):
    """
    Run a system command and return the result.

    Args:
        cmd: Command to run
        cwd: Working directory
        check: Whether to raise exception on non-zero return code
        silent: If True, suppress output and return (success, output) tuple.
                If False, print command and return bool.
        spinner_message: Optional message to display with spinner when silent=True.
                         If None and silent=True, no spinner is shown.

    Returns:
        If silent=False: bool indicating success
        If silent=True: tuple[bool, str] of (success, output)
    """
    if silent:
        spinner_context = (
            Spinner(spinner_message) if spinner_message else _null_context()
        )

        try:
            with spinner_context:
                result = run(
                    cmd,
                    cwd=cwd,
                    check=False,
                    stdout=PIPE,
                    stderr=STDOUT,
                    text=True,
                )
                status_code = result.returncode
                output = result.stdout if result.stdout else ""

                return status_code == 0, output
        except Exception as e:
            return False, str(e)
    else:
        cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)

        if "-q" not in cmd_str and "--quiet" not in cmd_str:
            print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")

        try:
            result = run(cmd, cwd=cwd, check=check)

            return result.returncode == 0
        except CalledProcessError:
            return False


class _null_context:
    """Null context manager for when no spinner is needed."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
