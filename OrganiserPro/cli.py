import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .dedupe import find_duplicates, find_duplicates_cli
from .sorter import sort_by_type, sort_by_date


# This function needs to be importable for tests to mock it
def dedupe(directory, recursive=True, delete=False, move_to=None, dry_run=False, **kwargs):
    """Find and handle duplicate files in DIRECTORY."""
    if dry_run:
        console.print(f"[yellow]Dry run: Would search for duplicates in {directory}")
        if recursive:
            console.print("[yellow]Would search recursively")
        if delete:
            console.print("[yellow]Would delete duplicates")
        if move_to:
            console.print(f"[yellow]Would move duplicates to {move_to}")
        return 0
    
    try:
        # Call the actual implementation
        return find_duplicates_cli(
            directory=directory,
            recursive=recursive,
            delete=delete,
            move_to=move_to
        )
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        return 1


console = Console()
VERSION = "0.1.0"


@click.group(
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(version=VERSION, message="%(prog)s, version %(version)s")
@click.pass_context
def cli(ctx):
    """FileOrganizer - Organize your files with ease"""
    if ctx.invoked_subcommand is None:
        click.echo("FileOrganizer - Organize your files with ease")
        click.echo("\nCommands:")
        click.echo("  sort     Sort files in DIRECTORY by type, date, or size")
        click.echo("  dedupe   Find and handle duplicate files in DIRECTORY")
        ctx.exit(0)


# Individual sort commands that the tests expect
@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_type(directory, dry_run):
    """Sort files in DIRECTORY by file type."""
    directory = str(Path(directory).resolve())
    if dry_run:
        exts = set(
            p.suffix.lower()
            for p in Path(directory).iterdir()
            if p.is_file() and not p.name.startswith(".")
        )
        console.print(
            "Would group files by type into folders: "
            f"{', '.join(exts) if exts else 'No files found'}"
        )
        return 0
    sort_by_type_cmd(directory, dry_run)
    return 0


def sort_by_date(directory, date_format="%Y-%m", dry_run=False):
    """Sort files in DIRECTORY by date.
    
    Args:
        directory: The directory to sort files in
        date_format: The date format string (default: "%Y-%m")
        dry_run: If True, only show what would be done
    """
    directory = str(Path(directory).resolve())
    if dry_run:
        console.print(f"Would group files by date in format: {date_format}")
        return 0
    sort_by_date_cmd(directory, date_format, dry_run)
    return 0


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--date-format",
    default="%Y-%m",
    help="Date format for organizing files (e.g., '%%Y-%%m-%%d' or '%%Y/%%m/%%d')",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_date_cmd(directory, date_format, dry_run=False):
    """Sort files in DIRECTORY by date."""
    # Call with positional arguments to match test expectations
    return sort_by_date(directory, date_format, dry_run)


# Keep the original sort command for backward compatibility
@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--by",
    type=click.Choice(["type", "date", "size"]),
    default="type",
    help="Sort files by type (extension), date, or size",
)
@click.option(
    "--date-format",
    default="%Y-%m",
    help="Date format for organizing files (e.g., '%%Y-%%m-%%d' or '%%Y/%%m/%%d')",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort(directory, by, date_format, dry_run):
    """Sort files in DIRECTORY by type, date, or size."""
    directory = str(Path(directory).resolve())

    if by == "type":
        sort_by_type(directory, dry_run=dry_run)
    elif by == "date":
        # Call with positional arguments to match test expectations
        sort_by_date(directory, date_format, dry_run)
    else:  # size
        console.print("Sorting by size is not yet implemented", style="yellow")
        return 1
    return 0


# Keep these functions for backward compatibility with tests
def sort_by_type_cmd(directory: str, dry_run: bool = False):
    """Legacy function for sort by type functionality."""
    if dry_run:
        exts = set(
            p.suffix.lower()
            for p in Path(directory).iterdir()
            if p.is_file() and not p.name.startswith(".")
        )
        console.print(
            "Would group files by type into folders: "
            f"{', '.join(exts) if exts else 'No files found'}"
        )
    else:
        sort_by_type(directory)


def sort_by_date_cmd(directory: str, date_format: str, dry_run: bool = False):
    """Legacy function for sort by date functionality."""
    if dry_run:
        console.print(f"Would group files by date in format: {date_format}")
    else:
        sort_by_date(directory, date_format)


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_size(directory: str, dry_run: bool):
    """Sort files in DIRECTORY by size."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print("[bold]Sort by:[/] size")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
        console.print("Would sort files by size")
    else:
        console.print("Sorting by size is not yet implemented", style="yellow")


def sort_by_size_cmd(directory: str, dry_run: bool = False):
    """Shared implementation of sort by size functionality."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print("[bold]Sort by:[/] size")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
        console.print("Would sort files by size")
    else:
        console.print("Sorting by size is not yet implemented", style="yellow")
        sys.exit(1)


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
)
@click.option(
    "--recursive/--no-recursive",
    default=True,
    help="Search for duplicates in subdirectories (default: recursive on)",
)
@click.option(
    "--delete", is_flag=True, help="Delete duplicate files (keep first occurrence)"
)
@click.option(
    "--move-to",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help="Move duplicate files to this directory",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def dedupe_cmd(directory, recursive, delete, move_to, dry_run):
    """Find and handle duplicate files in DIRECTORY."""
    return dedupe(
        directory=directory,
        recursive=recursive,
        delete=delete,
        move_to=move_to,
        dry_run=dry_run
    )


# Alias for backwards compatibility
dedupe = dedupe_cmd


# Legacy dedupe command implementation (kept for backward compatibility)
def dedupe_cmd(
    directory: str, recursive: bool, delete: bool, move_to: Optional[str], dry_run: bool
) -> int:
    """Legacy function for dedupe command."""
    # Just call the main dedupe function with the same parameters
    return dedupe(directory, recursive, delete, move_to, dry_run)


if __name__ == "__main__":
    cli()
