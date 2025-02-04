# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-02-04

### Added
- Core functionality for multi-environment Python tool runner
- PyPI publishing via GitHub Actions with OIDC authentication

### Changed
- Enhanced CI workflow with type checking and test result reporting
- Updated GitHub Actions workflow commands for Hatch scripts
- Updated GitHub Actions workflow permissions for release management
- Fixed package structure and installation issues
- Updated pre-commit hook configuration

### Removed
- Integration test job from GitHub Actions workflow

## [0.1.1] - 2025-02-04

### Changed
- Initial package release on PyPI
- Fixed package metadata and dependencies

## [0.1.0] - 2025-02-04

### Added
- Initial project structure for pipenv-tools-hook
- Development environments and tooling configuration
- pytest and pytest-cov dependencies for testing

[0.1.3]: https://github.com/macieyng/pipenv-tools-hook/compare/v0.1.1...v0.1.3
[0.1.1]: https://github.com/macieyng/pipenv-tools-hook/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/macieyng/pipenv-tools-hook/releases/tag/v0.1.0
