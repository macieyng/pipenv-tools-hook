# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.7]

### Added
- Methods to check Pipenv environment status and tool installation
- Comprehensive test coverage for Pipenv environment detection
- Tests for tool installation checks and error handling scenarios

### Changed
- Improved tool execution logic for both inside and outside Pipenv environments
- Enhanced error messaging for missing tools in Pipenv environments
- Updated GitHub Actions workflow to support version updates on release
- Configured bumpver for automated version management
- Enhanced test coverage for file grouping and path resolution
- Improved argument parsing tests for main function
- Modified bumpver configuration for more precise version matching

### Fixed
- Bumpver integration in release workflow

## [0.1.7] - 2025-02-04

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

## [0.1.7] - 2025-02-04

### Changed
- Initial package release on PyPI
- Fixed package metadata and dependencies

## [0.1.7] - 2025-02-04

### Added
- Initial project structure for pipenv-tools-hook
- Development environments and tooling configuration
- pytest and pytest-cov dependencies for testing

[0.1.4]: https://github.com/macieyng/pipenv-tools-hook/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/macieyng/pipenv-tools-hook/compare/v0.1.1...v0.1.3
[0.1.1]: https://github.com/macieyng/pipenv-tools-hook/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/macieyng/pipenv-tools-hook/releases/tag/v0.1.0
