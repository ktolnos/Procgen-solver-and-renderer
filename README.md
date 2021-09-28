# BruhAI

A homemade AGI.

### Before start
* install the latest `poetry` version (https://python-poetry.org)
* install dependencies from .lock file with `poetry install`
* run `pre-commit` to build pre-commit environment

### Run linters
* run all: `pre-commit`
* manually run mypy: `mypy .`
* manually run isort (and fix imports order): `isort .`
* manually run flake8: `flake8 .`

### Add new dependency
* use `poetry add package_name`
* make sure that it's correctly described in `pyproject.toml`
* mypy may ask you to add `types` for newly installed package. Check by running `mypy .`
* if you have conflicting .lock file from another branch - rebuild .lock file with `poetry update`

### Credits
* opryshko.evgeniy@gmail.com - research
* gaponov.daniil@gmail.com - dev, repo maintainer
