"""Tests for the OrganiserPro.dedupe module."""

import hashlib
import os
from pathlib import Path
import pytest
from OrganiserPro.dedupe import find_duplicates, handle_duplicates, get_file_hash


def test_get_file_hash(temp_dir: Path) -> None:
    """Test the get_file_hash function with known content."""
    # Create a test file with known content
    test_file = temp_dir / "test.txt"
    test_content = "This is a test file with known content"
    test_file.write_text(test_content)

    # Calculate expected hash
    hasher = hashlib.sha256()
    hasher.update(test_content.encode("utf-8"))
    expected_hash = hasher.hexdigest()

    # Test the function
    assert get_file_hash(test_file) == expected_hash


def test_get_file_hash_nonexistent_file() -> None:
    """Test that get_file_hash handles non-existent files gracefully."""
    assert get_file_hash(Path("/nonexistent/file/path")) == ""


def test_find_duplicates_empty_directory(temp_dir: Path) -> None:
    """Test find_duplicates with an empty directory."""
    assert find_duplicates(str(temp_dir)) == {}


def test_find_duplicates_no_duplicates(temp_dir: Path) -> None:
    """Test find_duplicates with files that have unique content."""
    # Create test files with different content
    (temp_dir / "file1.txt").write_text("Content 1")
    (temp_dir / "file2.txt").write_text("Content 2")

    assert find_duplicates(str(temp_dir)) == {}


def test_find_duplicates_with_duplicates(temp_dir: Path) -> None:
    """Test find_duplicates with duplicate files."""
    # Create test files with duplicate content
    content = "This is a duplicate file"
    (temp_dir / "file1.txt").write_text(content)
    (temp_dir / "file2.txt").write_text(content)

    # Create a different file
    (temp_dir / "file3.txt").write_text("Different content")

    # Find duplicates
    duplicates = find_duplicates(str(temp_dir))

    # Should find one set of duplicates with two files
    assert len(duplicates) == 1
    assert len(list(duplicates.values())[0]) == 2


def test_find_duplicates_recursive(temp_dir: Path) -> None:
    """Test find_duplicates with recursive directory search."""
    # Create test files in subdirectories
    content = "This is a duplicate file"
    (temp_dir / "file1.txt").write_text(content)
    (temp_dir / "subdir").mkdir()
    (temp_dir / "subdir" / "file2.txt").write_text(content)

    # Should find duplicates when recursive=True (default)
    duplicates = find_duplicates(str(temp_dir), recursive=True)
    assert len(duplicates) == 1
    assert len(list(duplicates.values())[0]) == 2

    # Should not find duplicates when recursive=False
    assert find_duplicates(str(temp_dir), recursive=False) == {}


def test_handle_duplicates_dry_run(temp_dir: Path, capsys: pytest.CaptureFixture) -> None:
    """Test handle_duplicates in dry run mode."""
    # Create test files with duplicate content
    content = "Duplicate content"
    files = [temp_dir / "file1.txt", temp_dir / "file2.txt", temp_dir / "file3.txt"]
    for file in files:
        file.write_text(content)

    # Run in dry run mode (no changes)
    duplicates = {"hash1": [files[0], files[1], files[2]]}
    handle_duplicates(duplicates, delete=False, move_to=None)

    # Verify output
    captured = capsys.readouterr()
    output = captured.out
    assert "2 duplicate files in 1 groups" in output
    assert "Note: Use --delete to remove duplicates or --move-to to move them" in output

    # Verify no files were deleted or moved
    assert all(file.exists() for file in files)


def test_handle_duplicates_delete(temp_dir: Path, capsys: pytest.CaptureFixture) -> None:
    """Test handling duplicates with delete option."""
    # Create test files with same content
    file1 = temp_dir / "file1.txt"
    file2 = temp_dir / "file2.txt"
    file1.write_text("test content")
    file2.write_text("test content")

    # Set file1 to be older than file2
    file1_timestamp = 1642204800  # 2022-01-15
    file2_timestamp = 1642291200  # 2022-01-16
    os.utime(file1, (file1_timestamp, file1_timestamp))
    os.utime(file2, (file2_timestamp, file2_timestamp))

    duplicates = {"hash1": [file1, file2]}
    handle_duplicates(duplicates, delete=True)

    # Verify output
    captured = capsys.readouterr()
    assert "deleted" in captured.out.lower()

    # Check that only one file remains
    remaining_files = list(temp_dir.glob("*"))
    assert len(remaining_files) == 1
    assert file1.exists()  # Older file should be kept
    assert not file2.exists()  # Newer file should be deleted


def test_handle_duplicates_move_to(temp_dir: Path) -> None:
    """Test handle_duplicates with move_to directory."""
    # Create test files with duplicate content
    content = "Duplicate content"
    files = [temp_dir / "file1.txt", temp_dir / "file2.txt"]
    for file in files:
        file.write_text(content)

    # Create a destination directory
    dest_dir = temp_dir / "duplicates"

    # Run with move_to
    duplicates = {"hash1": files}  # Both files are duplicates, first one will be kept
    handle_duplicates(duplicates, delete=False, move_to=str(dest_dir))

    # Verify files were moved
    assert files[0].exists()  # First file should remain
    assert not files[1].exists()  # Second file should be moved
    moved_files = list(dest_dir.glob("*"))
    assert len(moved_files) == 1  # One file should be in the destination
    assert moved_files[0].name == "file2.txt"  # The moved file should be file2.txt
