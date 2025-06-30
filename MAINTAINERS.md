# Maintainer's Guide

This document provides information for maintainers of the FileOrganizer project.

## Project Structure

```
fileorganizer/
├── fileorganizer/      # Main package source code
├── tests/              # Test suite
├── docs/               # Documentation
├── .github/            # GitHub configuration
└── ...                 # Project configuration files
```

## Branch Strategy

- `main`: Stable, production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

## Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer) for version numbers:

- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality in a backward-compatible manner
- **PATCH** version for backward-compatible bug fixes

## Release Process

### 1. Prepare the Release

1. Create a release branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/vX.Y.Z
   ```

2. Update version numbers:
   - Update `fileorganizer/__init__.py`
   - Update `CHANGELOG.md` with release notes
   - Update documentation if needed

3. Commit the changes:
   ```bash
   git add .
   git commit -m "chore: prepare release vX.Y.Z"
   ```

### 2. Create the Release

1. Merge the release branch into `main`:
   ```bash
   git checkout main
   git merge --no-ff release/vX.Y.Z
   git tag -a vX.Y.Z -m "Version X.Y.Z"
   git push origin main --tags
   ```

2. Merge back into `develop`:
   ```bash
   git checkout develop
   git merge --no-ff release/vX.Y.Z
   git push origin develop
   ```

3. Delete the release branch:
   ```bash
   git branch -d release/vX.Y.Z
   git push origin --delete release/vX.Y.Z
   ```

### 3. Publish to PyPI

1. Build the distribution packages:
   ```bash
   pip install --upgrade build twine
   python -m build
   ```

2. Upload to PyPI Test (verify first):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Dependency Management

1. Add new dependencies to `setup.py` under `install_requires`
2. Update `requirements.txt` with `pip freeze > requirements.txt`
3. Document any new dependencies in the appropriate documentation

## Code Review Guidelines

1. Ensure all tests pass
2. Verify code style and type hints
3. Check for proper documentation
4. Ensure backward compatibility or document breaking changes
5. Review security implications

## Security Issues

1. Report security issues to security@example.com
2. Include detailed reproduction steps
3. Allow reasonable time for a fix before disclosure
4. Follow responsible disclosure practices

## Deprecation Policy

1. Mark deprecated features with `@deprecated` decorator
2. Include deprecation notice in docstring
3. Document the recommended alternative
4. Remove deprecated features after 2 major versions

## Backward Compatibility

1. Maintain backward compatibility within major versions
2. Use deprecation warnings for breaking changes
3. Document all breaking changes in the changelog
4. Provide upgrade guides for major version changes

## Performance Considerations

1. Profile performance-critical code
2. Document performance characteristics
3. Consider memory usage for large datasets
4. Optimize for the common case

## Documentation Updates

1. Update all relevant documentation for changes
2. Ensure docstrings are up to date
3. Add examples for new features
4. Update the changelog

## Issue Triage

1. Label issues appropriately
2. Prioritize based on impact and severity
3. Reference related issues and PRs
4. Close issues when resolved

## Community Management

1. Be welcoming to new contributors
2. Provide constructive feedback
3. Recognize contributions
4. Enforce the code of conduct

## Emergency Procedures

### Security Vulnerability

1. Acknowledge receipt of the report
2. Work on a fix in a private repository
3. Prepare a security release
4. Notify users about the vulnerability and update

### Broken Release

1. Immediately tag a new version if possible
2. Revert the broken release if needed
3. Communicate the issue to users
4. Document the incident and resolution
