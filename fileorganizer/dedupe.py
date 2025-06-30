import os
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
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
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (IOError, PermissionError) as e:
        console.print(f"[yellow]Warning: Could not read {file_path}: {e}")
        return ""

def find_duplicates(directory: str, recursive: bool = True) -> Dict[str, List[Path]]:
    """
    Find duplicate files in the specified directory.
    
    Args:
        directory: Directory to search for duplicates
        recursive: Whether to search subdirectories
        
    Returns:
        Dict mapping file hashes to lists of duplicate files
    """
    files_by_size: Dict[int, List[Path]] = {}
    files_by_hash: Dict[str, List[Path]] = {}
    
    # First group files by size (potential duplicates will have same size)
    with Progress() as progress:
        task = progress.add_task("Scanning files...", total=0)
        
        glob_pattern = '**/*' if recursive else '*'
        all_files = list(Path(directory).rglob(glob_pattern) if recursive else Path(directory).glob('*'))
        progress.update(task, total=len(all_files))
        
        for file_path in all_files:
            progress.advance(task)
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    file_size = file_path.stat().st_size
                    files_by_size.setdefault(file_size, []).append(file_path)
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
                        files_by_hash.setdefault(file_hash, []).append(file_path)
    
    # Only keep hashes with multiple files
    return {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}

def handle_duplicates(duplicates: Dict[str, List[Path]], delete: bool = False, move_to: Optional[str] = None) -> None:
    """
    Handle duplicate files by either deleting them or moving them to a specified directory.
    
    Args:
        duplicates: Dictionary mapping file hashes to lists of duplicate files
        delete: If True, delete all but the first file in each duplicate set
        move_to: If provided, move duplicates to this directory instead of deleting
    """
    from rich.table import Table
    from rich.console import Console
    import shutil
    
    console = Console()
    total_duplicates = sum(len(files) - 1 for files in duplicates.values() if len(files) > 1)
    
    if total_duplicates == 0:
        console.print("\n[green]No duplicate files found![/]")
        return
    
    # Prepare the move_to directory if specified
    move_dir = Path(move_to).expanduser().resolve() if move_to else None
    if move_dir and not move_dir.exists():
        move_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(f"\nFound {len(duplicates)} sets of duplicates ({total_duplicates} duplicate files in total)")
    
    moved_count = 0
    deleted_count = 0
    
    for i, (file_hash, files) in enumerate(duplicates.items(), 1):
        if len(files) <= 1:
            continue
            
        # Sort files by modification time (oldest first)
        files.sort(key=lambda f: f.stat().st_mtime)
        
        # Create a table for this set of duplicates
        table = Table(title=f"Duplicate Set {i} ({len(files)} files, {files[0].stat().st_size/1024:.2f} KB each)")
        table.add_column("Keep", justify="center")
        table.add_column("Modified", style="dim")
        table.add_column("Path")
        
        # Keep the first file
        table.add_row("✓", str(datetime.fromtimestamp(files[0].stat().st_mtime)), str(files[0]))
        
        # Process duplicates
        for file_path in files[1:]:
            table.add_row("✗", str(datetime.fromtimestamp(file_path.stat().st_mtime)), str(file_path))
            
            if delete:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    console.print(f"[red]Error deleting {file_path}: {e}[/]")
            elif move_dir:
                try:
                    target = move_dir / file_path.name
                    # Handle filename conflicts
                    counter = 1
                    while target.exists():
                        target = move_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                        counter += 1
                    # Use shutil.move instead of rename to handle cross-device moves
                    shutil.move(str(file_path), str(target))
                    moved_count += 1
                except Exception as e:
                    console.print(f"[red]Error moving {file_path}: {e}[/]")
        
        console.print(table)
    
    # Print summary
    if delete:
        console.print(f"\n[green]✓ Deleted {deleted_count} duplicate files[/]")
    elif move_to:
        console.print(f"\n[green]✓ Moved {moved_count} duplicate files to {move_dir}[/]")
    else:
        console.print("\n[yellow]No action taken (use --delete or --move-to to handle duplicates)[/]")

def find_duplicates_cli(directory: str, recursive: bool = True, delete: bool = False, 
                        move_to: Optional[str] = None) -> None:
    """
    CLI interface for finding and handling duplicate files.
    """
    if delete and move_to:
        console.print("[red]Error: Cannot use both --delete and --move-to")
        return
    
    if delete and not Confirm.ask("\n[red]WARNING: This will delete duplicate files. Continue?", default=False):
        return
    
    duplicates = find_duplicates(directory, recursive)
    handle_duplicates(duplicates, delete, move_to)