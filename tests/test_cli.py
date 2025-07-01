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
    """Test the --help flag."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
    assert "sort-by-type" in result.output
    assert "sort-by-date" in result.output
    assert "dedupe" in result.output
    assert "dedupe        Find and handle duplicate files in DIRECTORY" in result.output


def test_cli_version(runner: CliRunner) -> None:
    """Test the --version flag."""
    from OrganiserPro import __version__
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["--version"])
    assert result.exit_code == 0
    assert f"organiserpro, version {__version__}" in result.output


def test_cli_no_args_shows_help(runner: CliRunner) -> None:
    """Test that running with no arguments shows help."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, [])
    assert result.exit_code == 0
    assert "FileOrganizer - Organize your files with ease" in result.output
    assert "sort-by-type" in result.output
    assert "sort-by-date" in result.output
    assert "dedupe" in result.output


@patch("OrganiserPro.commands.sort_by_type_impl")
def test_cli_sort_type(mock_sort: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the sort-by-type command."""
    # Create a test file
    (temp_dir / "test.txt").write_text("test")

    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["sort-by-type", str(temp_dir)])
    assert result.exit_code == 0
    # The mock should be called with the resolved path as a keyword argument
    mock_sort.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()), dry_run=False
    )


@patch("OrganiserPro.commands.sort_by_date_impl")
def test_cli_sort_date(mock_sort: MagicMock, runner: CliRunner, temp_dir: Path) -> None:
    """Test the sort-by-date command."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["sort-by-date", str(temp_dir)])
    assert result.exit_code == 0
    # Check that the implementation was called with the correct arguments
    mock_sort.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()), date_format="%Y-%m", dry_run=False
    )


@patch("OrganiserPro.commands.sort_by_date_impl")
def test_cli_sort_date_with_format(
    mock_sort: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the sort-by-date command with a custom format."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(
        cli_command,
        ["sort-by-date", str(temp_dir), "--date-format", "%Y/%m"],
    )
    assert result.exit_code == 0
    # Check that the implementation was called with the correct arguments
    mock_sort.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()), date_format="%Y/%m", dry_run=False
    )


@patch("OrganiserPro.commands.sort_by_type_impl")
def test_cli_sort_no_args_uses_default(
    mock_sort: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test that sort-by-type works with default options."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["sort-by-type", str(temp_dir)])
    assert result.exit_code == 0
    # The mock should be called with the resolved path
    mock_sort.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()), dry_run=False
    )


@patch("OrganiserPro.commands.dedupe", return_value=0)
def test_cli_dedup_dry_run(
    mock_find: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
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


@patch("OrganiserPro.dedupe.find_duplicates_cli")
def test_cli_dedup_recursive(
    mock_dedupe: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the dedupe --recursive flag."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--recursive"])
    assert result.exit_code == 0
    mock_dedupe.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()),
        recursive=True,
        delete=False,
        move_to=None,
        dry_run=False,
    )


@patch("OrganiserPro.dedupe.find_duplicates_cli")
def test_cli_dedup_dry_run(
    mock_dedupe: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the dedupe --dry-run flag."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--dry-run"])
    assert result.exit_code == 0
    # Should not call the actual implementation in dry-run mode
    mock_dedupe.assert_not_called()
    assert "Dry run" in result.output


@patch("OrganiserPro.dedupe.find_duplicates_cli")
def test_cli_dedup_delete(
    mock_dedupe: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the dedupe --delete flag."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["dedupe", str(temp_dir), "--delete"])
    assert result.exit_code == 0
    mock_dedupe.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()),
        recursive=True,  # Default is True
        delete=True,
        move_to=None,
        dry_run=False,
    )


@patch("OrganiserPro.dedupe.find_duplicates_cli")
def test_cli_dedup_move_to(
    mock_dedupe: MagicMock, runner: CliRunner, temp_dir: Path
) -> None:
    """Test the dedupe --move-to flag."""
    # Create a directory to move duplicates to
    move_dir = temp_dir / "duplicates"
    move_dir.mkdir()

    # Set up the mock to return success
    mock_dedupe.return_value = 0

    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(
        cli_command, ["dedupe", str(temp_dir), "--move-to", str(move_dir)]
    )
    assert result.exit_code == 0

    # Check that find_duplicates was called with the correct arguments
    mock_dedupe.assert_called_once_with(
        directory=str(Path(temp_dir).resolve()),
        recursive=True,  # Default is True
        delete=False,
        move_to=str(Path(move_dir).resolve()),
        dry_run=False,
    )


def test_cli_dedup_no_directory_fails(runner: CliRunner) -> None:
    """Test that dedupe with no directory fails."""
    from OrganiserPro.cli import cli as cli_command

    result = runner.invoke(cli_command, ["dedupe"])
    assert result.exit_code != 0
    assert "Missing argument 'TARGET_DIR'" in result.output
