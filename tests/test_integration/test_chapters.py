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
            result = converter.convert_file(source_file, output_file, standalone=True)

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
            result = converter.convert_file(source_file, output_file, standalone=True)

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
            result = converter.convert_file(source_file, output_file, standalone=True)

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
            result = converter.convert_file(source_file, output_file, standalone=True)

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
            result = converter.convert_file(source_file, output_file, standalone=True)

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
                result = converter.convert_file(source_file, output_file, standalone=True)
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
            result = converter.convert_file(source_file, output_file, standalone=True)
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
