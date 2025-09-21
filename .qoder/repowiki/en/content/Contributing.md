# Contributing

<cite>
**Referenced Files in This Document**   
- [pyproject.toml](file://pyproject.toml)
- [run_tests.py](file://run_tests.py)
- [CHANGELOG.md](file://CHANGELOG.md)
- [src/cli.py](file://src/cli.py)
- [src/installer.py](file://src/installer.py)
- [tests/test_basic.py](file://tests/test_basic.py)
- [tests/test_installer.py](file://tests/test_installer.py)
</cite>

## Table of Contents
1. [Development Setup](#development-setup)
2. [Code Contribution Guidelines](#code-contribution-guidelines)
3. [Testing Process](#testing-process)
4. [Adding Platform Integrations](#adding-platform-integrations)
5. [Documentation Improvements](#documentation-improvements)
6. [Release Process and Versioning](#release-process-and-versioning)
7. [Build System and Packaging](#build-system-and-packaging)
8. [Best Practices for Code Extensions](#best-practices-for-code-extensions)

## Development Setup

To contribute to Agent OS, you must first set up a proper Python development environment. The project requires Python 3.8 or higher, as specified in the `pyproject.toml` file. It is recommended to use a virtual environment to isolate dependencies.

Start by cloning the repository and navigating to the project root:

```bash
git clone https://github.com/fenghaitao/agent-os.git
cd agent-os
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the project dependencies using pip:

```bash
pip install -e .
```

This installs the core dependencies listed in `pyproject.toml`, including `click`, `requests`, `pyyaml`, and `rich`. For development purposes, install optional dependencies:

```bash
pip install -e .[dev]
```

This installs development tools such as `pytest`, `black`, `flake8`, and `mypy` for code formatting, linting, and type checking.

**Section sources**
- [pyproject.toml](file://pyproject.toml#L1-L121)
- [src/cli.py](file://src/cli.py#L1-L187)

## Code Contribution Guidelines

All contributions to Agent OS must follow a structured branch management workflow. Create a new feature or fix branch from the main branch:

```bash
git checkout -b feature/your-feature-name
```

Commit messages should follow conventional commit format: `<type>(scope): description`. Supported types include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, and `chore`. For example:

```bash
git commit -m "feat(cli): add --all-platforms flag to install command"
```

When submitting a pull request:
- Ensure all tests pass
- Include relevant test cases for new functionality
- Update documentation if applicable
- Reference any related issues using `#issue-number`
- Provide a clear description of changes and motivation

Pull requests must be reviewed and approved before merging. The main branch is protected and requires passing CI checks.

**Section sources**
- [CHANGELOG.md](file://CHANGELOG.md#L1-L300)
- [src/cli.py](file://src/cli.py#L1-L187)

## Testing Process

Agent OS includes a test suite located in the `tests/` directory. The suite contains unit and integration tests for core components such as the CLI and installer. To run all tests, execute the test runner script:

```bash
python run_tests.py
```

This script runs `test_basic.py` and `test_installer.py`, verifying package structure, file contents, import integrity, and installer functionality. Individual test files can be executed directly:

```bash
python tests/test_basic.py
python tests/test_installer.py
```

When writing new tests:
- Place test files in the `tests/` directory
- Name files with the prefix `test_` or suffix `_test.py`
- Use descriptive function names starting with `test_`
- Test one behavior per function
- Include assertions for expected outcomes

The test configuration is defined in `pyproject.toml` under `[tool.pytest.ini_options]`, specifying test paths, file patterns, and default options.

**Section sources**
- [run_tests.py](file://run_tests.py#L1-L36)
- [tests/test_basic.py](file://tests/test_basic.py#L1-L160)
- [tests/test_installer.py](file://tests/test_installer.py#L1-L118)

## Adding Platform Integrations

To add support for a new AI coding platform, create corresponding directories and templates under the project root. For example, to support a new platform "MyAgent", create:

```
myagent/commands/
myagent/agents/
```

Add command templates in the `commands/` directory using the platform's expected format (e.g., JSON, YAML, TOML). Update the `installer.py` class to include the new platform in the installation mappings:

```python
if self.platforms['myagent']:
    platform_mappings.extend([
        ('myagent/agents/', '.myagent/agents/'),
        ('myagent/commands/', '.myagent/commands/')
    ])
```

Register the platform in the CLI help text and status command output. Ensure the platform-specific files are included in the package data configuration in `pyproject.toml`:

```toml
[tool.setuptools.package-data]
src = [
    "myagent/**/*",
    # ... other entries
]
```

Update documentation to reflect the new integration.

**Section sources**
- [src/installer.py](file://src/installer.py#L1-L155)
- [pyproject.toml](file://pyproject.toml#L1-L121)

## Documentation Improvements

Documentation is maintained in Markdown format across various directories including `instructions/`, `standards/`, and platform-specific folders. When updating documentation:

- Use consistent heading hierarchy (H1 for main title, H2 for sections, etc.)
- Follow the existing style guide in `standards/code-style/python-style.md`
- Use clear, concise language
- Include relevant examples
- Maintain cross-references between related documents

For new features, create corresponding instruction files in `instructions/core/` or `instructions/meta/`. Update platform-specific prompts in `github-copilot/prompts/` or `qwen-code/commands/` as needed. Ensure all new documentation is linked from relevant parent documents.

**Section sources**
- [standards/code-style/python-style.md](file://standards/code-style/python-style.md)
- [instructions/core/](file://instructions/core/)
- [github-copilot/prompts/](file://github-copilot/prompts/)

## Release Process and Versioning

Agent OS follows Semantic Versioning (SemVer) 2.0.0 as documented in `CHANGELOG.md`. Version numbers follow the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

All notable changes are recorded in `CHANGELOG.md` using the Keep a Changelog format. Before releasing:
- Update the changelog with user-facing changes
- Increment the version number in `pyproject.toml`
- Verify all tests pass
- Ensure documentation reflects changes

Releases are tagged in Git with the version prefix `v`, e.g., `v1.5.0`. The changelog includes links to compare views between versions.

**Section sources**
- [CHANGELOG.md](file://CHANGELOG.md#L1-L300)
- [pyproject.toml](file://pyproject.toml#L1-L121)

## Build System and Packaging

Agent OS uses `setuptools` as its build backend, configured through `pyproject.toml`. The build system requires `setuptools>=45` and `wheel`. Key packaging configurations include:

- Project metadata (name, version, description, authors)
- Dependencies in the `dependencies` array
- Optional dependencies for development and testing
- Entry points for the CLI command `agent-os`
- Package data to include non-Python files

The `setup.py` file is not used; all configuration is in `pyproject.toml`. To build a distribution:

```bash
python -m build
```

This creates both source and wheel distributions in the `dist/` directory. The package is installable via pip and supports editable installs for development.

**Section sources**
- [pyproject.toml](file://pyproject.toml#L1-L121)
- [src/cli.py](file://src/cli.py#L1-L187)

## Best Practices for Code Extensions

When extending Agent OS functionality:
- Maintain backward compatibility
- Follow existing code style and patterns
- Write comprehensive tests
- Document public interfaces
- Use type hints consistently
- Minimize external dependencies

For new CLI commands, use the `click` framework consistently with existing commands. For installer modifications, preserve the progress display and error handling patterns. When adding new configuration options, consider their impact on existing installations.

Design extensions to be modular and reusable. Prefer composition over inheritance when possible. Use rich for user-facing output to maintain consistent formatting. Validate inputs and provide helpful error messages.

**Section sources**
- [src/cli.py](file://src/cli.py#L1-L187)
- [src/installer.py](file://src/installer.py#L1-L155)
- [pyproject.toml](file://pyproject.toml#L1-L121)