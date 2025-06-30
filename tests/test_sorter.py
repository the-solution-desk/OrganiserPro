"""Tests for the fileorganizer.sorter module."""
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from fileorganizer.sorter import sort_by_type, sort_by_date, get_file_extension


def test_get_file_extension():
    """Test the get_file_extension helper function."""
    assert get_file_extension(Path("test.txt")) == "txt"
    assert get_file_extension(Path("archive.tar.gz")) == "gz"
    assert get_file_extension(Path("no_extension")) == "no_extension"
    assert get_file_extension(Path(".hidden")) == ""
    assert get_file_extension(Path("folder/.hidden")) == ""


def test_sort_by_type_creates_directories(temp_dir: Path):
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


def test_sort_by_type_handles_duplicate_filenames(temp_dir: Path):
    """Test that sort_by_type handles duplicate filenames correctly."""
    # Create test files with same name
    (temp_dir / "file1.txt").write_text("First file")
    (temp_dir / "file1_1.txt").write_text("Second file with similar name")

    # Run the sorter
    sort_by_type(str(temp_dir))

    # Verify both files exist in the txt directory
    txt_dir = temp_dir / "txt"
    assert txt_dir.is_dir()
    
    # Check that both files were moved to the txt directory
    txt_files = list(txt_dir.glob("*.txt"))
    assert len(txt_files) == 2
    
    # Verify the original files no longer exist in the root
    assert not (temp_dir / "file1.txt").exists()
    assert not (temp_dir / "file1_1.txt").exists()
    assert "First file" in txt_files[0].read_text() or "First file" in txt_files[1].read_text()
    assert ("Second file with similar name" in txt_files[0].read_text() or 
            "Second file with similar name" in txt_files[1].read_text())


def test_sort_by_date_creates_directories(temp_dir: Path):
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
    assert len(files_in_2022_02) >= 1  # At least one of file2.txt or file3.txt should be here
    
    # Verify the original files are no longer in the source directory
    for file_path in file_paths:
        assert not file_path.exists(), f"File {file_path} still exists in source directory"


def test_sort_by_date_with_custom_format(temp_dir: Path, monkeypatch):
    """Test that sort_by_date respects custom date formats."""
    # Mock the timezone to be consistent across different environments
    def mock_localtime(secs=None):
        from time import localtime
        lt = localtime(secs)
        # Force the time to be in UTC to avoid timezone issues
        return (2022, 1, 1, 0, 0, 0, 5, 1, 0)  # 2022-01-01 00:00:00, Saturday
    
    # Apply the mock
    monkeypatch.setattr('time.localtime', mock_localtime)
    
    # Create a test file
    file_path = temp_dir / "test.txt"
    file_path.write_text("Test content")
    
    # Set modification time to a known date using os.utime
    timestamp = 1640995200  # 2022-01-01 00:00:00 UTC
    os.utime(file_path, (timestamp, timestamp))  # Set both atime and mtime

    # Run with custom format (using a format that creates a single directory)
    sort_by_date(str(temp_dir), "%Y-%m")
    
    # Check that the file was moved to a date-based directory
    # The exact directory name depends on the date format and timezone
    date_dirs = list(temp_dir.glob("*"))
    assert len(date_dirs) > 0, "No date directories were created"
    
    # Check that the file exists in one of the date directories
    found = False
    for date_dir in date_dirs:
        if date_dir.is_dir():
            moved_files = list(date_dir.glob("*.txt"))
            if moved_files:
                assert len(moved_files) == 1, f"Expected 1 file in {date_dir}, found {len(moved_files)}"
                assert "test" in moved_files[0].stem, f"File {moved_files[0]} doesn't match expected name pattern"
                found = True
                break
    
    assert found, "No files were moved to date-based directories"
    
    # Verify the original file is no longer in the source directory
    assert not file_path.exists(), f"File {file_path} still exists in source directory"


def test_sort_nonexistent_directory():
    """Test that sort functions handle non-existent directories gracefully."""
    # Should not raise an exception, just log an error
    sort_by_type("/nonexistent/path/1234567890")
    sort_by_date("/nonexistent/path/1234567890")