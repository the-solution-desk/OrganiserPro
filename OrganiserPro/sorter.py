import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, track

console = Console()

def get_file_extension(file_path: Path) -> str:
    """Get the lowercase file extension without the dot, or the full name if no extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: The file extension without the dot, or the full name if no extension,
             or empty string for hidden files
    """
    # Handle hidden files (including those in subdirectories)
    if file_path.name.startswith('.'):
        return ''
    # Handle files with no extension (not hidden)
    if not file_path.suffix:
        return file_path.name
    # Handle normal files with extensions
    return file_path.suffix[1:].lower()

def sort_by_type(directory: str) -> None:
    """
    Sort files in the specified directory into subdirectories based on file extensions.
    
    Args:
        directory: Path to the directory to sort
    """
    source_dir = Path(directory).expanduser().resolve()
    
    # Get all files (excluding hidden files)
    all_files = []
    for file_path in source_dir.glob('*'):  # Only process top-level files
        if file_path.is_file() and not file_path.name.startswith('.'):
            all_files.append(file_path)
    
    if not all_files:
        console.print("[yellow]No files found to sort![/]")
        return
    
    # Create a progress bar
    with Progress() as progress:
        task = progress.add_task("Sorting files...", total=len(all_files))
        files_processed = 0
        extensions_created = set()
        
        for file_path in all_files:
            try:
                # Get file extension and create target directory
                ext = get_file_extension(file_path)
                ext_dir = source_dir / ext
                
                if ext not in extensions_created:
                    ext_dir.mkdir(exist_ok=True)
                    extensions_created.add(ext)
                
                # Create the target path
                target_path = ext_dir / file_path.name
                
                # Handle duplicate filenames by appending a counter
                counter = 1
                original_target = target_path
                while target_path.exists():
                    # If file is the same (same inode), skip it
                    if target_path.samefile(file_path):
                        break
                    # Otherwise, append a counter to make the filename unique
                    new_name = f"{original_target.stem}_{counter}{original_target.suffix}"
                    target_path = original_target.with_name(new_name)
                    counter += 1
                
                # Move the file if it's not already in the right place
                if not target_path.exists() or not target_path.samefile(file_path):
                    shutil.move(str(file_path), str(target_path))
                    files_processed += 1
                
            except Exception as e:
                console.print(f"[red]Error processing {file_path.name}: {e}")
            finally:
                progress.update(task, advance=1)
    
    console.print(f"✅ Sorted {files_processed} files into {len(extensions_created)} directories")

def sort_by_date(directory: str, date_format: str = "%Y-%m") -> None:
    """
    Sort files in the given directory into subdirectories by modification date.
    
    Args:
        directory: Path to the directory containing files to sort
        date_format: Format string for the date-based directory names (e.g., "%Y-%m-%d")
    """
    from datetime import datetime
    import os
    from pathlib import Path
    
    source_dir = Path(directory).expanduser().resolve()
    
    if not source_dir.exists() or not source_dir.is_dir():
        console.print(f"[red]Error: Directory not found: {directory}")
        return
    
    # Get all files (only in the top-level directory, not subdirectories)
    all_files = []
    for file_path in source_dir.glob('*'):
        if file_path.is_file() and not file_path.name.startswith('.'):
            all_files.append(file_path)
    
    if not all_files:
        console.print("[yellow]No files found to sort![/]")
        return
    
    # Create a progress bar
    with Progress() as progress:
        task = progress.add_task("Sorting files by date...", total=len(all_files))
        files_processed = 0
        date_dirs_created = set()
        
        for file_path in all_files:
            try:
                # Get modification time and format it
                mtime = file_path.stat().st_mtime
                date_str = datetime.fromtimestamp(mtime).strftime(date_format)
                
                # Create target directory based on date
                date_dir = source_dir / date_str
                
                # Create all parent directories if they don't exist
                if date_format.count('/') > 0:
                    date_dir.parent.mkdir(parents=True, exist_ok=True)
                
                # Only create the directory if we haven't seen this date yet
                if date_str not in date_dirs_created:
                    date_dir.mkdir(exist_ok=True)
                    date_dirs_created.add(date_str)
                
                # Create the target path
                target_path = date_dir / file_path.name
                
                # Handle duplicate filenames by appending a counter
                counter = 1
                original_target = target_path
                while target_path.exists():
                    # If it's the same file, skip it
                    if target_path.samefile(file_path):
                        break
                    # Otherwise, append a counter to make the filename unique
                    new_name = f"{original_target.stem}_{counter}{original_target.suffix}"
                    target_path = original_target.with_name(new_name)
                    counter += 1
                
                # Move the file if it's not already in the right place
                if not target_path.exists() or not target_path.samefile(file_path):
                    shutil.move(str(file_path), str(target_path))
                    files_processed += 1
                
            except Exception as e:
                console.print(f"[red]Error processing {file_path.name}: {e}")
            finally:
                progress.update(task, advance=1)
    
    console.print(f"✅ Sorted {files_processed} files into {len(date_dirs_created)} date-based directories")