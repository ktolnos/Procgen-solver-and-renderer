import abc
import importlib
import logging
import os
from typing import Type, final

BRUHAI_CONFIGURATION_VAR = "BRUHAI_CONFIGURATION"
DEFAULT_BRUHAI_CONFIGURATION = "Default"
BRUHAI_CONFIGURATIONS_MODULE_VAR = "BRUHAI_CONFIGURATIONS_MODULE"
DEFAULT_BRUHAI_CONFIGURATIONS_MODULE = "settings.configurations"


class Configuration(metaclass=abc.ABCMeta):
    LOGGING = {}

    @classmethod
    @final
    def setup(cls) -> Type["Configuration"]:
        found_configurations_by_name = {}

        configurations_module = os.environ.get(BRUHAI_CONFIGURATIONS_MODULE_VAR, DEFAULT_BRUHAI_CONFIGURATIONS_MODULE)
        try:
            module = importlib.import_module(configurations_module)
        except Exception as ex:
            print(f"Cannot import configurations module `{configurations_module}`: {ex}")
            exit(-1)
        for name, value in module.__dict__.items():
            if isinstance(value, type) and issubclass(value, Configuration):
                found_configurations_by_name[name] = value

        configuration_name = os.environ.get(BRUHAI_CONFIGURATION_VAR, DEFAULT_BRUHAI_CONFIGURATION)
        if configuration_name not in found_configurations_by_name:
            print(f"Cannot setup configuration `{configuration_name}`: Configuration does not exists. "
                  f"Found configurations: {list(found_configurations_by_name)}")
            exit(-1)
        configuration = found_configurations_by_name[configuration_name]

        logging.basicConfig(**configuration.LOGGING)

        logger = logging.getLogger(__name__)
        logger.info(f"Running with configuration `{configuration_name}` "
                    f"({configurations_module}.{configuration_name}).")

        return configuration
