"""Nox configuration for automated testing and linting."""

import nox
from pathlib import Path

# Default sessions to run when no session is specified
nox.options.sessions = ["tests", "lint", "typecheck"]

# Python versions to test against
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]

# Package directory
PACKAGE = "fileorganizer"

# Files and directories to run linting on
LINT_PATHS = ["fileorganizer", "tests", "noxfile.py", "setup.py"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    session.install("pytest", "pytest-cov", "pytest-xdist")
    session.install(".")
    session.run(
        "pytest",
        "--cov",
        PACKAGE,
        "--cov-report",
        "term-missing",
        "-n",
        "auto",
        "-v",
        *session.posargs,
    )


@nox.session
def lint(session):
    """Run all linters."""
    session.install(
        "black",
        "flake8",
        "flake8-bugbear",
        "isort",
    )
    session.run("black", "--check", *LINT_PATHS)
    session.run("flake8", *LINT_PATHS)
    session.run("isort", "--check-only", *LINT_PATHS)


@nox.session
def typecheck(session):
    """Run static type checking."""
    session.install("mypy", "types-setuptools")
    session.install(".")
    session.run("mypy", PACKAGE)


@nox.session
def format(session):
    """Format code using Black and isort."""
    session.install("black", "isort")
    session.run("isort", *LINT_PATHS)
    session.run("black", *LINT_PATHS)


@nox.session
def docs(session):
    """Build the documentation."""
    session.install("-r", "requirements-docs.txt")
    session.install(".")
    session.chdir("docs")
    session.run(
        "sphinx-build",
        "-b",
        "html",
        ".",
        "_build/html",
        "-W",
        "-n",  # Enable nit-picky mode
    )


@nox.session
def build(session):
    """Build source and wheel distributions."""
    session.install("build", "twine", "check-wheel-contents")
    session.run("python", "-m", "build")
    session.run("twine", "check", "--strict", "dist/*")
    session.run("check-wheel-contents", "dist")


@nox.session(python=False)
def clean(session):
    """Clean up build artifacts and caches."""
    patterns = [
        ".pytest_cache",
        ".mypy_cache",
        "build",
        "dist",
        "*.egg-info",
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        ".coverage",
        "htmlcov",
        ".tox",
        ".nox",
    ]

    for pattern in patterns:
        for path in Path.cwd().rglob(pattern):
            if path.is_dir():
                session.run("rm", "-rf", str(path), external=True)
            else:
                path.unlink()
