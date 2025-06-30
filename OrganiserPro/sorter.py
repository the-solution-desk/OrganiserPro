import shutil
from datetime import datetime
from pathlib import Path

from rich.console import Console
console = Console()


def get_file_extension(file_path: Path) -> str:
    """Get the file extension without the dot.

    Args:
        file_path: Path to the file

    Returns:
        str: The file extension without the dot, or the full name if no extension,
             or empty string for hidden files
    """
    if file_path.name.startswith("."):
        return ""
    if not file_path.suffix:
        return file_path.name
    return file_path.suffix[1:].lower()


def sort_by_type(directory: str) -> None:
    """Sort files in the given directory into subdirectories by file type.

    Args:
        directory: Path to the directory containing files to sort
    """
    source_dir = Path(directory).expanduser().resolve()

    # Get all files (excluding hidden files)
    all_files = []
    for file_path in source_dir.glob("*"):  # Only process top-level files
        if file_path.is_file() and not file_path.name.startswith("."):
            all_files.append(file_path)

    if not all_files:
        console.print("[yellow]No files found to sort![/]")
        return

    # Create a progress bar
    with console.status("Sorting files..."):
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
                    new_name = (
                        f"{original_target.stem}_{counter}{original_target.suffix}"
                    )
                    target_path = original_target.with_name(new_name)
                    counter += 1

                # Move the file if it's not already in the right place
                if not target_path.exists() or not target_path.samefile(file_path):
                    shutil.move(str(file_path), str(target_path))
                    files_processed += 1

            except Exception as e:
                console.print(f"[red]Error processing {file_path.name}: {e}")

    console.print(
        f"✅ Sorted {files_processed} files into {len(extensions_created)} directories"
    )


def sort_by_date(directory: str, date_format: str = "%Y-%m") -> None:
    """
    Sort files into subdirectories based on file type, size, or date.

    Args:
        directory: Directory to sort
        date_format: Format string for date-based sorting
    """
    source_dir = Path(directory).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        console.print(f"[red]Error: {directory} is not a valid directory")
        return

    # Get all files (only in the top-level directory, not subdirectories)
    all_files = []
    for file_path in source_dir.glob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            all_files.append(file_path)

    if not all_files:
        console.print("[yellow]No files found to sort![/]")
        return

    # Track processed files and created directories
    files_processed = 0
    date_dirs_created = set()

    # Process files with progress
    with console.status("Sorting files..."):
        for file_path in all_files:
            if file_path.is_file() and not file_path.name.startswith("."):
                try:
                    # Get the file's last modified time and format it
                    mtime = file_path.stat().st_mtime
                    dt = datetime.fromtimestamp(mtime)
                    date_str = dt.strftime(
                        date_format.replace("YYYY", "%Y").replace(
                            "MM", "%m"
                        ).replace("DD", "%d")
                    )

                    # Create target directory if it doesn't exist
                    target_dir = source_dir / date_str
                    if date_str not in date_dirs_created:
                        target_dir.mkdir(exist_ok=True)
                        date_dirs_created.add(date_str)

                    target_path = target_dir / file_path.name

                    # Handle filename conflicts
                    counter = 1
                    while target_path.exists():
                        target_path = target_dir / (
                            f"{file_path.stem}_{counter}{file_path.suffix}"
                        )
                        counter += 1

                    # Move the file
                    file_path.rename(target_path)
                    files_processed += 1
                except (OSError, PermissionError) as e:
                    msg = f"[yellow]Warning: Could not process {file_path}: {e}"
                    console.print(msg)
                    continue

    console.print(
        f"✅ Sorted {files_processed} files into "
        f"{len(date_dirs_created)} date-based directories"
    )
