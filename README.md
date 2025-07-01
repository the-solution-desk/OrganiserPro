# 🗂️ OrganiserPro

[![PyPI version](https://img.shields.io/pypi/v/organiserpro.svg)](https://pypi.org/project/organiserpro/)
[![Python 3.8–3.13](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://pypi.org/project/organiserpro/)
[![Tests](https://github.com/the-solution-desk/OrganiserPro/actions/workflows/ci.yml/badge.svg)](https://github.com/the-solution-desk/OrganiserPro/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/the-solution-desk/OrganiserPro/branch/main/graph/badge.svg)](https://codecov.io/gh/the-solution-desk/OrganiserPro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/organiserpro/badge/?version=latest)](https://organiserpro.readthedocs.io/en/latest/?badge=latest)

> **OrganiserPro** is a powerful, cross-platform command-line tool for sorting, deduplicating, and managing your files with ease. Keep your files tidy—sort, organize, and eliminate clutter in seconds.

---

## ✨ Features

- **Smart File Sorting**
  - Sort files by type (extension)
  - Organize by modification or creation date
  - Customizable date formats
  - *Dry-run* mode to preview changes

- **Duplicate Detection**
  - Find duplicate files by content
  - Remove or move duplicates automatically
  - Recursive directory scanning

- **User-Friendly**
  - Beautiful terminal output powered by [`rich`](https://github.com/Textualize/rich)
  - Progress bars for long operations
  - Clear error messages and comprehensive help system

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

```bash
pip install organiserpro
```

### Using a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install organiserpro
```

---

## 🛠️ Usage

### Basic Commands

```bash
# Sort files in a directory
organiserpro sort /path/to/directory

# Find and remove duplicates
organiserpro dedupe /path/to/directory

# Get help
organiserpro --help
```

### Examples

```bash
# Sort files by type
organiserpro sort ~/Downloads --by type

# Sort files by date
organiserpro sort ~/Pictures --by date --date-format "%Y-%m"

# Preview actions without making changes (dry run)
organiserpro sort ~/Documents --dry-run
```

---

## 🏁 Quickstart

Sort your Downloads folder by file type:

```bash
organiserpro sort ~/Downloads
```

Remove duplicate files in a folder:

```bash
organiserpro dedupe ~/Pictures
```

Preview actions before making changes:

```bash
organiserpro sort ~/Documents --dry-run
```

See more in the [Documentation](https://organiserpro.readthedocs.io/en/latest/).

---

## 📸 Example Output

```
[16:32:01] Sorting 150 files in /Users/you/Downloads
┣━━ Images (43)
┣━━ Documents (58)
┣━━ Archives (22)
┣━━ Others (27)
✔ All files sorted in 2.3 seconds.
```

---

## 📚 Documentation

For full documentation, advanced usage, and configuration options, visit [Read the Docs](https://organiserpro.readthedocs.io/).

- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

### Development Setup

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```
4. Make your changes and run tests:
   ```bash
   pytest
   ```
5. Commit your changes: `git commit -m "Add some feature"`
6. Push to the branch: `git push origin feature/your-feature`
7. Create a new Pull Request

Please also see our [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For questions or suggestions, please [open an issue](https://github.com/the-solution-desk/organiserpro/issues) or email [opensource@thesolutiondesk.com](mailto:opensource@thesolutiondesk.com).

> **Note for Ubuntu/Debian/Python 3.12+ users:**  
> If you try to install system-wide with pip, you may see an `externally-managed-environment` error due to recent Python packaging changes ([PEP 668](https://peps.python.org/pep-0668/)).  
> Using a virtual environment avoids this problem and keeps your Python setup clean.

For more help, see the [Python packaging user guide](https://packaging.python.org/tutorials/installing-packages/).

---

## 🔗 Quick Links

- [Full Documentation](https://organiserpro.readthedocs.io/en/latest/)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Open an Issue](https://github.com/the-solution-desk/organiserpro/issues)
- [Start a Discussion](https://github.com/the-solution-desk/organiserpro/discussions)

---
