.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts


.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

.PHONY: clean-docs
clean-docs:  ## remove docs build artifacts
	rm -f docs/CHANGELOG.rst
	rm -f docs/expected.rst
	rm -f docs/tree.txt
	rm -f docs/help.txt
	$(MAKE) -C docs clean

.PHONY: lint
lint: ## check style with pylint
	pylint src/changelogdir tests/*.py

.PHONY: test
test: ## run tests quickly with the default Python
	py.test

.PHONY: test-all
test-all: ## run tests on every Python version with tox
	tox

.PHONY: coverage
coverage: ## check code coverage quickly with the default Python
	py.test --cov-report term-missing --cov=src/

.PHONY: docs
docs: clean-docs ## generate Sphinx HTML documentation, including API docs
	changelogdir -o docs/CHANGELOG.rst
	changelogdir -c tests/demo-project/.changelogdirrc -o docs/expected.rst
	cd tests && tree -a demo-project > ../docs/tree.txt
	changelogdir -h > docs/help.txt
	$(MAKE) -C docs html

.PHONY: dist
dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

.PHONY: test-release
test-release: dist  ## package and upload to pypitest
	twine upload -r pypitest dist/*

.PHONY: release
release: dist  ## package and upload a release
	twine upload -r pypi dist/*

.PHONY: install
install: clean ## install the package to the active Python's site-packages
	python setup.py install

.PHONY: develop
develop: clean ## install editable package
	python setup.py develop
