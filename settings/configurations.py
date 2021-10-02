import logging
from pathlib import Path

from bruhai.configuration import Configuration
from settings import __version__


class Base(Configuration):
    VERSION = __version__
    ROOT_DIR = (Path(__file__) / ".." / "..").resolve()

    LOGGING = {
        "format": "%(asctime)s %(name)s [%(levelname)s] %(message)s",
        "level": logging.DEBUG,
        "datefmt": "%m/%d/%Y %H:%M:%S",
    }


class Default(Base):
    ...
