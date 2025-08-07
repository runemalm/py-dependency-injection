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
	PYTHONPATH=$(SRC):$(TESTS) poetry run pytest $(TESTS)

################################################################################
# RELEASE
################################################################################

.PHONY: build
build: ## build the python package
	poetry build

.PHONY: clean
clean: ## clean the build
	rm -rf build dist
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

.PHONY: publish-test
publish-test: ## upload package to test.pypi.org
	poetry publish --repository testpypi

.PHONY: publish
publish: ## upload package to PyPI
	poetry publish

.PHONY: act-feature
act-feature: ## Run release workflow locally with act
	@act push --job unittests -P ubuntu-latest=catthehacker/ubuntu:act-latest

.PHONY: release-test-all
release-test-all: ## Install from TestPyPI and run test on all versions
	@for PY in 3.7 3.8 3.9 3.10 3.11 3.12 3.13; do \
		echo "\n--- Running release-test-version for Python $$PY ---"; \
		make release-test-version PY=$$PY || exit 1; \
	done

.PHONY: release-test-version
release-test-version: ## Install package from TestPyPI and test it. Usage: make release-test-version PY=3.10
	@if [ -z "$(PY)" ]; then \
		echo "❌ PY is required. Usage: make release-test-version PY=3.10"; exit 1; \
	fi
	@echo "\n>>> Installing from TestPyPI with Python $(PY)"
	@PYTHON_BIN=$$(pyenv prefix $(PY))/bin/python; \
	VENV_DIR=.venv-install-test-$(PY); \
	$$PYTHON_BIN -m venv $$VENV_DIR && \
	$$VENV_DIR/bin/pip install --upgrade pip && \
	$$VENV_DIR/bin/pip install --index-url https://test.pypi.org/simple/ \
	                             --extra-index-url https://pypi.org/simple \
	                             py-dependency-injection && \
	$$VENV_DIR/bin/python scripts/test_installed_package.py && \
	rm -rf $$VENV_DIR

.PHONY: sync-version
sync-version: ## Sync version.py to pyproject.toml
	python scripts/sync_version.py

################################################################################
# PRE-COMMIT HOOKS
################################################################################

.PHONY: black
black: ## format code using black
	poetry run black --line-length 88 $(SRC) $(TESTS)

.PHONY: black-check
black-check: ## check code don't violate black formatting rules
	poetry run black --check --line-length 88 $(SRC) $(TESTS)

.PHONY: flake
flake: ## lint code with flake
	poetry run flake8 --max-line-length=88 $(SRC) $(TESTS)

.PHONY: pre-commit-install
pre-commit-install: ## install the pre-commit git hook
	poetry run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## run the pre-commit hooks
	poetry run pre-commit run --all-files

################################################################################
# DOCS
################################################################################

.PHONY: sphinx-venv-init
sphinx-venv-init: ## Init venv for docs
	cd $(DOCS) && \
	command -v pyenv >/dev/null || { echo "pyenv not found"; exit 1; } && \
	pyenv versions --bare | grep -q "^$(DOCS_PYTHON_VERSION)$$" || { echo "pyenv $(DOCS_PYTHON_VERSION) not installed"; exit 1; } && \
	PYENV_PYTHON=$$(pyenv root)/versions/$(DOCS_PYTHON_VERSION)/bin/python && \
	$$PYENV_PYTHON -m venv .venv && \
	.venv/bin/pip install --upgrade pip

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

.PHONY: sphinx-clean
sphinx-clean: ## Remove Sphinx build artifacts
	rm -rf $(DOCS)/_build

.PHONY: sphinx-rebuild
sphinx-rebuild: ## re-build the sphinx docs
	cd $(DOCS) && \
	rm -rf _build/.doctrees && \
	.venv/bin/sphinx-build -M clean . _build && \
	.venv/bin/sphinx-build -M html . _build

.PHONY: sphinx-autobuild
sphinx-autobuild: ## activate autobuild of docs
	cd $(DOCS) && \
	.venv/bin/sphinx-autobuild . _build/html --watch $(SRC)

################################################################################
# POETRY
################################################################################

.PHONY: poetry-install-with-dev
poetry-install-with-dev: ## Install all dependencies including dev group
	poetry install --with dev

.PHONY: poetry-env-remove
poetry-env-remove: ## Remove the Poetry virtual environment
	poetry env info --path >/dev/null 2>&1 && poetry env remove python || echo "No Poetry environment found."

.PHONY: poetry-env-info-path
poetry-env-info-path: ## Show the path to the Poetry virtual environment
	poetry env info --path

.PHONY: poetry-add
poetry-add: ## Install a runtime package (uses PACKAGE)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ PACKAGE is required. Usage: make poetry-add PACKAGE=your-package"; exit 1; \
	fi
	poetry add $(PACKAGE)

.PHONY: poetry-add-dev
poetry-add-dev: ## Install a dev package (uses PACKAGE)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ PACKAGE is required. Usage: make poetry-add-dev PACKAGE=your-package"; exit 1; \
	fi
	poetry add --group dev $(PACKAGE)

.PHONY: poetry-show-tree
poetry-show-tree: ## Show dependency tree
	poetry show --tree

.PHONY: poetry-export-requirements-txt
poetry-export-requirements-txt: ## Export requirements.txt (for Docker or CI)
	poetry export --without-hashes --format=requirements.txt > requirements.txt
