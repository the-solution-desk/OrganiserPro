# Contributing to FileOrganizer

Thank you for your interest in contributing to FileOrganizer! We welcome contributions from everyone, whether you're a developer, designer, writer, or just someone with a good idea.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Coding Standards](#coding-standards)
- [Git Workflow](#git-workflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Code Review Process](#code-review-process)
- [Reporting Issues](#reporting-issues)
- [Requesting Features](#requesting-features)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

## Ways to Contribute

There are many ways to contribute to FileOrganizer:

- **Code contributions**: Fix bugs, implement new features, or improve existing code
- **Documentation**: Improve documentation, fix typos, or add examples
- **Bug reports**: Report bugs you find while using FileOrganizer
- **Feature requests**: Suggest new features or improvements
- **Testing**: Help test the software and report issues
- **Community**: Help answer questions on issue trackers or forums
- **Localization**: Help translate the project into other languages

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/your-username/fileorganizer.git
   cd fileorganizer
   ```

3. **Add the upstream remote** to keep your fork in sync:

   ```bash
   git remote add upstream https://github.com/the-solution-desk/fileorganizer.git
   ```

4. **Sync your fork** with the upstream repository:

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

## Development Environment Setup

1. **Create and activate a virtual environment** (recommended):

   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install the package in development mode** with all dependencies:

   ```bash
   pip install -e .[dev]
   ```

3. **Install pre-commit hooks** to ensure code quality:

   ```bash
   pre-commit install
   ```

4. **Create a new branch** for your changes:

   ```bash
   git checkout -b feat/your-feature-name  # or fix/your-bugfix-name
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for all functions and methods
- Write docstrings for all public functions, classes, and modules
- Keep lines under 88 characters (Black's default line length)
- Write tests for new features and bug fixes
- Document all new features and changes
- Use absolute imports
- Follow the existing code style and patterns

## Git Workflow

1. **Always work on a branch** - Never commit directly to `main`
2. **Keep your branch up to date** with the latest changes from `main`
3. **Write meaningful commit messages** (see below)
4. **Keep commits small and focused** - One logical change per commit
5. **Rebase your branch** before creating a pull request:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

### Examples:

```
feat: add support for sorting by file size

Add a new feature to sort files by their size in bytes. This allows users to
organize their files by size ranges.

Closes #123
```

```
fix(cli): handle empty directories in dedupe command

Fix a bug where the dedupe command would fail when encountering empty
directories. Now it skips empty directories with a warning message.

Fixes #45
```

### Emoji Cheatsheet (optional):

- :bug: `:bug:` - Bug fixes
- :sparkles: `:sparkles:` - New features
- :memo: `:memo:` - Documentation updates
- :art: `:art:` - Code style/format improvements
- :zap: `:zap:` - Performance improvements
- :white_check_mark: `:white_check_mark:` - Adding tests
- :wrench: `:wrench:` - Configuration changes
- :recycle: `:recycle:` - Refactoring
- :fire: `:fire:` - Removing code/files
- :lock: `:lock:` - Security fixes
- :arrow_up: `:arrow_up:` - Upgrading dependencies
- :arrow_down: `:arrow_down:` - Downgrading dependencies

## Testing

We use [pytest](https://docs.pytest.org/) for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=fileorganizer --cov-report=term-missing

# Run a specific test file
pytest tests/test_something.py -v

# Run a specific test function
pytest tests/test_something.py::test_function_name -v

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- Write tests for all new features and bug fixes
- Keep tests focused and independent
- Use descriptive test function names
- Test edge cases and error conditions
- Use fixtures for common test data
- Mock external dependencies

## Documentation

We use [Sphinx](https://www.sphinx-doc.org/) for documentation. To build the documentation:

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build the documentation
cd docs
make html

# Open the documentation in your browser
open _build/html/index.html  # On macOS
start _build/html/index.html  # On Windows
```

### Writing Documentation

- Keep documentation up to date with code changes
- Write clear and concise docstrings
- Use NumPy or Google style docstrings consistently
- Include examples in docstrings
- Document all public APIs
- Keep README.md up to date
- Update CHANGELOG.md for user-facing changes

## Code Review Process

1. **Create a pull request (PR)** with your changes
   - Reference any related issues
   - Update documentation as needed
   - Ensure all tests pass
   - Keep PRs focused and reasonably sized

2. **Request review** from maintainers
   - Use @mentions if specific feedback is needed
   - Be responsive to review comments

3. **Address feedback** and update your PR
   - Make additional commits for review rounds
   - Squash commits before final merge
   - Update documentation if needed

4. **Once approved**, a maintainer will merge your PR

## Reporting Issues

When reporting issues, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Environment details (OS, Python version, etc.)
5. Any relevant error messages or logs
6. If possible, include a minimal reproducible example

## Requesting Features

When requesting new features, please:

1. Describe the problem you're trying to solve
2. Explain why this feature is important
3. Suggest possible implementations (if any)
4. Provide examples of similar features in other projects (if applicable)

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for more information.

## License

By contributing to FileOrganizer, you agree that your contributions will be licensed under the MIT License.
