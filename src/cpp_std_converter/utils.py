"""Shared utility functions for the C++ standard converter.

This module provides common utilities for subprocess execution, file operations,
and temporary file management to reduce code duplication across the codebase.
"""

import contextlib
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class CommandError(Exception):
    """Raised when a subprocess command fails."""

    pass


def run_command(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    timeout: float | None = None,
    capture_output: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess:
    """Run a subprocess command with consistent error handling.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        check: If True, raise CommandError on non-zero exit
        timeout: Optional timeout in seconds
        capture_output: If True, capture stdout/stderr
        text: If True, decode output as text

    Returns:
        CompletedProcess instance with stdout, stderr, returncode

    Raises:
        CommandError: If check=True and command fails
        subprocess.TimeoutExpired: If timeout is exceeded
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=text,
            check=check,
            timeout=timeout,
        )
        return result
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(str(arg) for arg in cmd)
        error_msg = f"Command failed: {cmd_str}"
        if e.stderr:
            error_msg += f"\n{e.stderr}"
        raise CommandError(error_msg) from e


def run_command_silent(
    cmd: list[str],
    cwd: Path | None = None,
    timeout: float | None = None,
) -> tuple[bool, str, str]:
    """Run a command without raising exceptions, return success status and output.

    Useful when you want to handle errors manually without exceptions.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        timeout: Optional timeout in seconds

    Returns:
        Tuple of (success: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", f"Command timed out after {timeout}s")
    except Exception as e:
        return (False, "", str(e))


@contextlib.contextmanager
def temp_tex_file(content: str):
    """Create a temporary .tex file with the given content.

    This context manager creates a temporary LaTeX file, yields its path,
    and ensures cleanup even if an exception occurs.

    Args:
        content: LaTeX content to write to the file

    Yields:
        Path: Path to the temporary .tex file

    Example:
        with temp_tex_file(latex_content) as tex_path:
            result = pandoc_convert(tex_path)
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8")
    try:
        tmp.write(content)
        tmp.close()
        tmp_path = Path(tmp.name)
        yield tmp_path
    finally:
        tmp_path = Path(tmp.name)
        with contextlib.suppress(FileNotFoundError):
            tmp_path.unlink()


@contextlib.contextmanager
def temp_file(content: str, suffix: str = ".txt", encoding: str = "utf-8"):
    """Create a temporary file with the given content.

    More generic version of temp_tex_file for any file type.

    Args:
        content: Content to write to the file
        suffix: File suffix (e.g., '.txt', '.md')
        encoding: Text encoding to use

    Yields:
        Path: Path to the temporary file
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding=encoding)
    try:
        tmp.write(content)
        tmp.close()
        tmp_path = Path(tmp.name)
        yield tmp_path
    finally:
        tmp_path = Path(tmp.name)
        with contextlib.suppress(FileNotFoundError):
            tmp_path.unlink()


def create_temp_tex_file(content: str) -> Path:
    """Create a temporary .tex file with the given content.

    Unlike temp_tex_file() context manager, this function returns the path
    and leaves cleanup to the caller. Useful when temp file needs to persist
    beyond the creation scope.

    Args:
        content: Content to write to the file

    Returns:
        Path to the created temporary file

    Example:
        temp_path = create_temp_tex_file(latex_content)
        # Use temp_path...
        temp_path.unlink()  # Manual cleanup when done
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


def safe_read_file(path: Path, encoding: str = "utf-8", errors: str = "strict") -> str | None:
    """Read a file if it exists, return None if it doesn't.

    Args:
        path: Path to the file to read
        encoding: Text encoding to use
        errors: How to handle encoding errors ('strict', 'ignore', 'replace')

    Returns:
        File contents as string, or None if file doesn't exist

    Example:
        content = safe_read_file(Path("config.txt"))
        if content:
            process(content)
    """
    if not path.exists():
        return None
    try:
        return path.read_text(encoding=encoding, errors=errors)
    except OSError as e:
        logger.warning(f"Failed to read {path}: {e}")
        return None


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist.

    Args:
        path: Directory path to create

    Returns:
        The same path (for chaining)

    Example:
        output_file = ensure_dir(output_dir) / "result.md"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_unlink(path: Path, missing_ok: bool = True) -> None:
    """Delete a file, optionally ignoring if it doesn't exist.

    Args:
        path: Path to the file to delete
        missing_ok: If True, don't raise error if file doesn't exist
    """
    try:
        path.unlink(missing_ok=missing_ok)
    except OSError as e:
        if not missing_ok:
            raise
        logger.debug(f"Could not delete {path}: {e}")


def cleanup_temp_files(temp_files: list[Path]) -> None:
    """Clean up a list of temporary files, ignoring errors.

    Args:
        temp_files: List of temporary file paths to delete

    Example:
        temp_files = [Path("/tmp/file1.tex"), Path("/tmp/file2.tex")]
        cleanup_temp_files(temp_files)
    """
    for temp_file in temp_files:
        with contextlib.suppress(Exception):
            temp_file.unlink()


def expand_latex_inputs(content: str, base_dir: Path) -> str:
    """Expand \\input{} commands in LaTeX content.

    Recursively expands all \\input{filename} commands by replacing them
    with the content of the referenced .tex file.

    Args:
        content: LaTeX content containing \\input{} commands
        base_dir: Base directory to resolve relative file paths

    Returns:
        Content with all \\input{} commands expanded

    Example:
        content = r"\\input{intro}\\nSome text"
        expanded = expand_latex_inputs(content, Path("source/"))
    """
    import re

    def expand_input(match):
        filename = match.group(1)
        input_file = base_dir / f"{filename}.tex"

        if input_file.exists():
            return input_file.read_text(encoding="utf-8")
        else:
            # If file doesn't exist, keep the \input command
            return match.group(0)

    # Replace \input{filename} with file content
    # Handle both \input{filename} and \input {filename}
    return re.sub(r"\\input\s*\{([^}]+)\}", expand_input, content)
