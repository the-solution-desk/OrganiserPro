.. _installation:

Installation
============

Prerequisites
------------

- Python 3.7 or higher
- pip (Python package installer)

Installation Methods
-------------------

Using pip (recommended)
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install fileorganizer

From source
^^^^^^^^^^^

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/the-solution-desk/fileorganizer.git
      cd fileorganizer

2. Install in development mode:

   .. code-block:: bash

      pip install -e .[dev]

Verification
-----------

After installation, verify that the installation was successful by running:

.. code-block:: bash

   fileorganizer --version

This should display the installed version of FileOrganizer.

Development Dependencies
-----------------------

For development, install the additional dependencies:

.. code-block:: bash

   pip install -e .[dev]

This will install all the necessary packages for development, testing, and documentation.
