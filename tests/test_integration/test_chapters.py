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

"""Integration tests for converting full C++ standard chapters"""

import re
import tempfile
from pathlib import Path

import pytest

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration

# Fixtures draft_repo and converter are provided by conftest.py (session scope)
# to prevent race conditions when running tests in parallel


class TestChapterConversion:
    """Test conversion of full chapters from the C++ standard"""

    def test_intro_chapter(self, converter, draft_repo):
        """Test converting intro.tex chapter"""
        source_file = draft_repo.source_dir / "intro.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            # Convert
            converter.convert_file(source_file, output_file, standalone=True)

            # Verify output file exists and has content
            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 1000, "Output file too small"

            # Verify section headings converted (with visible stable names)
            assert re.search(
                r'^# Scope <a id="intro\.scope">\[\[intro\.scope\]\]</a>$', content, re.MULTILINE
            ), "Missing expected heading with anchor"
            assert re.search(r"^## ", content, re.MULTILINE), "No level 2 headings found"
            # Verify HTML anchors are present with visible stable names
            assert (
                '<a id="intro.scope">[[intro.scope]]</a>' in content
            ), "Missing HTML anchor with visible stable name for intro.scope"

            # Verify no unconverted macros
            assert "\\Cpp{}" not in content, "Unconverted \\Cpp{} macro found"
            assert "\\tcode{" not in content, "Unconverted \\tcode{} macro found"
            assert "\\keyword{" not in content, "Unconverted \\keyword{} macro found"

            # Verify definitions are converted correctly (intro.defs section)
            definition_count = len(re.findall(r"^#### \d+\s+\w", content, re.MULTILINE))
            assert definition_count == 68, f"Expected 68 definitions, found {definition_count}"

            # Verify specific definitions
            assert "#### 1 access" in content, "Missing definition 1 (access)"
            assert (
                "#### 27 implementation-defined strict total order over pointers" in content
            ), "Missing definition 27"
            assert "#### 68 well-formed program" in content, "Missing definition 68"

            # Verify definition context labels
            assert (
                "⟨execution-time action⟩" in content
            ), "Missing context label for 'access' definition"
            assert "⟨library⟩" in content, "Missing library context labels"

            # Verify definition anchors
            assert (
                '<a id="defns.access">[defns.access]</a>' in content
            ), "Missing anchor for 'access' definition"

            # Verify no unconverted definition macros
            assert "\\definition{" not in content, "Unconverted \\definition{} macro found"
            assert "\\defncontext{" not in content, "Unconverted \\defncontext{} macro found"
            assert "\\begin{defnote}" not in content, "Unconverted \\begin{defnote} found"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_basic_chapter(self, converter, draft_repo):
        """Test converting basic.tex chapter"""
        source_file = draft_repo.source_dir / "basic.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)

            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 5000, "Output file too small"

            # Check for code blocks
            code_block_count = content.count("``` cpp")
            assert code_block_count > 10, f"Too few code blocks found: {code_block_count}"

            # Verify headings
            assert re.search(r"^# ", content, re.MULTILINE), "No level 1 headings"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_expressions_chapter(self, converter, draft_repo):
        """Test converting expressions.tex chapter (contains many code blocks)"""
        source_file = draft_repo.source_dir / "expressions.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)

            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 10000, "Output file too small"

            # Expressions chapter in n4950 has ~90 code blocks
            code_block_count = content.count("``` cpp")
            assert code_block_count >= 85, f"Too few code blocks: {code_block_count} (expected ≥85)"

            # Verify inline code
            inline_code_count = len(re.findall(r"`[^`]+`", content))
            assert inline_code_count > 100, "Too few inline code elements"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_classes_chapter(self, converter, draft_repo):
        """Test converting classes.tex chapter"""
        source_file = draft_repo.source_dir / "classes.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)

            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 10000, "Output file too small"

            # Classes chapter in n4950 has ~137 code blocks
            code_block_count = content.count("``` cpp")
            assert code_block_count >= 130, f"Too few code blocks: {code_block_count}"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_grammar_chapter(self, converter, draft_repo):
        """Test converting grammar.tex chapter (contains grammar blocks)"""
        source_file = draft_repo.source_dir / "grammar.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)

            assert output_file.exists()
            content = output_file.read_text()
            # Grammar chapter is small (summary of grammar, not full grammar)
            assert len(content) > 500, "Output file too small"

            # Grammar chapter in n4950 has 6 BNF code blocks
            bnf_block_count = content.count("``` bnf")
            assert bnf_block_count >= 5, f"Too few BNF blocks: {bnf_block_count}"

        finally:
            if output_file.exists():
                output_file.unlink()


class TestQualityChecks:
    """Test output quality metrics"""

    def test_no_empty_output(self, converter, draft_repo):
        """Verify all core chapters produce non-empty output"""
        chapters = ["intro.tex", "lex.tex", "basic.tex", "expressions.tex"]

        for chapter_name in chapters:
            source_file = draft_repo.source_dir / chapter_name
            if not source_file.exists():
                continue

            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
                output_file = Path(tmp.name)

            try:
                converter.convert_file(source_file, output_file, standalone=True)
                content = output_file.read_text()

                # Minimum size check (1KB)
                assert (
                    len(content) >= 1024
                ), f"{chapter_name} output too small: {len(content)} bytes"

            finally:
                if output_file.exists():
                    output_file.unlink()

    def test_macro_expansion(self, converter, draft_repo):
        """Verify common macros are expanded"""
        source_file = draft_repo.source_dir / "intro.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)
            content = output_file.read_text()

            # Check that common macros don't appear unexpanded
            problematic_patterns = [
                r"\\Cpp\{\}",
                r"\\tcode\{[^}]+\}(?!`)",  # \tcode not followed by backtick
                r"\\keyword\{[^}]+\}",
                r"\\rSec\d",
            ]

            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                # Allow small number of edge cases (< 5)
                assert len(matches) < 5, f"Too many unconverted {pattern}: {len(matches)}"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_time_chapter_table_parsing(self, converter, draft_repo):
        """Test time.tex chapter - regression test for issue #77 (malformed %z table rows)"""
        source_file = draft_repo.source_dir / "time.tex"
        if not source_file.exists():
            pytest.skip(f"Source file not found: {source_file}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            converter.convert_file(source_file, output_file, standalone=True)
            content = output_file.read_text()

            # Verify basic conversion
            assert len(content) > 10000, "time.md output too small"

            # Regression test for issue #77: Check that %z table rows are correctly formed
            # Before fix: rows were malformed with missing specifier column
            # After fix: rows should have 2 columns with %z in first column

            # Find table rows containing "offset" (both %z rows mention "offset from UTC")
            # These should be proper 2-column rows, not single-column malformed rows
            lines = content.split('\n')

            # Look for rows that mention "offset from UTC" - these are the %z rows
            offset_rows = [line for line in lines if 'offset from UTC' in line and line.startswith('|')]

            # Should find at least 2 %z rows (formatting and parsing tables)
            assert len(offset_rows) >= 2, f"Expected at least 2 table rows with 'offset from UTC', found {len(offset_rows)}"

            for row in offset_rows:
                # Key test: The row should have %z as the first column
                # Correct format: | `%z` | Description... | or | `%z`      | Description... | (with alignment spaces)
                # Malformed format would be: | . If the offset... |

                # Strip to check structure (tables may have alignment spaces)
                row_stripped = '|'.join(part.strip() for part in row.split('|'))

                # First cell should contain %z
                assert row_stripped.startswith('| `%z` |') or row.startswith('| `%z`'), \
                    f"Row should contain `%z` in first column, got: {row[:80]}"

                # Verify it's not a malformed single-column row starting with ". "
                assert not row.strip().startswith('| .'), \
                    f"Row should not be malformed starting with '| .'"

            # Also verify that malformed single-column rows starting with ". If the offset" don't exist
            malformed_pattern = r'^\|\s*\.\s+(If the offset|The modified commands).*\|$'
            malformed_matches = re.findall(malformed_pattern, content, re.MULTILINE)
            assert len(malformed_matches) == 0, f"Found {len(malformed_matches)} malformed rows"

        finally:
            if output_file.exists():
                output_file.unlink()
