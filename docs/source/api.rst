.. _api:

API Reference
============

This document provides detailed information about the FileOrganizer API. It's intended for developers who want to extend or modify the functionality of FileOrganizer.

.. toctree::
   :maxdepth: 2

   modules

Core Modules
-----------

.. automodule:: fileorganizer.cli
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: fileorganizer.dedupe
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: fileorganizer.sorter
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: fileorganizer.encryptor
   :members:
   :undoc-members:
   :show-inheritance:

Command Line Interface
---------------------

.. click:: fileorganizer.cli:cli
   :prog: fileorganizer
   :nested: full
   :show-nested:

Exceptions
----------

.. automodule:: fileorganizer.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: fileorganizer.utils
   :members:
   :undoc-members:
   :show-inheritance:
