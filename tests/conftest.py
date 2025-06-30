"""Pytest configuration and fixtures for OrganiserPro tests."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator, List, Tuple

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing and clean up after."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


def create_test_files(directory: Path, file_list: List[Tuple[str, str]]) -> None:
    """Create test files in the specified directory.

    Args:
        directory: Directory to create files in
        file_list: List of tuples (filename, content)
    """
    for filename, content in file_list:
        file_path = directory / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        # Set modification time to a fixed value for consistent testing
        os.utime(file_path, (1617235200, 1617235200))  # 2021-04-01 00:00:00
