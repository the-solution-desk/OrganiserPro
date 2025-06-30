import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .sorter import sort_by_type, sort_by_date
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
        console.print(Panel.fit(
            "[bold blue]FileOrganizer[/] - Organize your files with ease\n\n"
            "[yellow]Usage:[/] fileorganizer [OPTIONS] COMMAND [ARGS]...\n\n"
            "[bold]Commands:[/]\n"
            "  sort     Sort files by type, date, or size\n"
            "  dedupe   Find and remove duplicate files\n"
            "  help     Show this message and exit\n"
            "  version  Show version and exit",
            title="FileOrganizer",
            border_style="blue"
        ))
        console.print("\nRun 'fileorganizer COMMAND --help' for more information on a command.")

# Sort command
@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--by', type=click.Choice(['type', 'date', 'size']), default='type',
              help='Sort files by type (extension), date, or size')
@click.option('--date-format', default='%Y-%m', show_default=True,
              help='Date format for date-based sorting (e.g., %%Y-%%m-%%d for YYYY-MM-DD)')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
def sort(directory: str, by: str, date_format: str, dry_run: bool):
    """Sort files in DIRECTORY by type, date, or size."""
    console.print(f"[bold]Sorting files in:[/] {directory}")
    console.print(f"[bold]Sort by:[/] {by}")
    
    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
    
    try:
        if by == 'type':
            console.print("\n[bold]Sorting files by type...[/]")
            if not dry_run:
                sort_by_type(directory)
            else:
                # Simulate finding files
                from pathlib import Path
                exts = set(p.suffix.lower() for p in Path(directory).iterdir() 
                          if p.is_file() and not p.name.startswith('.'))
                console.print(f"Would create {len(exts)} directories for file types: {', '.join(exts) or 'none'}")
        
        elif by == 'date':
            console.print(f"\n[bold]Sorting files by date (format: {date_format})...[/]")
            if not dry_run:
                sort_by_date(directory, date_format)
            else:
                # Simulate finding files
                from datetime import datetime
                console.print(f"Would group files by date in format: {date_format}")
        
        elif by == 'size':
            console.print("\n[bold]Sorting files by size...[/]")
            if not dry_run:
                console.print("[yellow]Size-based sorting is not yet implemented")
            else:
                console.print("Would sort files into size-based categories")
    
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)

# Dedupe command
@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--recursive/--no-recursive', default=True, help='Search subdirectories recursively')
@click.option('--delete', is_flag=True, help='Delete duplicate files (keeping the oldest)')
@click.option('--move-to', type=click.Path(file_okay=False, resolve_path=True),
              help='Move duplicate files to this directory instead of deleting')
@click.option('--dry-run', is_flag=True, help='Show duplicates without making changes')
def dedupe(directory: str, recursive: bool, delete: bool, move_to: Optional[str], dry_run: bool):
    """Find and handle duplicate files in DIRECTORY."""
    if dry_run:
        console.print("[yellow]Dry run: No changes will be made")
        delete = False
        move_to = None
    
    try:
        find_duplicates_cli(
            directory=directory,
            recursive=recursive,
            delete=delete,
            move_to=move_to
        )
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()