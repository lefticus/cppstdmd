# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org>

"""Integration tests for CLI functionality"""

import subprocess
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def cli_command():
    """Return the CLI command to run"""
    return ["./venv/bin/python3", "./convert.py"]


@pytest.fixture(scope="module")
def draft_source_dir():
    """Ensure draft repo exists and return path to source directory"""
    from cpp_std_converter.repo_manager import DraftRepoManager

    repo_manager = DraftRepoManager()

    # Ensure repo exists
    if not repo_manager.exists():
        try:
            repo_manager.clone(shallow=False)
        except Exception as e:
            pytest.skip(f"Could not clone draft repository: {e}")

    # Checkout n4950 (C++23) for consistent state
    try:
        repo_manager.checkout("n4950")
    except Exception as e:
        pytest.skip(f"Could not checkout n4950: {e}")

    source_dir = repo_manager.source_dir
    if not source_dir.exists():
        pytest.skip(f"Source directory not found: {source_dir}")

    return source_dir


class TestCLIBasic:
    """Test basic CLI functionality"""

    def test_help_command(self, cli_command):
        """Test --help flag"""
        result = subprocess.run(
            cli_command + ["--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Convert C++ standard LaTeX files" in result.stdout
        assert "--git-ref" in result.stdout

    def test_single_file_to_stdout(self, cli_command, draft_source_dir):
        """Test converting single file to stdout"""
        input_file = draft_source_dir / "intro.tex"
        if not input_file.exists():
            pytest.skip(f"Input file not found: {input_file}")

        result = subprocess.run(
            cli_command + [str(input_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert len(result.stdout) > 1000
        assert "# Scope" in result.stdout

    def test_single_file_to_file(self, cli_command, draft_source_dir):
        """Test converting single file to output file"""
        input_file = draft_source_dir / "intro.tex"
        if not input_file.exists():
            pytest.skip(f"Input file not found: {input_file}")

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            result = subprocess.run(
                cli_command + [str(input_file), "-o", str(output_file)],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0
            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 1000
            assert "# Scope" in content

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_verbose_mode(self, cli_command, draft_source_dir):
        """Test verbose output"""
        input_file = draft_source_dir / "intro.tex"
        if not input_file.exists():
            pytest.skip(f"Input file not found: {input_file}")

        result = subprocess.run(
            cli_command + [str(input_file), "-v"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Verbose mode should print command
        assert "Running: pandoc" in result.stderr


class TestCLIGitIntegration:
    """Test CLI git integration features"""

    def test_list_tags(self, cli_command):
        """Test --list-tags option"""
        result = subprocess.run(
            cli_command + ["--list-tags"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Available C++ standard version tags:" in result.stderr
        assert "n4140" in result.stdout or "n4950" in result.stdout

    def test_git_ref_conversion(self, cli_command, draft_source_dir):
        """Test converting with specific git ref"""
        input_file = draft_source_dir / "intro.tex"
        if not input_file.exists():
            pytest.skip(f"Input file not found: {input_file}")

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            result = subprocess.run(
                cli_command
                + [str(input_file), "--git-ref", "n4140", "-o", str(output_file), "-v"],  # C++14
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0
            assert "Using draft version: n4140" in result.stderr
            assert output_file.exists()

            content = output_file.read_text()
            assert len(content) > 1000

        finally:
            if output_file.exists():
                output_file.unlink()


class TestCLIDirectory:
    """Test directory conversion"""

    def test_directory_conversion(self, cli_command, draft_source_dir):
        """Test converting entire directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            result = subprocess.run(
                cli_command + [str(draft_source_dir), "-o", str(output_dir)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
            )

            assert result.returncode == 0

            # Check that some files were created
            md_files = list(output_dir.glob("*.md"))
            assert len(md_files) > 5, f"Too few files converted: {len(md_files)}"

            # Verify specific expected files
            expected_files = ["intro.md", "basic.md", "expressions.md"]
            for expected in expected_files:
                expected_path = output_dir / expected
                if expected_path.exists():
                    content = expected_path.read_text()
                    assert len(content) > 1000, f"{expected} too small"


class TestCLIErrorHandling:
    """Test error handling"""

    def test_missing_input_file(self, cli_command):
        """Test error when input file doesn't exist"""
        result = subprocess.run(
            cli_command + ["/nonexistent/file.tex"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_directory_without_output(self, cli_command, draft_source_dir):
        """Test error when converting directory without -o option"""
        result = subprocess.run(
            cli_command + [str(draft_source_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "output required" in result.stderr.lower()

    def test_invalid_git_ref(self, cli_command, draft_source_dir):
        """Test error with invalid git ref"""
        input_file = draft_source_dir / "intro.tex"
        if not input_file.exists():
            pytest.skip(f"Input file not found: {input_file}")

        result = subprocess.run(
            cli_command
            + [
                str(input_file),
                "--git-ref",
                "nonexistent-tag-12345",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "Repository error" in result.stderr or "error" in result.stderr.lower()
