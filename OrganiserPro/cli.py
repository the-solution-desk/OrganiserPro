import sys
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel

from .sorter import sort_by_type as sorter_sort_by_type, sort_by_date as sorter_sort_by_date
from .dedupe import find_duplicates_cli

console = Console()

VERSION = "0.1.0"


# Define the main command group
@click.group(invoke_without_command=True)
@click.version_option(version=VERSION, message="%(prog)s v%(version)s")
@click.pass_context
def cli(ctx):
    """FileOrganizer: Sort, deduplicate, and organize your files with ease."""
    if ctx.invoked_subcommand is None:
        # Show help if no subcommand is provided
        console.print(
            Panel.fit(
                "[bold blue]FileOrganizer[/] - Organize your files with ease\n\n"
                "[yellow]Usage:[/] OrganiserPro [OPTIONS] COMMAND [ARGS]...\n\n"
                "[bold]Commands:[/]\n"
                "  sort     Sort files by type, date, or size\n"
                "  dedupe   Find and remove duplicate files\n"
                "  help     Show this message and exit\n"
                "  version  Show version and exit",
                title="FileOrganizer",
                border_style="blue",
            )
        )
        console.print(
            "\nRun 'OrganiserPro COMMAND --help' for more information on a command."
        )


# Sort command (legacy)
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
    show_default=True,
    help="Date format for date-based sorting (e.g., %%Y-%%m-%%d for YYYY-MM-DD)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort(directory: str, by: str, date_format: str, dry_run: bool):
    """Sort files in DIRECTORY by type, date, or size."""
    if by == "type":
        sort_by_type_cmd(directory, dry_run)
    elif by == "date":
        sort_by_date_cmd(directory, date_format, dry_run)
    else:  # size
        console.print("Sorting by size is not yet implemented", style="red")
        sys.exit(1)


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_type(directory: str, dry_run: bool):
    """Sort files in DIRECTORY by file type (extension)."""
    sort_by_type_cmd(directory, dry_run)


def sort_by_type_cmd(directory: str, dry_run: bool = False):
    """Shared implementation of sort by type functionality."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print("[bold]Sort by:[/] type")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")

    msg = f"[green]Sorting files in {directory} by type...[/green]"
    console.print(msg)
    if not dry_run:
        sorter_sort_by_type(directory)
    else:
        from pathlib import Path
        exts = set(
            p.suffix.lower()
            for p in Path(directory).iterdir()
            if p.is_file() and not p.name.startswith(".")
        )
        msg = f"Would group files by type into folders: "
        msg += f"{', '.join(exts) if exts else 'No files found'}"
        console.print(msg)


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--date-format",
    default="%Y-%m",
    show_default=True,
    help="Date format for date-based sorting (e.g., %%Y-%%m-%%d for YYYY-MM-DD)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def sort_by_date(directory: str, date_format: str, dry_run: bool):
    """Sort files in DIRECTORY by date."""
    sort_by_date_cmd(directory, date_format, dry_run)


def sort_by_date_cmd(directory: str, date_format: str, dry_run: bool = False):
    """Shared implementation of sort by date functionality."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print("[bold]Sort by:[/] date")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")

    console.print(f"\n[bold]Sorting files by date (format: {date_format})...[/]")
    if not dry_run:
        sorter_sort_by_date(directory, date_format)
    else:
        console.print(f"Would group files by date in format: {date_format}")


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


# Dedupe command
@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "--recursive/--no-recursive",
    default=False,
    help="Search for duplicates in subdirectories",
)
@click.option(
    "--delete", is_flag=True, help="Delete duplicate files (keep only one copy)"
)
@click.option(
    "--move-to",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help="Move duplicate files to this directory instead of deleting them",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def dedupe(directory: str, recursive: bool, delete: bool, move_to: Optional[str], dry_run: bool):
    """Find and handle duplicate files in DIRECTORY."""
    dedupe_cmd(directory, recursive, delete, move_to, dry_run)


# Dedupe command (direct implementation)
def dedupe_cmd(directory: str, recursive: bool, delete: bool, 
              move_to: Optional[str], dry_run: bool):
    """Find and handle duplicate files in DIRECTORY."""
    console.print(f"[bold]Searching for duplicate files in:[/] {directory}")

    if recursive:
        console.print("[yellow]Searching recursively in subdirectories")

    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
    elif delete:
        console.print("[red]Will delete duplicate files (keeping one copy)")
    elif move_to:
        console.print(f"[yellow]Will move duplicate files to: {move_to}")

    try:
        # Call the actual deduplication function
        find_duplicates_cli(directory, recursive, delete, move_to, dry_run)
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
