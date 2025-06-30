# Troubleshooting Guide

This guide provides solutions to common issues you might encounter while using FileOrganizer.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Permission Issues](#permission-issues)
- [Performance Issues](#performance-issues)
- [Common Errors](#common-errors)
- [Getting Help](#getting-help)

## Installation Issues

### Error: "Command not found: OrganiserPro"

**Symptoms**: After installation, the `OrganiserPro` command is not recognized.

**Solution**:

1. Ensure the Python scripts directory is in your system's PATH

2. Try reinstalling with:

   ```bash
   pip uninstall OrganiserPro
   pip install -e .
   ```

3. On Linux/macOS, you might need to add `~/.local/bin` to your PATH:

   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Package Installation Fails

**Symptoms**: Errors during package installation.

**Solution**:

1. Ensure you have the latest pip:

   ```bash
   pip install --upgrade pip
   ```

2. Install build dependencies:

   ```bash
   # On Debian/Ubuntu
   sudo apt-get install python3-dev python3-pip
   ```

## Permission Issues

### "Permission Denied" Errors

**Symptoms**: Errors when accessing files or directories.

**Solution**:

1. Ensure you have the necessary permissions to access the files or directories.
2. Use `sudo` if you need elevated privileges.
3. Check the file permissions with `ls -l` and adjust them with `chmod` if needed.

## Performance Issues

### Slow Performance with Large Directories

**Symptoms**: The application is slow when processing large directories.

**Solution**:

1. Use the `--workers` option to increase the number of worker processes.
2. Consider processing smaller batches of files at a time.
3. Close other resource-intensive applications.

## Common Errors

### Module Not Found Error

**Symptoms**: Errors about missing modules.

**Solution**:

1. Ensure all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. If you're in a virtual environment, make sure it's activated.

## Getting Help

If you encounter an issue not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/the-solution-desk/OrganiserPro/issues) for similar problems.
2. Open a new issue with details about your problem, including:
   - The exact command you ran
   - The full error message
   - Your operating system and Python version
   - Steps to reproduce the issue
