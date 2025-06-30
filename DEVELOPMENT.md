# Development Guide

This guide provides instructions for setting up a development environment for FileOrganizer.

## Prerequisites

- Python 3.7 or higher
- Git
- pip (Python package installer)

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/fileorganizer.git
   cd fileorganizer
   ```

3. **Set up a virtual environment** (recommended):
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install the package in development mode** with all dependencies:
   ```bash
   pip install -e .[dev]
   ```

5. **Install pre-commit hooks** to ensure code quality:
   ```bash
   pre-commit install
   ```

## Running Tests

Run the test suite using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=fileorganizer --cov-report=term-missing

# Run a specific test file
pytest tests/test_module.py

# Run a specific test function
pytest tests/test_module.py::test_function_name
```

## Code Style

We use several tools to maintain code quality and style:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for static type checking

Run these tools manually with:

```bash
# Format code with Black
black fileorganizer tests

# Sort imports with isort
isort fileorganizer tests

# Check code style with flake8
flake8 fileorganizer tests

# Check types with mypy
mypy fileorganizer
```

## Building Documentation

To build the documentation locally:

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build the documentation
cd docs
make html

# View the documentation
open _build/html/index.html  # On macOS
start _build/html/index.html  # On Windows
```

## Pre-commit Hooks

We use pre-commit hooks to automatically run code quality checks before each commit. These hooks are automatically installed when you run `pre-commit install`.

To run the pre-commit hooks manually:

```bash
pre-commit run --all-files
```

## Debugging

For debugging, you can use Python's built-in `pdb` or `ipdb` for a more feature-rich debugger:

```python
import ipdb; ipdb.set_trace()  # Add this line where you want to set a breakpoint
```

## Testing with Different Python Versions

We support Python 3.7+. To test with different Python versions, you can use `tox`:

```bash
pip install tox

tox  # Run tests against all configured Python versions
tox -e py39  # Run tests against Python 3.9 only
```

## Building Distribution Packages

To build source distribution and wheel packages:

```bash
pip install --upgrade build
python -m build
```

This will create `dist/` directory with the distribution packages.

## Submitting Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with a descriptive message:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a pull request against the `main` branch.

## Code Review Process

1. Ensure all tests pass
2. Update documentation as needed
3. Follow the code style guidelines
4. Add tests for new features
5. Update the changelog if necessary

## Profiling

For performance profiling, you can use `cProfile`:

```bash
python -m cProfile -o profile.stats path/to/script.py
```

And analyze the results with `snakeviz`:

```bash
pip install snakeviz
snakeviz profile.stats
```

## Common Tasks

### Update Dependencies

To update dependencies:

1. Update `setup.py` with new versions
2. Update `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```
3. Test the changes
4. Update documentation if needed

### Release a New Version

See [MAINTAINERS.md](MAINTAINERS.md) for detailed release instructions.

## Getting Help

If you need help with development:

1. Check the [documentation](https://fileorganizer.readthedocs.io/)
2. Search the [issue tracker](https://github.com/the-solution-desk/fileorganizer/issues)
3. Open a new issue if your question hasn't been answered
