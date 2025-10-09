# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-01-09

### Fixed - Major Code Review Issues

#### Issue 1: Removed Unused async_crew.py
- **Problem**: `async_crew.py` file existed but was never imported or used anywhere
- **Impact**: Dead code causing confusion about execution flow
- **Solution**: Completely removed the file
- **Benefit**: Cleaner codebase, no confusion about async execution

#### Issue 2: Simplified main.py Entry Point
- **Problem**: `main.py` contained 154 lines with utility functions mixed in
- **Impact**: Unclear execution flow, poor separation of concerns
- **Solution**: 
  - Created `utils/output_handler.py` module
  - Moved `save_complete_output()` function to output_handler
  - Moved `extract_and_save_components()` function to output_handler
  - Added `process_and_save_results()` convenience function
  - Reduced `main.py` to 64 lines focused on orchestration only
- **Benefit**: 
  - Clear entry point
  - Reusable utility functions
  - Better testability
  - Improved maintainability

### Added

- `utils/output_handler.py` - New module for output processing utilities
- `utils/__init__.py` - Package initialization with exports
- Comprehensive documentation in README.md
- CHANGELOG.md to track changes
- Clean architecture with proper separation of concerns

### Changed

- `main.py` - Simplified from 154 lines to 64 lines
- Project structure - Better organization of utility functions
- Documentation - Updated to reflect new architecture

### Removed

- `async_crew.py` - Unused file removed completely

## [1.0.0] - 2025-01-08

### Initial Release

- 4 specialized AI agents
- 8+ custom tools
- Multi-agent orchestration with CrewAI
- API discovery and documentation
- Security compliance checking
- SDK generation

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes
