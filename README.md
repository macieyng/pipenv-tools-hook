# pipenv-tools-hook

A pre-commit hook for running Python tools (like ruff, mypy, etc.) in multiple Pipenv environments within a monorepo or multi-project repository structure.

## Overview

This tool solves the common problem of running Python code quality tools in repositories with multiple Python projects, each with its own Pipenv environment and tooling requirements. It automatically:

- Discovers Pipenv environments in your repository
- Groups files by their closest controlling Pipenv environment
- Runs specified tools (like ruff, mypy) using the appropriate Pipenv environment for each file

## Features

- 🔍 Automatic Pipenv environment discovery
- 🗂️ Smart file-to-environment mapping
- 🛠️ Support for any Pipenv-installed tool (ruff, mypy, pylint, etc.)
- 🔄 Seamless integration with pre-commit
- 📁 Works with monorepos and multi-project repositories

## Installation

```bash
pip install pipenv-tools-hook
```

## Usage

1. Add the hook to your `.pre-commit-config.yaml`:
```yaml
repo: https://github.com/yourusername/pipenv-tools-hook
rev: v0.1.0 # Use the latest version
hooks:
id: pipenv-tools
name: Run Python tools in Pipenv environments
args: ['--tool=ruff'] # Specify which tool to run
```

2. Ensure each project directory that needs code quality checks has:
   - A `Pipfile` with the required tools installed
   - Appropriate tool configuration files (e.g., `pyproject.toml`, `setup.cfg`)

Example repository structure:
```
my-monorepo/
├── .pre-commit-config.yaml
├── project1/
│ ├── Pipfile
│ ├── pyproject.toml
│ ├── src/
│ │ └── main.py
│ └── tests/
│ └── test_main.py
└── project2/
├── Pipfile
├── pyproject.toml
└── app.py
```

## Configuration

The hook accepts the following arguments:

- `--tool`: (Required) The Python tool to run (e.g., ruff, mypy, pylint)
- `--args`: (Optional) Additional arguments to pass to the tool

Example configurations:

```yaml
# Run ruff linter
- id: pipenv-tools
  args: ['--tool=ruff', '--args=--fix']
# Run mypy type checker
- id: pipenv-tools
  args: ['--tool=mypy', '--args=--strict']
# Run pylint
- id: pipenv-tools
  args: ['--tool=pylint']

```

## How It Works

1. When the hook runs, it:
   - Scans the repository for `Pipfile`s
   - Maps each Python file to its controlling Pipenv environment
   - Groups files by environment
2. For each environment:
   - Changes to the appropriate directory
   - Runs the specified tool using `pipenv run`
   - Reports any issues found

## Requirements

- Python ≥ 3.8
- pipenv ≥ 2023.0
- pre-commit ≥ 2.9.0

## Development

To set up the development environment:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pipenv-tools-hook.git
cd pipenv-tools-hook
```
2. Install development dependencies:
```bash
pip install hatch
```

3. Run tests:
```bash
hatch run test
```
4. Run type checking:
```bash
hatch run typecheck
```

5. Run linting:
```bash
hatch run lint
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please make sure your PR includes:
- A clear description of the changes
- Updates to documentation if needed
- New tests for new functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
