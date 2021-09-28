from pathlib import Path

from config import __version__


class Base:
    VERSION = __version__
    ROOT_DIR = (Path(__file__) / ".." / "..").resolve()


class Test(Base):
    ...
