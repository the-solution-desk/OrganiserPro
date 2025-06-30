"""
FileOrganizer - A powerful tool for organizing, deduplicating, and managing files.

This package provides a command-line interface for sorting files by type, date, or size,
and for finding and handling duplicate files.
"""

# Version of the fileorganizer package
__version__ = "0.1.0"

from .cli import cli
from .sorter import sort_by_type, sort_by_date
from .dedupe import find_duplicates, find_duplicates_cli, handle_duplicates

__all__ = [
    'cli',
    'sort_by_type',
    'sort_by_date',
    'find_duplicates',
    'find_duplicates_cli',
    'handle_duplicates',
]