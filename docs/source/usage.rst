.. _usage:

Usage
=====

OrganiserPro provides a command-line interface (CLI) for organizing and managing files. This document explains how to use the various commands and options available.

Basic Commands
-------------

To see a list of available commands and options, run:

.. code-block:: bash

   OrganiserPro --help

This will display the main help message with all available commands.

Sorting Files
------------

The ``sort`` command helps you organize files in a directory based on different criteria.

### Sort by File Type

To sort files by their extension:

.. code-block:: bash

   OrganiserPro sort /path/to/directory --by type

This will create subdirectories named after file extensions and move files accordingly.

### Sort by Date

To sort files by their modification date:

.. code-block:: bash

   OrganiserPro sort /path/to/directory --by date

By default, files will be organized in subdirectories named with the format ``YYYY-MM``. You can specify a custom date format:

.. code-block:: bash

   OrganiserPro sort /path/to/directory --by date --date-format "%Y/%m/%d"

### Dry Run

To see what changes would be made without actually moving any files:

.. code-block:: bash

   OrganiserPro sort /path/to/directory --by type --dry-run

Finding and Handling Duplicates
-----------------------------

The ``dedupe`` command helps you find and handle duplicate files.

### Find Duplicates

To find duplicate files in a directory:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory

### Delete Duplicates

To automatically delete duplicate files (keeping the oldest copy):

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --delete

### Move Duplicates

To move duplicate files to a different directory:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --move-to /path/to/duplicates

### Recursive Search

To search for duplicates in subdirectories as well:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --recursive

### Dry Run

To see what duplicates would be found without making any changes:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --dry-run

Common Options
-------------

### Help

Get help for any command:

.. code-block:: bash

   OrganiserPro --help
   OrganiserPro sort --help
   OrganiserPro dedupe --help

### Version

Check the installed version:

.. code-block:: bash

   OrganiserPro --version

Exit Codes
---------

- ``0``: Success
- ``1``: Error or invalid arguments
- ``2``: Runtime error

Examples
--------

Sort files in the current directory by type:

.. code-block:: bash

   OrganiserPro sort . --by type

Find and delete duplicate files in a directory and its subdirectories:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --recursive --delete

Move duplicate files to a separate directory:

.. code-block:: bash

   OrganiserPro dedupe /path/to/directory --move-to /path/to/duplicates

For more detailed information about each command, use the ``--help`` flag with the specific command.
