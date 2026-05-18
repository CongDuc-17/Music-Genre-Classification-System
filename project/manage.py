#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _ensure_tensorflow_env_python():
    desired_python = Path(os.environ.get("GENRELAB_PYTHON", r"D:\CondaEnvs\tensorflow_env\python.exe"))
    if os.environ.get("GENRELAB_SKIP_PYTHON_REEXEC") == "1":
        return
    if not desired_python.is_file():
        return
    if Path(sys.executable).resolve() == desired_python.resolve():
        return

    os.environ["GENRELAB_SKIP_PYTHON_REEXEC"] = "1"
    print(f"Re-running with tensorflow_env Python: {desired_python}")
    os.execv(str(desired_python), [str(desired_python), *sys.argv])


def main():
    _ensure_tensorflow_env_python()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
