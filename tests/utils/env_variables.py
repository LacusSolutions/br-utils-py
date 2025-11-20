import os
import shutil
from pathlib import Path

from dotenv import load_dotenv


def load_test_env() -> None:
    package_root = Path(__file__).parent.parent.parent
    env_file = package_root / ".env.test"
    env_example_file = package_root / ".env.example"

    if not env_file.exists():
        if env_example_file.exists():
            shutil.copy(env_example_file, env_file)
        else:
            print(f'⚠️ Environment file "{env_file}" not found. Skipping...')
            return

    load_dotenv(env_file, override=False)

    with open(env_file) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip()

            if value:
                continue

            system_value = os.getenv(name)

            if system_value:
                os.environ[name] = system_value
