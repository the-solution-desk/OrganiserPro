import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel

from .sorter import sort_by_type, sort_by_date
from .dedupe import find_duplicates_cli

console = Console()
VERSION = "0.1.0"

# Main command group
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=VERSION, message="%(prog)s v%(version)s")
@click.pass_context
def cli(ctx):
    """FileOrganizer: Sort, deduplicate, and organize your files with ease."""
    if ctx.invoked_subcommand is None:
        # Show help if no subcommand is provided
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command(help="Sort files in DIRECTORY by type, date, or size")
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
)
@click.option(
    "--by",
    type=click.Choice(["type", "date", "size"]),
    default="type",
    show_default=True,
    help="Sort files by type (extension), date, or size",
)
@click.option(
    "--date-format",
    default="%Y-%m",
    show_default=True,
    help="Date format for date-based sorting (e.g., %%Y-%%m-%%d for YYYY-MM-DD)",
)
@click.option(
    "--dry-run", 
    is_flag=True, 
    help="Show what would be done without making changes"
)
def sort(directory: str, by: str, date_format: str, dry_run: bool):
    """Sort files in DIRECTORY by type, date, or size."""
    directory = str(Path(directory).resolve())
    
    if by == "type":
        if dry_run:
            exts = set(
                p.suffix.lower()
                for p in Path(directory).iterdir()
                if p.is_file() and not p.name.startswith(".")
            )
            console.print(f"Would group files by type into folders: {', '.join(exts) if exts else 'No files found'}")
        else:
            sort_by_type(directory)
    elif by == "date":
        if dry_run:
            console.print(f"Would group files by date in format: {date_format}")
        else:
            sort_by_date(directory, date_format)
    else:  # size
        console.print("Sorting by size is not yet implemented", style="yellow")
        sys.exit(1)


# Keep these functions for backward compatibility with tests
def sort_by_type_cmd(directory: str, dry_run: bool = False):
    """Legacy function for sort by type functionality."""
    if dry_run:
        exts = set(
            p.suffix.lower()
            for p in Path(directory).iterdir()
            if p.is_file() and not p.name.startswith(".")
        )
        console.print(f"Would group files by type into folders: {', '.join(exts) if exts else 'No files found'}")
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


@cli.command(help="Find and handle duplicate files in DIRECTORY")
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
)
@click.option(
    "--recursive/--no-recursive",
    default=False,
    help="Search for duplicates in subdirectories",
    show_default=True,
)
@click.option(
    "--delete", 
    is_flag=True, 
    help="Delete duplicate files (keep only one copy)",
)
@click.option(
    "--move-to",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help="Move duplicate files to this directory instead of deleting them",
)
@click.option(
    "--dry-run", 
    is_flag=True, 
    help="Show what would be done without making changes",
)
def dedupe(directory: str, recursive: bool, delete: bool, move_to: Optional[str], dry_run: bool):
    """Find and handle duplicate files in DIRECTORY."""
    directory = str(Path(directory).resolve())
    
    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
    
    if delete and move_to:
        console.print("[red]Error: Cannot use both --delete and --move-to options together")
        sys.exit(1)
    
    try:
        find_duplicates_cli(
            directory=directory,
            recursive=recursive,
            delete=delete,
            move_to=move_to,
            dry_run=dry_run
        )
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)


# Legacy dedupe command implementation
def dedupe_cmd(directory: str, recursive: bool, delete: bool, 
              move_to: Optional[str], dry_run: bool):
    """Legacy function for dedupe command."""
    return dedupe.callback(
        directory=directory,
        recursive=recursive,
        delete=delete,
        move_to=move_to,
        dry_run=dry_run
    )


if __name__ == "__main__":
    cli()
