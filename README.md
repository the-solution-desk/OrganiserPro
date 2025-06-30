# FileOrganizer

[![PyPI](https://img.shields.io/pypi/v/fileorganizer)](https://pypi.org/project/fileorganizer/)
[![Python Version](https://img.shields.io/pypi/pyversions/fileorganizer)](https://www.python.org/downloads/)
[![Tests](https://github.com/the-solution-desk/fileorganizer/actions/workflows/ci.yml/badge.svg)](https://github.com/the-solution-desk/fileorganizer/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/the-solution-desk/fileorganizer/branch/main/graph/badge.svg)](https://codecov.io/gh/the-solution-desk/fileorganizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/fileorganizer/badge/?version=latest)](https://fileorganizer.readthedocs.io/en/latest/?badge=latest)

A powerful, cross-platform command-line tool for organizing, deduplicating, and managing files with ease. FileOrganizer helps you keep your files tidy by sorting them into logical directories, finding and removing duplicates, and more.

## ✨ Features

- **Smart File Sorting**
  - Sort files by type (extension)
  - Organize by modification/creation date
  - Customizable date formats
  - Dry-run mode to preview changes

- **Duplicate Detection**
  - Find duplicate files by content
  - Remove duplicates automatically
  - Move duplicates to a separate directory
  - Recursive directory scanning

- **User-Friendly**
  - Beautiful terminal output with `rich`
  - Progress bars for long operations
  - Clear error messages
  - Comprehensive help system

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Using pip (Recommended)

```bash
pip install fileorganizer
```

### Development Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/the-solution-desk/fileorganizer.git
   cd fileorganizer
   ```

2. Set up a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode with all dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

### Verifying Installation

```bash
fileorganizer --version
```

## 🛠️ Usage

### Sort files by type (extension)

```bash
fileorganizer sort /path/to/directory --by type
```

### Sort files by date (group by year-month)

```bash
fileorganizer sort /path/to/directory --by date --date-format "%Y-%m"
```

### Find duplicate files (dry run)

```bash
fileorganizer dedupe /path/to/directory --dry-run
```

### Remove duplicate files (keeping the oldest copy)

```bash
fileorganizer dedupe /path/to/directory --delete
```

### Move duplicates to a different directory

```bash
fileorganizer dedupe /path/to/directory --move-to /path/to/duplicates
```

## 📝 Examples

### Example 1: Organize your Downloads folder

```bash
# Sort files by type
fileorganizer sort ~/Downloads --by type

# Then find and remove duplicates
fileorganizer dedupe ~/Downloads --delete
```

### Example 2: Organize photos by year and month

```bash
fileorganizer sort ~/Pictures/Photos --by date --date-format "%Y/%m"
```

## 🧪 Running Tests

### Install test dependencies

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest -v
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Credits

- Built with ❤️ by [Amber Boudreau](https://github.com/the-solution-desk)
- Uses [Click](https://click.palletsprojects.com/) for CLI
- Beautiful output powered by [Rich](https://github.com/Textualize/rich)
