.. _api:

API Reference
============

This document provides detailed information about the FileOrganizer API. It's intended for developers who want to extend or modify the functionality of FileOrganizer.

.. toctree::
   :maxdepth: 2

   modules

Core Modules
-----------

.. automodule:: OrganiserPro.cli
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: OrganiserPro.dedupe
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: OrganiserPro.sorter
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: OrganiserPro.encryptor
   :members:
   :undoc-members:
   :show-inheritance:

Command Line Interface
---------------------

.. click:: OrganiserPro.cli:cli
   :prog: OrganiserPro
   :nested: full
   :show-nested:

Exceptions
----------

.. automodule:: OrganiserPro.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: OrganiserPro.utils
   :members:
   :undoc-members:
   :show-inheritance:
