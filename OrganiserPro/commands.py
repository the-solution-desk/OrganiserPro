"""CLI command implementations for OrganiserPro."""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .sorter import sort_by_type as sort_by_type_impl, sort_by_date as sort_by_date_impl

console = Console()


@click.command(name="sort-by-type")
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_type(directory: str, dry_run: bool) -> int:
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
    # Call with keyword arguments to match test expectations
    sort_by_type_impl(directory=directory, dry_run=dry_run)
    return 0


@click.command(name="sort-by-date")
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
def sort_by_date(directory: str, date_format: str, dry_run: bool) -> int:
    """Sort files in DIRECTORY by date."""
    directory = str(Path(directory).resolve())
    if dry_run:
        console.print(f"Would group files by date in format: {date_format}")
        return 0
    # Call with keyword arguments to match test expectations
    sort_by_date_impl(directory=directory, date_format=date_format, dry_run=dry_run)
    return 0


@click.command()
@click.argument(
    "target_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
)
@click.option(
    "--recursive/--no-recursive",
    is_flag=True,
    default=True,
    help="Search for duplicates in subdirectories (default: recursive on)",
    show_default=True,
)
@click.option(
    "--delete",
    is_flag=True,
    help="Delete duplicate files (keep first occurrence)",
    default=False,
)
@click.option(
    "--move-to",
    type=click.Path(file_okay=False, dir_okay=True, path_type=str),
    help="Move duplicate files to this directory",
    default=None,
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes",
    default=False,
)
def dedupe(
    target_dir: str,
    recursive: bool,
    delete: bool,
    move_to: Optional[str],
    dry_run: bool,
) -> int:
    """Find and handle duplicate files in DIRECTORY.

    DIRECTORY: The directory to search for duplicate files in.
    """
    try:
        # Resolve the directory path
        resolved_dir = str(Path(target_dir).resolve())

        if dry_run:
            console.print(
                f"[yellow]Dry run: Would search for duplicates in {resolved_dir}"
            )
            console.print("Dry run: No files will be modified")
            return 0

        # Call the deduplication function
        from .dedupe import find_duplicates_cli

        # Call the function with the resolved paths
        find_duplicates_cli(
            directory=resolved_dir,
            recursive=recursive,
            delete=delete,
            move_to=str(Path(move_to).resolve()) if move_to else None,
            dry_run=dry_run,
        )
        return 0  # Success
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        return 1  # Error exit code
