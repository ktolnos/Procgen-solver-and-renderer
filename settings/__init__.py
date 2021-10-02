from pathlib import Path

import toml


def get_version() -> str:
    path = (Path(__file__) / ".." / ".." / "pyproject.toml").resolve()
    pyproject_toml = toml.load(path)
    return pyproject_toml["tool"]["poetry"]["version"]


__version__ = get_version()
