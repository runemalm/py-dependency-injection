##########################################################################
# This is the project's Makefile.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################

HOME := $(shell echo ~)
PWD := $(shell pwd)
SRC := $(PWD)/src
TESTS := $(PWD)/tests
DOCS := $(PWD)/docs

DOCS_PYTHON_VERSION := 3.12.11

# Load env file
include env.make
export $(shell sed 's/=.*//' env.make)

##########################################################################
# MENU
##########################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# TEST
##########################################################################

.PHONY: test
test: ## run test suite
	PYTHONPATH=$(SRC):$(TESTS) pipenv run pytest $(TESTS)

################################################################################
# RELEASE
################################################################################

.PHONY: bump-version
bump-version: ## bump the package version (uses VERSION)
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$(VERSION)\"/" $(SRC)/dependency_injection/_version.py

.PHONY: build
build: ## build the python package
	pipenv run python setup.py sdist bdist_wheel

.PHONY: clean
clean: ## clean the build
	python setup.py clean
	rm -rf build dist
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

.PHONY: upload-test
upload-test: ## upload package to testpypi repository
	TWINE_USERNAME=$(PYPI_USERNAME_TEST) TWINE_PASSWORD=$(PYPI_PASSWORD_TEST) pipenv run twine upload --repository testpypi --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## upload package to pypi repository
	TWINE_USERNAME=$(PYPI_USERNAME) TWINE_PASSWORD=$(PYPI_PASSWORD) pipenv run twine upload --skip-existing dist/*

################################################################################
# DOCS
################################################################################

.PHONY: sphinx-venv-init
sphinx-venv-init: ## Init venv for docs (requires pyenv $(DOCS_PYTHON_VERSION))
	cd $(DOCS) && \
	command -v pyenv >/dev/null || { echo "pyenv not found"; exit 1; } && \
	pyenv versions --bare | grep -q "^$(DOCS_PYTHON_VERSION)$$" || { echo "pyenv $(DOCS_PYTHON_VERSION) not installed"; exit 1; } && \
	PYENV_PYTHON=$$(pyenv root)/versions/$(DOCS_PYTHON_VERSION)/bin/python && \
	$$PYENV_PYTHON -m venv .venv && \
	.venv/bin/pip install --upgrade pip && \
	.venv/bin/pip install -r requirements.txt

.PHONY: sphinx-venv-install
sphinx-venv-install: ## Install or update docs venv from requirements.txt
	cd $(DOCS) && \
	[ -d .venv ] || { echo "Missing .venv — run sphinx-venv-init first."; exit 1; } && \
	.venv/bin/pip install -r requirements.txt

.PHONY: sphinx-venv-rm
sphinx-venv-rm: ## Remove docs venv
	rm -rf $(DOCS)/.venv

.PHONY: sphinx-html
sphinx-html: ## build the sphinx html
	cd $(DOCS) && .venv/bin/sphinx-build -M html . _build

.PHONY: sphinx-rebuild
sphinx-rebuild: ## re-build the sphinx docs
	cd $(DOCS) && \
	.venv/bin/sphinx-build -M clean . _build && \
	.venv/bin/sphinx-build -M html . _build

.PHONY: sphinx-autobuild
sphinx-autobuild: ## activate autobuild of docs
	cd $(DOCS) && \
	.venv/bin/sphinx-autobuild . _build/html --watch $(SRC)

################################################################################
# PRE-COMMIT HOOKS
################################################################################

.PHONY: black
black: ## run black auto-formatting
	pipenv run black $(SRC) $(TESTS)

.PHONY: black-check
black-check: ## check code don't violate black formatting rules
	pipenv run black --check $(SRC)

.PHONY: flake
flake: ## lint code with flake
	pipenv run flake8 --max-line-length=88 $(SRC)

.PHONY: pre-commit-install
pre-commit-install: ## install the pre-commit git hook
	pipenv run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## run the pre-commit hooks
	pipenv run pre-commit run --all-files

################################################################################
# PIPENV
################################################################################

.PHONY: pipenv-rm
pipenv-rm: ## remove the virtual environment
	pipenv --rm

.PHONY: pipenv-install-dev
pipenv-install-dev: ## setup the virtual environment, with dev packages
	pipenv install --dev

.PHONY: pipenv-install-package
pipenv-install-package: ## install a package (uses PACKAGE)
	pipenv install $(PACKAGE)

.PHONY: pipenv-install-dev-package
pipenv-install-dev-package: ## install a dev package (uses PACKAGE)
	pipenv install --dev $(PACKAGE)

.PHONY: pipenv-graph
pipenv-graph: ## Check installed packages
	pipenv graph

.PHONY: pipenv-generate-requirements
pipenv-generate-requirements: ## Check a requirements.txt
	pipenv lock -r > requirements.txt

.PHONY: pipenv-shell
pipenv-shell: ## Activate the virtual environment
	pipenv shell

.PHONY: pipenv-venv
pipenv-venv: ## Show the path to the venv
	pipenv --venv

.PHONY: pipenv-lock-and-install
pipenv-lock-and-install: ## Lock the pipfile and install (after updating Pipfile)
	pipenv lock && \
	pipenv install --dev

.PHONY: pipenv-pip-freeze
pipenv-pip-freeze: ## Run pip freeze in the virtual environment
	pipenv run pip freeze
