.. _contributing:

Contributing to FileOrganizer
============================

Thank you for your interest in contributing to FileOrganizer! We welcome contributions from everyone, whether you're a developer, designer, writer, or just someone with a good idea.

Ways to Contribute
-----------------

There are many ways to contribute to FileOrganizer:

- **Code contributions**: Fix bugs, implement new features, or improve existing code
- **Documentation**: Improve documentation, fix typos, or add examples
- **Bug reports**: Report bugs you find while using FileOrganizer
- **Feature requests**: Suggest new features or improvements
- **Testing**: Help test the software and report issues
- **Community**: Help answer questions on issue trackers or forums

Getting Started
--------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   .. code-block:: bash

      git clone https://github.com/your-username/fileorganizer.git
      cd fileorganizer

3. **Set up the development environment**:

   .. code-block:: bash

      # Create and activate a virtual environment (recommended)
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

      # Install the package in development mode with all dependencies
      pip install -e .[dev]

4. **Create a new branch** for your changes:

   .. code-block:: bash

      git checkout -b your-feature-branch

5. **Make your changes** and ensure tests pass:

   .. code-block:: bash

      # Run tests
      pytest

      # Check code style
      black fileorganizer tests
      isort fileorganizer tests
      flake8 fileorganizer tests

6. **Commit your changes** with a clear message:

   .. code-block:: bash

      git commit -m "Add your commit message here"

7. **Push to your fork** and submit a pull request

Coding Standards
---------------

- Follow `PEP 8`_ style guidelines
- Use type hints for all functions and methods
- Write docstrings for all public functions, classes, and modules
- Keep lines under 88 characters (Black's default line length)
- Write tests for new features and bug fixes
- Document all new features and changes

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/

Commit Message Guidelines
-----------------------

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - :bug: `:bug:` when fixing a bug
  - :sparkles: `:sparkles:` when adding a new feature
  - :memo: `:memo:` when writing docs
  - :art: `:art:` when improving the format/structure
  - :zap: `:zap:` when improving performance
  - :white_check_mark: `:white_check_mark:` when adding tests
  - :wrench: `:wrench:` when updating configuration
  - :recycle: `:recycle:` when refactoring code
  - :fire: `:fire:` when removing code or files
  - :lock: `:lock:` when dealing with security
  - :arrow_up: `:arrow_up:` when upgrading dependencies
  - :arrow_down: `:arrow_down:` when downgrading dependencies

Testing
------

We use pytest_ for testing. To run the tests:

.. code-block:: bash

   # Run all tests
   pytest

   # Run tests with coverage
   pytest --cov=fileorganizer

   # Run a specific test file
   pytest tests/test_something.py -v

   # Run a specific test function
   pytest tests/test_something.py::test_function_name -v

.. _pytest: https://docs.pytest.org/

Documentation
------------

We use Sphinx_ for documentation. To build the documentation:

.. code-block:: bash

   # Install documentation dependencies
   pip install -e .[docs]

   # Build the documentation
   cd docs
   make html

   # Open the documentation in your browser
   open _build/html/index.html

.. _Sphinx: https://www.sphinx-doc.org/

Code Review Process
------------------

1. Create a pull request (PR) with your changes
2. Ensure all CI checks pass
3. A maintainer will review your PR and provide feedback
4. Address any feedback and update your PR
5. Once approved, a maintainer will merge your PR

Code of Conduct
--------------

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. See :doc:`code_of_conduct` for more information.

License
------
By contributing to FileOrganizer, you agree that your contributions will be licensed under the MIT License.
