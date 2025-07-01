import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .dedupe import find_duplicates, find_duplicates_cli
from .sorter import sort_by_type as sort_by_type_impl, sort_by_date as sort_by_date_impl

# Initialize console for rich output
console = Console()
VERSION = "0.1.0"

# Create the main CLI group
@click.group(
    name="organiserpro",
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
        click.echo("  sort-by-type    Sort files in DIRECTORY by file type")
        click.echo("  sort-by-date    Sort files in DIRECTORY by date")
        click.echo("  dedupe          Find and handle duplicate files in DIRECTORY")
        click.echo("\nUse 'organiserpro COMMAND --help' for more information about a command.")
        ctx.exit(0)

# Import and register commands directly
from .commands import sort_by_type, sort_by_date, dedupe

# Register all commands with the main CLI
cli.add_command(sort_by_type)
cli.add_command(sort_by_date)
cli.add_command(dedupe)

# Keep these functions for backward compatibility with tests
def sort_by_type_cmd(directory: str, dry_run: bool = False) -> int:
    """Legacy function for sort by type functionality."""
    from .commands import sort_by_type
    return sort_by_type.callback(directory, dry_run=dry_run)


def sort_by_date_cmd(directory: str, date_format: str, dry_run: bool = False) -> int:
    """Legacy function for sort by date functionality."""
    from .commands import sort_by_date
    return sort_by_date.callback(directory, date_format=date_format, dry_run=dry_run)


def sort_by_size_cmd(directory: str, dry_run: bool = False) -> int:
    """Legacy function for sort by size functionality."""
    from .commands import sort_by_size
    return sort_by_size.callback(directory, dry_run=dry_run)
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


# Legacy function for backwards compatibility with tests
def dedupe_cmd(directory: str, recursive: bool = True, delete: bool = False, 
              move_to: Optional[str] = None, dry_run: bool = False) -> int:
    """Legacy function for dedupe command."""
    from .commands import dedupe as dedupe_func
    return dedupe_func(
        target_dir=directory,
        recursive=recursive,
        delete=delete,
        move_to=move_to,
        dry_run=dry_run
    )


if __name__ == "__main__":
    cli()
