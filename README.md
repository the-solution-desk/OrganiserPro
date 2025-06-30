# OrganiserPro

[![PyPI](https://img.shields.io/pypi/v/organiserpro)](https://pypi.org/project/organiserpro/)
[![Python Version](https://img.shields.io/pypi/pyversions/organiserpro)](https://www.python.org/downloads/)
[![Tests](https://github.com/the-solution-desk/organiserpro/actions/workflows/ci.yml/badge.svg)](https://github.com/the-solution-desk/organiserpro/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/the-solution-desk/organiserpro/branch/main/graph/badge.svg)](https://codecov.io/gh/the-solution-desk/organiserpro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
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
  - Beautiful terminal output powered by `rich`
  - Progress bars for long operations
  - Clear error messages and comprehensive help system

---

## 🚀 Installation

**Prerequisites:**  
- Python 3.7 or higher  
- [pip](https://pip.pypa.io/en/stable/) (Python package manager)

**The recommended way to install OrganiserPro is in a virtual environment.**

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv organiserpro-env
source organiserpro-env/bin/activate  # On Windows use: organiserpro-env\Scripts\activate

# Install OrganiserPro from PyPI
pip install organiserpro
```

> **Note for Ubuntu/Debian/Python 3.12+ users:**  
> If you try to install system-wide with pip, you may see an `externally-managed-environment` error due to recent changes in Python packaging (PEP 668).  
> Using a virtual environment avoids this problem and keeps your Python setup clean.

For more help, see the [Python packaging user guide](https://packaging.python.org/tutorials/installing-packages/).

---

## 🏁 Quickstart

Sort your Downloads folder by file type:

```bash
organiserpro sort --directory ~/Downloads
```

Remove duplicate files in a folder:

```bash
organiserpro deduplicate --directory ~/Pictures
```

*Preview actions before making changes:*

```bash
organiserpro sort --directory ~/Documents --dry-run
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

- [Full Documentation](https://organiserpro.readthedocs.io/en/latest/)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

---

## 🤝 Contributing

We love contributions! Please see our [Contributing Guide](CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md), and [Security Policy](SECURITY.md).

---

## 🛡 License

[MIT License](LICENSE) © [The Solution Desk](https://github.com/the-solution-desk)

---

## 💬 Need Help?

- Open an [issue](https://github.com/the-solution-desk/organiserpro/issues)
- Join the discussion or reach out via [Discussions](https://github.com/the-solution-desk/organiserpro/discussions)

---
