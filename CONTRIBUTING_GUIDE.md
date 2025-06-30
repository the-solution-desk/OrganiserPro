# Contributing Guide

Thank you for considering contributing to FileOrganizer! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Code Review Process](#code-review-process)
- [Community](#community)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/OrganiserPro.git
   cd OrganiserPro
   ```
3. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
4. **Install the package in development mode** with all dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. **Install pre-commit hooks** to ensure code quality:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/description-of-fix
   ```

2. **Make your changes** following the code style guidelines.

3. **Run tests** to ensure nothing is broken:
   ```bash
   pytest
   ```

4. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "Add feature/fix: brief description of changes"
   ```

5. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

6. **Open a pull request** against the `main` branch.

## Code Style

We use several tools to maintain code quality and style:

- **Black** for code formatting
- **isort** for import sorting
- **Flake8** for linting
- **mypy** for static type checking

These are enforced through pre-commit hooks. You can also run them manually:

```bash
black .
isort .
flake8
mypy .
```

## Testing

We use `pytest` for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=OrganiserPro --cov-report=term-missing

# Run a specific test file
pytest tests/test_module.py

# Run tests in parallel
pytest -n auto
```

## Documentation

We use Sphinx for documentation. To build the documentation locally:

```bash
cd docs
make html
```

The built documentation will be available in `docs/_build/html/`.

## Pull Request Process

1. Ensure any install or build dependencies are updated.
2. Update the README.md with details of changes if needed.
3. Update the CHANGELOG.md with a summary of changes.
4. You may merge the PR once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Any relevant error messages or logs
- Your environment (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please open an issue to discuss your idea before implementing it.

## Code Review Process

1. A maintainer will review your PR and provide feedback.
2. You may be asked to make changes or provide additional information.
3. Once approved, a maintainer will merge your PR.

## Community

Join our community on [Discord/Slack/other platform] to ask questions and discuss ideas.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
