"""A pre-commit hook for running Python tools in multiple Pipenv environments.

This module provides functionality to run Python tools (like ruff, mypy, etc.)
in multiple Pipenv environments within a monorepo or multi-project repository structure.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


@contextmanager
def chdir(path: Path) -> Generator[None, None, None]:
    """Context manager for changing directory."""
    current = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current)


class PipenvToolsHook:
    """A hook for running Python tools in multiple Pipenv environments.

    This class handles discovering Pipenv environments, grouping files by their
    controlling environment, and running specified tools within each environment.
    """

    def __init__(
        self: PipenvToolsHook,
        tool: str,
        tool_args: list[str] | None = None,
    ) -> None:
        """Initialize the hook.

        Args:
            tool: The Python tool to run (e.g., ruff, mypy)
            tool_args: Optional arguments to pass to the tool
        """
        self.tool = tool
        self.tool_args = tool_args or []
        self._pipfile_cache: dict[Path, Path] = {}
        self.root_dir = Path.cwd().resolve()

    def discover_pipfiles(self: PipenvToolsHook, start_dir: Path) -> dict[Path, Path]:
        """Scan directory tree and cache Pipfile locations.

        Args:
            start_dir: The directory to start scanning from

        Returns:
            A mapping of directory paths to their Pipfile paths
        """
        if not self._pipfile_cache:
            start_dir = Path(start_dir).resolve()
            for root, _, files in os.walk(start_dir):
                root_path = Path(root).resolve()
                if "Pipfile" in files:
                    self._pipfile_cache[root_path] = root_path / "Pipfile"

        return self._pipfile_cache

    def get_controlling_pipfile(
        self: PipenvToolsHook,
        file_path: Path,
    ) -> Path | None:
        """Find the nearest parent directory containing a Pipfile.

        Args:
            file_path: The path to the file to find the controlling Pipfile for

        Returns:
            The path to the directory containing the controlling Pipfile,
            or None if not found
        """
        current = Path(file_path).parent.resolve()
        root = self.root_dir.resolve()

        while current >= root:
            if current in self._pipfile_cache:
                return current
            current = current.parent

        return None

    def group_files_by_pipenv(
        self: PipenvToolsHook,
        files: list[str],
    ) -> dict[Path, set[Path]]:
        """Group files by their controlling Pipfile directory.

        Args:
            files: List of file paths to group

        Returns:
            A mapping of Pipfile directories to sets of file paths they control
        """
        grouped: dict[Path, set[Path]] = {}

        # Ensure we have discovered all Pipfiles
        self.discover_pipfiles(self.root_dir)

        for file in files:
            file_path = Path(file).resolve()
            if not file_path.is_absolute():
                file_path = (self.root_dir / file_path).resolve()

            pipfile_dir = self.get_controlling_pipfile(file_path)

            if pipfile_dir is None:
                sys.stderr.write(f"Warning: No Pipfile found for {file_path}\n")
                continue

            if pipfile_dir not in grouped:
                grouped[pipfile_dir] = set()

            grouped[pipfile_dir].add(file_path)

        return grouped

    def run_tool(self: PipenvToolsHook, files: list[str]) -> int:
        """Run the specified tool on grouped files.

        Args:
            files: List of file paths to run the tool on

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        grouped_files = self.group_files_by_pipenv(files)

        if not grouped_files:
            sys.stderr.write("No files to check!\n")
            # If no files were found to check, consider it a failure
            return 1

        exit_code = 0

        for pipfile_dir, file_group in grouped_files.items():
            with chdir(pipfile_dir):
                try:
                    # Convert paths to strings relative to the Pipfile directory
                    relative_paths = [
                        str(f.relative_to(pipfile_dir)) for f in file_group
                    ]

                    result = subprocess.run(
                        ["pipenv", "run", self.tool, *self.tool_args, *relative_paths],
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    # Print output
                    if result.stdout:
                        sys.stdout.write(result.stdout)
                    if result.stderr:
                        sys.stderr.write(result.stderr)

                    if result.returncode != 0:
                        exit_code = 1

                except subprocess.CalledProcessError as e:
                    sys.stderr.write(
                        f"Error running {self.tool} in {pipfile_dir}: {e}\n",
                    )
                    exit_code = 1
                except Exception as e:  # noqa: BLE001
                    sys.stderr.write(f"Unexpected error in {pipfile_dir}: {e}\n")
                    exit_code = 1

        return exit_code


def main() -> None:
    """Run the pre-commit hook."""
    parser = argparse.ArgumentParser(
        description="Run Python tools in multiple Pipenv environments",
    )
    parser.add_argument("--tool", required=True, help="Tool to run (e.g., ruff, mypy)")
    parser.add_argument(
        "--tool-args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the tool",
    )
    parser.add_argument("files", nargs="*", help="Files to check")

    args = parser.parse_args()

    # Split files from tool args if they were mixed
    tool_args = []
    files = []
    if args.tool_args:
        # Find the first argument that looks like a file path
        for i, arg in enumerate(args.tool_args):
            if not arg.startswith("-"):
                # Everything before this is a tool arg
                tool_args = args.tool_args[:i]
                # Everything from this point on is a file
                files = args.tool_args[i:] + args.files
                break
        else:
            # If no file-like arguments found in tool_args
            tool_args = args.tool_args
            files = args.files
    else:
        files = args.files

    hook = PipenvToolsHook(args.tool, tool_args)
    sys.exit(hook.run_tool(files))


if __name__ == "__main__":
    main()
