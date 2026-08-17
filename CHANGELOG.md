# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite under `tests/` covering both `builder.py` and `cli.py` (achieving 90% coverage).
- `pytest` and `pytest-cov` added as development dependencies.
- `ruff` added as a development dependency for fast linting and formatting.
- `ruff` configuration added to `pyproject.toml` (target-version py38, line length 88, ignoring E501).
- Generated and added an official project logo to the `README.md`.
- Expanded the `README.md` to thoroughly explain the project's core philosophy: "Instantly scaffold and write beautiful presentations for any project using a single shared Python library."
- Dedicated "References & Acknowledgements" section in the `README.md` to credit Marp, MarpX, and Jinja2.

### Changed
- Refactored `README.md` to detail specific "Features" and "Use Cases" (e.g., Automated Reporting, Standardized Workflows, Data Pipeline Integration).
- Formatted the codebase utilizing `ruff format .` and `ruff check . --fix`.

## [0.1.0] - Initial Release

### Added
- Core `marpx-builder` CLI application with `init`, `build`, and `watch` commands.
- Bundled canonical `MarpX` themes (`einstein`, `gödel`, `socrates`, `newton`, etc.).
- Integration with Jinja2 for dynamic, variable-driven slides.
- Support for HTML, PDF, and PPTX exports.
- Basic scaffold structure for new presentation projects (`marpx.yaml`, `presentation.md`, `custom.css`, `assets/`).
