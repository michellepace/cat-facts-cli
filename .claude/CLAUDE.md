# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Use British spelling throughout.

## Project Purpose

A uv-based Python 3.14+ project template configured for test-driven development and code quality checks. Provides a ready-to-use structure for packages (`src/`), standalone scripts (`scripts/`), and Jupyter notebooks (`notebooks/`), with pre-commit hooks running Ruff, Pyright, and pytest on every commit.

## Tech Stack

- **Python 3.14+** with **uv** package manager
- **Ruff** — linting (all rules enabled) and formatting
- **Pyright** — type checking
- **pytest** — testing
- **pre-commit** — automated quality checks
- **ipykernel** / **nbdime** — Jupyter notebook support
- **pandas** / **plotly** — included as example data dependencies

## Project Structure

UV-based Python 3.14+ template with TDD workflow:

- `src/` — distributable packages
- `scripts/` — standalone utilities
- `notebooks/` — Jupyter notebooks
- `tests/` — mirrors `src/` structure

## UV Workflow (Strict)

For `uv` documentation, refer to <https://docs.astral.sh/uv/llms.txt>

- Use `uv run` — never activate venv
- Use `uv add` — never pip
- Use `pyproject.toml` — never requirements.txt

```bash
# Setup & Dependencies
uv sync                                    # Match packages to lockfile
uv add --dev <pkg>                         # Add dev dependency
uv tree                                    # Show installed dependencies
uv lock --upgrade-package <pkg>            # Update specific package
uv lock --upgrade && uv sync               # Update all packages and apply

# Development
uv run pre-commit run --all-files          # Quality checks
uv run pytest                              # All tests
uv run pytest -v tests/test_specific.py::test_function
uv run ruff check --fix                    # Lint and auto-fix
uv run ruff format                         # Format
```

## Code Design Principles: Elegant Simplicity over Over-Engineered

**TDD-Driven Design**: Write tests first - this naturally creates better architecture:

- **Pure functions preferred** - no side effects in business logic, easier to test
- **Clear module boundaries** - easier to test and understand
- **Single responsibility** - complex functions are hard to test

**Key Architecture Guidelines**:

- **Layer separation** - CLI → business logic → I/O
- **One module, one purpose** - Each `.py` file has a clear, focused role
- **Handle errors at boundaries** - Catch exceptions in CLI layer, not business logic
- **Type hints required** - All function signatures need type annotations
- **Descriptive naming** - Functions/variables should clearly indicate purpose and be consistent throughout

## TDD Implementation

- Use pytest's `tmp_path` fixture to avoid creating test files
- Avoid mocks as they introduce unnecessary complexity
- Test incrementally: One test should drive one behaviour
- Use focused test names that describe what's being tested

## Code Quality Standards

- **Ruff**: Linting (ALL rules enabled)
- **Pyright**: Type checking (see [pyproject.toml](../pyproject.toml))
- **Pre-commit**: Auto-runs on every commit
