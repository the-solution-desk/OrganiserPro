"""Tests for the OrganiserPro.cli module."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import click
import pytest
from click.testing import CliRunner

from OrganiserPro.cli import cli, dedupe
from OrganiserPro.dedupe import find_duplicates_cli as real_find_duplicates_cli


@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_cli_help(runner):
    """Test the CLI help output."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
    assert "sort" in result.output
    assert "dedupe" in result.output
    assert "sort    Sort files in DIRECTORY by type, date, or size" in result.output
    assert "dedupe  Find and handle duplicate files in DIRECTORY" in result.output


def test_cli_version(runner):
    """Test the --version flag."""
    from OrganiserPro import __version__

    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert (
        f"cli, version {__version__}" in result.output
        or f"cli v{__version__}" in result.output
    )


def test_cli_no_args_shows_help(runner):
    """Test that running with no arguments shows help."""
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "FileOrganizer - Organize your files with ease" in result.output
    assert "sort     Sort files by type, date, or size" in result.output


@patch("OrganiserPro.cli.sort_by_type")
def test_cli_sort_type(mock_sort, runner, temp_dir):
    """Test the sort --type command."""
    # Create a test file
    (temp_dir / "test.txt").write_text("test")

    result = runner.invoke(cli, ["sort", str(temp_dir), "--by", "type"])
    assert result.exit_code == 0
    # The mock should be called with the resolved path
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])


@patch("OrganiserPro.cli.sort_by_date")
def test_cli_sort_date(mock_sort, runner, temp_dir):
    """Test the sort --date command."""
    result = runner.invoke(cli, ["sort", str(temp_dir), "--by", "date"])
    assert result.exit_code == 0
    mock_sort.assert_called_once_with(str(temp_dir), "%Y-%m")


@patch("OrganiserPro.cli.sort_by_date")
def test_cli_sort_date_with_format(mock_sort, runner, temp_dir):
    """Test the sort --date command with a custom format."""
    result = runner.invoke(
        cli, ["sort", str(temp_dir), "--by", "date", "--date-format", "%Y/%m"]
    )
    assert result.exit_code == 0
    # The mock should be called with the resolved path and date_format as positional arguments
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])
    assert (
        mock_sort.call_args[0][1] == "%Y/%m"
    )  # date_format is the second positional argument


@patch("OrganiserPro.cli.sort_by_type")
def test_cli_sort_no_args_uses_default(mock_sort, runner, temp_dir):
    """Test that sort with no --by option uses the default (type)."""
    result = runner.invoke(cli, ["sort", str(temp_dir)])
    assert result.exit_code == 0
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])


@patch("OrganiserPro.cli.find_duplicates_cli")
def test_cli_dedupe_dry_run(mock_find, runner, temp_dir):
    """Test the dedupe command with dry run."""
    # Mock the find_duplicates_cli function to return some test data
    mock_find.return_value = {
        "hash1": [str(temp_dir / "file1.txt"), str(temp_dir / "file2.txt")],
        "hash2": [str(temp_dir / "file3.txt")],
    }

    result = runner.invoke(cli, ["dedupe", str(temp_dir), "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run: No changes will be made" in result.output

    # Verify find_duplicates_cli was called with the correct arguments
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default value
        delete=False,  # Overridden by dry-run
        move_to=None,  # Not specified
    )


@patch("OrganiserPro.cli.find_duplicates_cli")
def test_cli_dedupe_recursive(mock_find, runner, temp_dir):
    """Test the dedupe command with recursive search."""
    mock_find.return_value = {}

    result = runner.invoke(cli, ["dedupe", str(temp_dir), "--recursive"])
    assert result.exit_code == 0
    mock_find.assert_called_once_with(
        directory=str(temp_dir), recursive=True, delete=False, move_to=None
    )


@patch("OrganiserPro.cli.find_duplicates_cli")
def test_cli_dedupe_delete(mock_find, runner, temp_dir):
    """Test the dedupe command with delete option."""
    mock_find.return_value = {}

    result = runner.invoke(cli, ["dedupe", str(temp_dir), "--delete"])
    assert result.exit_code == 0
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default value
        delete=True,  # Set by --delete
        move_to=None,  # Not specified
    )


@patch("OrganiserPro.cli.find_duplicates_cli")
def test_cli_dedupe_move_to(mock_find, runner, temp_dir):
    """Test the dedupe command with move-to option."""
    mock_find.return_value = {}

    # Create a directory to move duplicates to
    move_dir = temp_dir / "duplicates"
    move_dir.mkdir()

    result = runner.invoke(cli, ["dedupe", str(temp_dir), "--move-to", str(move_dir)])
    assert result.exit_code == 0

    # Check that find_duplicates_cli was called with move_to set
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default value
        delete=False,  # Not deleting, moving instead
        move_to=str(move_dir),
    )


def test_cli_dedupe_no_directory_fails(runner):
    """Test that dedupe with no directory fails."""
    result = runner.invoke(cli, ["dedupe"])
    assert result.exit_code != 0
    assert "Error: Missing argument 'DIRECTORY'" in result.output
