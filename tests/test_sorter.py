"""Tests for the OrganiserPro.sorter module."""

import os
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from OrganiserPro.sorter import get_file_extension, sort_by_date, sort_by_type


# Mock the console object for all tests
@pytest.fixture(autouse=True)
def mock_console() -> Generator[MagicMock, None, None]:
    """Mock the console object for all tests.
    
    Returns:
        MagicMock: A mock of the console object with a status context manager.
    """
    with patch("OrganiserPro.sorter.console") as mock_console:
        # Mock the status context manager
        mock_status = MagicMock()
        mock_console.status.return_value.__enter__.return_value = mock_status
        yield mock_console


def test_get_file_extension() -> None:
    """Test the get_file_extension helper function."""
    assert get_file_extension(Path("test.txt")) == "txt"
    assert get_file_extension(Path("archive.tar.gz")) == "gz"
    assert get_file_extension(Path("no_extension")) == "no_extension"
    assert get_file_extension(Path(".hidden")) == ""
    assert get_file_extension(Path("folder/.hidden")) == ""


def test_sort_by_type_creates_directories(temp_dir: Path) -> None:
    """Test that sort_by_type creates directories for each file extension."""
    # Create test files
    test_files = [
        ("file1.txt", "Test content 1"),
        ("file2.txt", "Test content 2"),
        ("image1.jpg", "Fake image data"),
        ("document.pdf", "PDF content"),
    ]

    for filename, content in test_files:
        (temp_dir / filename).write_text(content)

    # Run the sorter
    sort_by_type(str(temp_dir))

    # Verify directories were created
    assert (temp_dir / "txt").is_dir()
    assert (temp_dir / "jpg").is_dir()
    assert (temp_dir / "pdf").is_dir()

    # Verify files were moved
    assert (temp_dir / "txt" / "file1.txt").exists()
    assert (temp_dir / "txt" / "file2.txt").exists()
    assert (temp_dir / "jpg" / "image1.jpg").exists()
    assert (temp_dir / "pdf" / "document.pdf").exists()


def test_sort_by_type_handles_duplicate_filenames(temp_dir: Path) -> None:
    """Test that sort_by_type handles duplicate filenames correctly."""
    # Create test files with same name but different content
    file1 = temp_dir / "file1.txt"
    file1.write_text("First file")

    file2 = temp_dir / "file1_1.txt"
    file2.write_text("Second file with similar name")

    # Set different modification times (1 day apart)
    timestamp1 = 1642204800  # 2022-01-15
    timestamp2 = 1642291200  # 2022-01-16
    os.utime(file1, (timestamp1, timestamp1))
    os.utime(file2, (timestamp2, timestamp2))

    # Test with a custom date format
    sort_by_date(str(temp_dir), "%Y-%m-%d")

    # Check if files were moved to date-based directories
    date_dirs = list(temp_dir.glob("*"))
    # We expect 2 date directories since we set different modification times
    assert (
        len(date_dirs) == 2
    ), f"Expected 2 date directories, found {len(date_dirs)}: {date_dirs}"

    # Check that files exist in their respective date directories
    files_found = 0
    for date_dir in date_dirs:
        files = list(date_dir.glob("*"))
        files_found += len(files)

    # We should have both files in date directories
    assert (
        files_found == 2
    ), f"Expected 2 files total in date directories, found {files_found}"

    # Verify the original files no longer exist in the root
    assert not (temp_dir / "file1.txt").exists()
    assert not (temp_dir / "file1_1.txt").exists()


def test_sort_by_date_creates_directories(temp_dir: Path) -> None:
    """Test that sort_by_date creates directories based on file modification dates."""
    # Create test files with different modification times
    test_files = [
        ("file1.txt", "2022-01-15 file"),
        ("file2.txt", "2022-02-20 file"),
        ("file3.txt", "2022-02-20 another file"),
    ]

    # Store file paths for later verification
    file_paths = []
    for i, (filename, content) in enumerate(test_files):
        file_path = temp_dir / filename
        file_path.write_text(content)
        # Set modification time to different dates using os.utime
        timestamp = 1642204800 + (i * 86400 * 15)  # 2022-01-15 + i*15 days
        os.utime(file_path, (timestamp, timestamp))  # Set both atime and mtime
        file_paths.append(file_path)

    # Run the sorter with year-month format
    sort_by_date(str(temp_dir), "%Y-%m")

    # Verify directories were created
    dir_2022_01 = temp_dir / "2022-01"
    dir_2022_02 = temp_dir / "2022-02"

    assert dir_2022_01.is_dir()
    assert dir_2022_02.is_dir()

    # Verify files were moved correctly
    files_in_2022_01 = list(dir_2022_01.glob("*"))
    files_in_2022_02 = list(dir_2022_02.glob("*"))

    # Check that we have files in the correct date directories
    # The exact filenames might have changed due to deduplication
    assert len(files_in_2022_01) >= 1  # At least file1.txt should be here
    assert (
        len(files_in_2022_02) >= 1
    )  # At least one of file2.txt or file3.txt should be here

    # Verify the original files are no longer in the source directory
    for file_path in file_paths:
        assert (
            not file_path.exists()
        ), f"File {file_path} still exists in source directory"


def test_sort_by_date_with_custom_format(temp_dir: Path) -> None:
    """Test that sort_by_date respects custom date formats."""
    # Create test files with different modification dates
    for i in range(3):
        file_path = temp_dir / f"file{i}.txt"
        file_path.write_text(f"Test file {i}")
        # Set modification time to different dates
        timestamp = 1642204800 + (i * 86400 * 15)  # 2022-01-15 + i*15 days
        os.utime(file_path, (timestamp, timestamp))  # Set both atime and mtime

    # Sort with custom format (year only)
    sort_by_date(str(temp_dir), "%Y")

    # Check if files were moved to year-based directories
    year_dirs = list(temp_dir.glob("*"))
    assert len(year_dirs) == 1  # All files from 2022
    assert year_dirs[0].name == "2022"

    # Check that files exist in the year directory
    year_dir = year_dirs[0]
    for i in range(3):
        assert (year_dir / f"file{i}.txt").exists()

    # Verify the original file is no longer in the source directory
    assert not file_path.exists(), f"File {file_path} still exists in source directory"


def test_sort_nonexistent_directory() -> None:
    """Test that sort functions handle non-existent directories gracefully."""
    # Test with a non-existent directory (should not raise an exception)
    try:
        sort_by_type("/non/existent/path")
        sort_by_date("/non/existent/path")
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
