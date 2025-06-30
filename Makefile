.PHONY: all install install-dev install-test install-docs test test-cov lint format check-format check-lint check-types check clean clean-pyc clean-build clean-test docs build publish help

# Variables
PYTHON = python3
PIP = pip
PYTEST = pytest
FLAKE8 = flake8
BLACK = black
ISORT = isort
MYPY = mypy
SPHINX_BUILD = sphinx-build
SOURCES = fileorganizer tests
PACKAGE = fileorganizer

# Default target
all: install

# Install the package in development mode
install: clean-pyc
	$(PIP) install -e .[dev]
	pre-commit install

# Install development dependencies
install-dev:
	$(PIP) install -r requirements-dev.txt

# Install test dependencies
install-test:
	$(PIP) install -r requirements-test.txt

# Install documentation dependencies
install-docs:
	$(PIP) install -r requirements-docs.txt

# Run tests
test:
	$(PYTEST) -v --cov=$(PACKAGE) --cov-report=term-missing

# Run tests with coverage
test-cov:
	$(PYTEST) -v --cov=$(PACKAGE) --cov-report=html

# Run linter
lint:
	$(FLAKE8) $(SOURCES)

# Format code
format:
	$(BLACK) $(SOURCES)
	$(ISORT) $(SOURCES)

# Check code formatting
check-format:
	$(BLACK) --check $(SOURCES)
	$(ISORT) --check-only $(SOURCES)

# Check code style
check-lint:
	$(FLAKE8) $(SOURCES)

# Run type checking
check-types:
	$(MYPY) $(PACKAGE)

# Run all checks
check: check-format check-lint check-types test

# Build documentation
docs:
	$(SPHINX_BUILD) -b html docs docs/_build/html

# Build source and wheel packages
build: clean
	$(PYTHON) -m build

# Publish package to PyPI
publish: build
	twine upload dist/*

# Clean up build artifacts
clean: clean-build clean-pyc clean-test
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete

# Clean Python file artifacts
clean-pyc:
	@echo "Cleaning Python file artifacts..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*~' -delete
	find . -type f -name '*.swp' -delete

# Clean build artifacts
clean-build:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .eggs/

# Clean test artifacts
clean-test:
	@echo "Cleaning test artifacts..."
	rm -f .coverage
	rm -f .coverage.*
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Show help
help:
	@echo "\nAvailable targets:"
	@echo "  install     Install the package in development mode"
	@echo "  install-dev Install development dependencies"
	@echo "  install-test Install test dependencies"
	@echo "  install-docs Install documentation dependencies"
	@echo "  test        Run tests"
	@echo "  test-cov    Run tests with coverage report"
	@echo "  lint        Run linter"
	@echo "  format      Format code"
	@echo "  check-format Check code formatting"
	@echo "  check-lint  Check code style"
	@echo "  check-types Run type checking"
	@echo "  check       Run all checks"
	@echo "  docs        Build documentation"
	@echo "  build       Build source and wheel packages"
	@echo "  publish     Publish package to PyPI"
	@echo "  clean       Remove all build, test, and Python artifacts"
	@echo "  clean-pyc   Remove Python file artifacts"
	@echo "  clean-build Remove build artifacts"
	@echo "  clean-test  Remove test artifacts"

# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

# Update dependencies
update-deps:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	pre-commit autoupdate
