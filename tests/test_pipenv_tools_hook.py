"""Tests for the pipenv-tools-hook package."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pipenv_tools_hook import PipenvToolsHook, chdir

# Constants for test values
TEST_TOOL = "ruff"
TEST_ARGS = ["--fix"]
TEST_FILES = ["file1.py", "file2.py"]
SUCCESS_CODE = 0
FAILURE_CODE = 1


@pytest.fixture
def test_env(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Create a test environment with Pipfiles and Python files."""
    # Create test directory structure
    project1_dir = tmp_path / "project1"
    project1_dir.mkdir()
    (project1_dir / "Pipfile").touch()
    (project1_dir / "src").mkdir()
    file1 = project1_dir / "src" / "file1.py"
    file1.touch()

    project2_dir = tmp_path / "project2"
    project2_dir.mkdir()
    (project2_dir / "Pipfile").touch()
    (project2_dir / "src").mkdir()
    file2 = project2_dir / "src" / "file2.py"
    file2.touch()

    return tmp_path, file1, file2


@pytest.fixture
def hook(test_env: tuple[Path, Path, Path]) -> PipenvToolsHook:
    """Create a PipenvToolsHook instance for testing."""
    tmp_path, _, _ = test_env
    hook = PipenvToolsHook(TEST_TOOL)
    hook.root_dir = tmp_path
    return hook


@pytest.fixture
def hook_with_args(test_env: tuple[Path, Path, Path]) -> PipenvToolsHook:
    """Create a PipenvToolsHook instance with tool arguments for testing."""
    tmp_path, _, _ = test_env
    hook = PipenvToolsHook(TEST_TOOL, TEST_ARGS)
    hook.root_dir = tmp_path
    return hook


def test_chdir() -> None:
    """Test the chdir context manager."""
    original_dir = Path.cwd()
    test_dir = original_dir.parent

    with chdir(test_dir):
        assert Path.cwd() == test_dir

    assert Path.cwd() == original_dir


def test_discover_pipfiles(
    hook: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test discovering Pipfiles in directory tree."""
    tmp_path, _, _ = test_env
    pipfiles = hook.discover_pipfiles(tmp_path)
    assert len(pipfiles) == 2


def test_get_controlling_pipfile(
    hook: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test finding the controlling Pipfile for a file."""
    tmp_path, file1, _ = test_env
    project1_dir = file1.parent.parent

    # Discover Pipfiles first
    hook.discover_pipfiles(tmp_path)

    # Test finding controlling Pipfile
    controlling_dir = hook.get_controlling_pipfile(file1)
    assert controlling_dir == project1_dir


def test_group_files_by_pipenv(
    hook: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test grouping files by their controlling Pipenv environment."""
    tmp_path, file1, file2 = test_env
    project1_dir = file1.parent.parent
    project2_dir = file2.parent.parent

    # Group files
    grouped = hook.group_files_by_pipenv([str(file1), str(file2)])
    assert len(grouped) == 2
    assert file1 in grouped[project1_dir]
    assert file2 in grouped[project2_dir]


def test_run_tool_success(
    hook: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test running tool with successful execution."""
    _, file1, file2 = test_env
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=SUCCESS_CODE,
            stdout="",
            stderr="",
        )
        result = hook.run_tool([str(file1), str(file2)])
        assert result == SUCCESS_CODE


def test_run_tool_failure(
    hook: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test running tool with failed execution."""
    _, file1, file2 = test_env
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=FAILURE_CODE,
            stdout="",
            stderr="Error message",
        )
        result = hook.run_tool([str(file1), str(file2)])
        assert result == FAILURE_CODE


def test_run_tool_with_args(
    hook_with_args: PipenvToolsHook, test_env: tuple[Path, Path, Path]
) -> None:
    """Test running tool with additional arguments."""
    _, file1, file2 = test_env
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=SUCCESS_CODE,
            stdout="",
            stderr="",
        )
        result = hook_with_args.run_tool([str(file1), str(file2)])
        assert result == SUCCESS_CODE
        # Verify tool args were passed correctly
        call_args = mock_run.call_args[0][0]
        assert TEST_ARGS[0] in call_args


def test_run_tool_no_files(hook: PipenvToolsHook) -> None:
    """Test running tool with no files."""
    result = hook.run_tool([])
    assert result == FAILURE_CODE


def test_main_argument_parsing() -> None:
    """Test command-line argument parsing in main function."""
    test_args = ["--tool", TEST_TOOL, "--tool-args", "--fix", "file1.py"]
    with patch.object(sys, "argv", ["script.py"] + test_args):
        with patch.object(PipenvToolsHook, "run_tool", return_value=SUCCESS_CODE):
            with pytest.raises(SystemExit) as exc_info:
                from pipenv_tools_hook import main

                main()
            assert exc_info.value.code == SUCCESS_CODE
