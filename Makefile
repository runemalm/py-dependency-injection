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
	PYTHONPATH=./src:./tests pytest $(TESTS)

# 	python -m unittest discover -s /Users/david/Projects/py-dependency-injection/tests -p "test_*.py" -t /Users/david/Projects/py-dependency-injection/src

################################################################################
# RELEASE
################################################################################

.PHONY: build
build: ## build the python package
	python setup.py sdist bdist_wheel

.PHONY: clean
clean: ## clean the build
	python setup.py clean
	rm -rf build dist py_dependency_injection.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: upload-test
upload-test: ## upload package to testpypi repository
	twine upload --repository testpypi --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## upload package to pypi repository
	twine upload --skip-existing dist/*

.PHONY: sphinx-quickstart
sphinx-quickstart: ## run the sphinx quickstart
	docker run -it --rm -v $(PWD)/docs:/docs sphinxdoc/sphinx sphinx-quickstart

.PHONY: sphinx-html
sphinx-html: ## build the sphinx html
	make -C docs html

.PHONY: sphinx-rebuild
sphinx-rebuild: ## re-build the sphinx docs
	make -C docs clean && make -C docs html

.PHONY: sphinx-autobuild
sphinx-autobuild: ## activate autobuild of docs
	sphinx-autobuild docs docs/_build/html --watch src

################################################################################
# PIPENV
################################################################################

.PHONY: pipenv-install
pipenv-install: ## install a package (uses PACKAGE)
	pipenv install --dev

.PHONY: pipenv-packages-install
pipenv-packages-install: ## install a package (uses PACKAGE)
	pipenv install $(PACKAGE)

.PHONY: pipenv-packages-install-dev
pipenv-packages-install-dev: ## install a dev package (uses PACKAGE)
	pipenv install --dev $(PACKAGE)

.PHONY: pipenv-packages-graph
pipenv-packages-graph: ## Check installed packages
	pipenv graph

.PHONY: pipenv-requirements-generate
pipenv-requirements-generate: ## Check a requirements.txt
	pipenv lock -r > requirements.txt

.PHONY: pipenv-venv-activate
pipenv-venv-activate: ## Activate the virtual environment
	pipenv shell

.PHONY: pipenv-venv-path
pipenv-venv-path: ## Show the path to the venv
	pipenv --venv

.PHONY: pipenv-lock-and-install
pipenv-lock-and-install: ## Lock the pipfile and install (after updating Pipfile)
	pipenv lock && \
	pipenv install --dev

.PHONY: pipenv-pip-freeze
pipenv-pip-freeze: ## Run pip freeze in the virtual environment
	pipenv run pip freeze

.PHONY: pipenv-setup-sync
pipenv-setup-sync: ## Sync dependencies between Pipfile and setup.py
	pipenv run pipenv-setup sync
