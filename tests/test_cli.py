"""Tests for the OrganiserPro.cli module."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from OrganiserPro import cli


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """Test the CLI help output."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
    assert "sort" in result.output
    assert "dedupe" in result.output
    assert (
        "sort          Sort files in DIRECTORY by type, date, or size" in result.output
    )
    assert "dedupe        Find and handle duplicate files in DIRECTORY" in result.output


def test_cli_version(runner: CliRunner) -> None:
    """Test the --version flag."""
    from OrganiserPro import __version__
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["--version"])
    assert result.exit_code == 0
    assert (
        f"cli, version {__version__}" in result.output
    )  


def test_cli_no_args_shows_help(runner: CliRunner) -> None:
    """Test that running with no arguments shows help."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, [])
    assert result.exit_code == 0
    assert "FileOrganizer - Organize your files with ease" in result.output
    assert "sort     Sort files in DIRECTORY by type, date, or size" in result.output
    assert "dedupe   Find and handle duplicate files in DIRECTORY" in result.output


@patch("OrganiserPro.cli.sort_by_type")
def test_cli_sort_type(mock_sort: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the sort --by type command."""
    # Create a test file
    (temp_dir / "test.txt").write_text("test")

    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["sort", str(temp_dir), "--by", "type"])
    assert result.exit_code == 0
    # The mock should be called with the resolved path
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])


@patch("OrganiserPro.cli.sort_by_date")
def test_cli_sort_date(mock_sort: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the sort --by date command."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["sort", str(temp_dir), "--by", "date"])
    assert result.exit_code == 0
    mock_sort.assert_called_once_with(str(temp_dir), "%Y-%m", False)


@patch("OrganiserPro.cli.sort_by_date")
def test_cli_sort_date_with_format(
    mock_sort: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the sort --by date command with a custom format."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(
        cli_command,
        ["sort", str(temp_dir), "--by", "date", "--date-format", "%Y/%m"],
    )
    assert result.exit_code == 0
    # The mock should be called with the resolved path and date_format as positional arguments
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])
    assert (
        mock_sort.call_args[0][1] == "%Y/%m"
    )  # Check date_format was passed correctlyond positional argument


@patch("OrganiserPro.cli.sort_by_type")
def test_cli_sort_no_args_uses_default(
    mock_sort: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test that sort with no --by option uses the default (type)."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["sort", str(temp_dir)])
    assert result.exit_code == 0
    mock_sort.assert_called_once()
    assert str(Path(temp_dir).resolve()) in str(mock_sort.call_args[0][0])


@patch("OrganiserPro.cli.dedupe", return_value=0)
def test_cli_dedup_dry_run(mock_find: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the dedupe command with --dry-run option."""
    # Create a test file
    (temp_dir / "test.txt").write_text("test")

    # Mock the dedupe function to return some test data
    mock_find.return_value = 0

    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--dry-run"])
    assert result.exit_code == 0
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default is True in CLI
        delete=False,
        move_to=None,
        dry_run=True,
    )


@patch("OrganiserPro.cli.dedupe", return_value=0)
def test_cli_dedup_recursive(mock_find: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the dedupe command with --recursive option."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--recursive"])
    assert result.exit_code == 0
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,
        delete=False,
        move_to=None,
        dry_run=False,
    )


@patch("OrganiserPro.cli.dedupe", return_value=0)
def test_cli_dedup_delete(mock_find: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the dedupe command with --delete option."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--delete"])
    assert result.exit_code == 0
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default is True in CLI
        delete=True,
        move_to=None,
        dry_run=False,
    )


@patch("OrganiserPro.cli.dedupe", return_value=0)
def test_cli_dedup_move_to(
    mock_find: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the dedupe command with --move-to option."""
    # Create a directory to move duplicates to
    move_dir = temp_dir / "duplicates"
    move_dir.mkdir()

    # Set up the mock to return success
    mock_find.return_value = 0

    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--move-to", str(move_dir)])
    assert result.exit_code == 0

    # Check that find_duplicates was called with the correct arguments
    mock_find.assert_called_once_with(
        directory=str(temp_dir),
        recursive=True,  # Default is True in CLI
        delete=False,  # Not deleting, moving instead
        move_to=str(move_dir),
        dry_run=False,
    )


def test_cli_dedup_no_directory_fails(runner: CliRunner) -> None:
    """Test that dedupe command fails when no directory is provided."""
    from OrganiserPro.cli import cli as cli_command
    result = runner.invoke(cli_command, ["dedupe"])
    assert result.exit_code != 0
    assert "Missing argument 'DIRECTORY'" in result.output
