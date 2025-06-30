from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.prompt import Confirm

console = Console()


def get_file_hash(file_path: Path, block_size: int = 65536) -> str:
    """
    Generate a hash for a file to uniquely identify its contents.

    Args:
        file_path: Path to the file
        block_size: Size of chunks to read at once

    Returns:
        str: SHA-256 hash of the file contents
    """
    hasher = sha256()
    try:
        with open(file_path, "rb") as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (IOError, PermissionError) as e:
        console.print(f"[yellow]Warning: Could not read {file_path}: {e}")
        return ""


def find_duplicates(directory: str) -> Dict[str, List[Path]]:
    """
    Find duplicate files in the given directory.

    Args:
        directory: Directory to search for duplicate files

    Returns:
        Dict mapping file hashes to lists of duplicate file paths
    """
    files_by_size: Dict[int, List[Path]] = defaultdict(list)
    files_by_hash: Dict[str, List[Path]] = defaultdict(list)

    # First group files by size (potential duplicates will have same size)
    with Progress() as progress:
        task = progress.add_task("Scanning files...", total=0)

        all_files = list(Path(directory).glob("*"))
        progress.update(task, total=len(all_files))

        for file_path in all_files:
            progress.advance(task)
            if file_path.is_file() and not file_path.name.startswith("."):
                try:
                    file_size = file_path.stat().st_size
                    files_by_size[file_size].append(file_path)
                except (OSError, PermissionError) as e:
                    console.print(f"[yellow]Warning: Could not access {file_path}: {e}")

    # For files with the same size, compare hashes
    with Progress() as progress:
        task = progress.add_task("Checking for duplicates...", total=len(files_by_size))

        for size, files in files_by_size.items():
            progress.advance(task)
            if len(files) > 1:  # Potential duplicates
                for file_path in files:
                    file_hash = get_file_hash(file_path)
                    if file_hash:  # Only add if we could read the file
                        files_by_hash[file_hash].append(file_path)

    # Only keep hashes with multiple files
    return {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}


def handle_duplicates(
    duplicates: Dict[str, List[Path]],
    delete: bool = False,
    move_to: Optional[str] = None,
) -> None:
    """Handle duplicate files by printing, deleting, or moving them.

    Args:
        duplicates: Dictionary mapping file hashes to lists of duplicate files
        delete: If True, delete all but the first file in each duplicate set
        move_to: If provided, move duplicates to this directory instead of deleting
    """
    total_duplicates = sum(
        len(files) - 1 for files in duplicates.values() if len(files) > 1
    )
    if total_duplicates == 0:
        console.print("[green]No duplicate files found![/green]")
        return

    console.print(f"\n[bold]Found {total_duplicates} duplicate files:")

    # Create destination directory if moving files
    if move_to:
        move_to_path = Path(move_to).expanduser().resolve()
        move_to_path.mkdir(parents=True, exist_ok=True)

    for file_hash, files in duplicates.items():
        if len(files) <= 1:
            continue

        console.print(f"\n[bold]Hash:[/] {file_hash[:8]}...")

        # Keep the first file, handle the rest as duplicates
        original = files[0]
        console.print(f"  [green]Keep:[/] {original}")

        for duplicate in files[1:]:
            if delete:
                try:
                    duplicate.unlink()
                    console.print(f"  [red]Deleted:[/] {duplicate}")
                except OSError as e:
                    msg = f"  [yellow]Error deleting {duplicate}: {e}"
                    console.print(msg)
            elif move_to:
                try:
                    target = move_to_path / duplicate.name
                    if target.exists():
                        # Add a suffix if the target already exists
                        suffix = 1
                        while target.exists():
                            target = target.with_stem(f"{duplicate.stem}_{suffix}")
                            suffix += 1
                    duplicate.rename(target)
                    console.print(f"  [yellow]Moved to:[/] {target}")
                except OSError as e:
                    msg = f"  [yellow]Error moving {duplicate}: {e}"
                    console.print(msg)
            else:
                console.print(f"  [yellow]Duplicate:[/] {duplicate}")

    if not delete and not move_to:
        msg = "\n[bold]Note:[/] Use --delete to remove "
        msg += "duplicates or --move-to to move them"
        console.print(msg)


def find_duplicates_cli(directory: str) -> None:
    """CLI interface for finding and handling duplicate files."""
    console = Console()

    if not Confirm.ask(
        "\n[red]WARNING: This will delete duplicate files. Continue?", default=False
    ):
        return

    duplicates = find_duplicates(directory)

    if not duplicates:
        console.print("\n[green]No duplicate files found![/]")
        return

    # Create and display a table of duplicates
    table = Table(title="Duplicate Files")
    table.add_column("Hash", style="cyan")
    table.add_column("Files", style="magenta")

    for file_hash, files in duplicates.items():
        table.add_row(file_hash[:8] + "...", "\n".join(str(f) for f in files))

    console.print(table)

    if Confirm.ask("\nDelete all but the first of each duplicate?", default=False):
        handle_duplicates(duplicates, delete=True)
    elif Confirm.ask("Move duplicates to a different directory?", default=False):
        move_to = click.prompt("Enter destination directory")
        handle_duplicates(duplicates, move_to=move_to)
