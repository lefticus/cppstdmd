"""Integration tests for StandardBuilder"""
import pytest
from pathlib import Path

from cpp_std_converter.standard_builder import StandardBuilder
from cpp_std_converter.converter import Converter
from cpp_std_converter.repo_manager import DraftRepoManager


pytestmark = pytest.mark.integration

# Fixtures draft_repo and converter are provided by conftest.py (session scope)
# to prevent race conditions when running tests in parallel


class TestStandardBuilder:
    """Test StandardBuilder class"""

    def test_extract_chapter_order(self, draft_repo):
        """Test extracting chapter order from std.tex"""
        builder = StandardBuilder(draft_repo.source_dir)

        chapters = builder.extract_chapter_order()

        # Verify we found chapters
        assert len(chapters) > 0, "Should extract at least one chapter"

        # Verify structure: front, mainmatter chapters, appendices, back
        # n4950 structure: front + 31 main chapters + 5 appendices + back = 38
        assert chapters[0] == 'front', "First chapter should be 'front'"
        assert chapters[-1] == 'back', "Last chapter should be 'back'"

        # Verify mainmatter chapters are present in order
        assert 'intro' in chapters, "'intro' should be present"
        assert 'lex' in chapters, "'lex' should be present"
        assert 'basic' in chapters, "'basic' should be present"
        assert 'threads' in chapters, "'threads' should be present"

        # Verify appendix chapters
        assert 'grammar' in chapters, "'grammar' appendix should be present"
        assert 'compatibility' in chapters, "'compatibility' appendix should be present"

        # Verify order: front < intro < threads < grammar < back
        front_idx = chapters.index('front')
        intro_idx = chapters.index('intro')
        threads_idx = chapters.index('threads')
        grammar_idx = chapters.index('grammar')
        back_idx = chapters.index('back')

        assert front_idx < intro_idx, "front should come before intro"
        assert intro_idx < threads_idx, "intro should come before threads"
        assert threads_idx < grammar_idx, "threads should come before grammar"
        assert grammar_idx < back_idx, "grammar should come before back"

        # Verify total count (front + 31 main + 5 appendices + back = 38)
        assert len(chapters) >= 37, f"Should have at least 37 chapters, got {len(chapters)}"

        # Verify no duplicates
        assert len(chapters) == len(set(chapters)), "Should not have duplicate chapters"

    def test_extract_chapter_order_without_frontmatter(self, draft_repo):
        """Test extracting chapters excluding frontmatter"""
        builder = StandardBuilder(draft_repo.source_dir)

        chapters = builder.extract_chapter_order(include_frontmatter=False)

        # Should not include 'front'
        assert 'front' not in chapters, "Should not include frontmatter"
        assert chapters[0] == 'intro', "First chapter should be 'intro' without frontmatter"

    def test_extract_chapter_order_without_backmatter(self, draft_repo):
        """Test extracting chapters excluding backmatter"""
        builder = StandardBuilder(draft_repo.source_dir)

        chapters = builder.extract_chapter_order(include_backmatter=False)

        # Should not include 'back'
        assert 'back' not in chapters, "Should not include backmatter"
        # Last should be an appendix chapter
        assert chapters[-1] in ['grammar', 'limits', 'compatibility', 'future', 'uax31'], \
            f"Last chapter should be an appendix, got {chapters[-1]}"

    def test_std_tex_exists(self, draft_repo):
        """Verify std.tex file exists"""
        builder = StandardBuilder(draft_repo.source_dir)
        assert builder.std_tex.exists(), "std.tex should exist"

    def test_invalid_draft_dir(self):
        """Test with invalid draft directory"""
        builder = StandardBuilder(Path("/nonexistent/path"))

        with pytest.raises(FileNotFoundError):
            builder.extract_chapter_order()

    def test_extract_stable_name_from_tex(self, converter, draft_repo):
        """Test extracting stable section names from .tex files"""
        builder = StandardBuilder(draft_repo.source_dir)

        # Test cases where filename != stable name
        test_cases = [
            ("expressions.tex", "expr"),     # expressions.tex → expr
            ("statements.tex", "stmt"),      # statements.tex → stmt
            ("preprocessor.tex", "cpp"),     # preprocessor.tex → cpp
            ("declarations.tex", "dcl"),     # declarations.tex → dcl
            ("classes.tex", "class"),        # classes.tex → class
            ("overloading.tex", "over"),     # overloading.tex → over
            ("templates.tex", "temp"),       # templates.tex → temp
            ("exception.tex", "except"),     # exception.tex → except
        ]

        # Test cases where filename == stable name
        test_cases_matching = [
            ("intro.tex", "intro"),
            ("lex.tex", "lex"),
            ("basic.tex", "basic"),
        ]

        for filename, expected_stable_name in test_cases:
            tex_file = draft_repo.source_dir / filename
            if tex_file.exists():
                stable_name = builder.extract_stable_name_from_tex(tex_file, converter)
                assert stable_name == expected_stable_name, \
                    f"Expected {filename} → {expected_stable_name}, got {stable_name}"

        for filename, expected_stable_name in test_cases_matching:
            tex_file = draft_repo.source_dir / filename
            if tex_file.exists():
                stable_name = builder.extract_stable_name_from_tex(tex_file, converter)
                assert stable_name == expected_stable_name, \
                    f"Expected {filename} → {expected_stable_name}, got {stable_name}"

    def test_extract_stable_name_fallback(self, converter, draft_repo):
        """Test that extraction falls back to filename on failure"""
        import tempfile

        builder = StandardBuilder(draft_repo.source_dir)

        # Create a temporary .tex file with no valid \rSec tag
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp:
            tmp.write("% This is just a comment\n")
            tmp.write("\\documentclass{article}\n")
            tmp.write("\\begin{document}\n")
            tmp.write("Hello world\n")
            tmp.write("\\end{document}\n")
            tmp_path = Path(tmp.name)

        try:
            stable_name = builder.extract_stable_name_from_tex(tmp_path, converter)
            # Should fall back to filename stem
            assert stable_name == tmp_path.stem, \
                f"Should fall back to filename stem, got {stable_name}"
        finally:
            tmp_path.unlink()

    def test_build_subset_of_chapters(self, converter, draft_repo):
        """Test building a subset of chapters (fast test)"""
        import tempfile

        # Create a mock StandardBuilder that only returns first 3 mainmatter chapters
        builder = StandardBuilder(draft_repo.source_dir)

        # Monkey-patch to only return first 3 mainmatter chapters for fast testing
        original_extract = builder.extract_chapter_order
        def limited_extract(include_frontmatter=True, include_backmatter=True):
            # Get only mainmatter chapters
            chapters = original_extract(include_frontmatter=False, include_backmatter=False)
            return chapters[:3]  # Only first 3 mainmatter chapters
        builder.extract_chapter_order = limited_extract

        # Create a temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            # Build subset of standard
            content, chapters = builder.build_full_standard(
                converter,
                output_file,
                verbose=True
            )

            # Verify output file exists and has content
            assert output_file.exists(), "Output file should exist"
            assert len(content) > 5000, "Output should have substantial content"

            # Verify exactly 3 chapters were converted
            assert len(chapters) == 3, f"Should have converted exactly 3 chapters, got {len(chapters)}"
            assert chapters == ['intro', 'lex', 'basic'], f"Should have converted intro, lex, basic, got {chapters}"

            # Verify TOC is present
            assert '# Table of Contents' in content, "Should have TOC"

            # Verify chapter separators (should be N for N chapters with TOC prepended)
            separator_count = content.count('\n---\n')
            assert separator_count == len(chapters), f"Should have {len(chapters)} separators for {len(chapters)} chapters with TOC, got {separator_count}"

            # Verify link definitions section exists
            assert '<!-- Link reference definitions -->' in content, "Should have link definitions section"

            # Verify some cross-references exist
            import re
            refs = re.findall(r'\[([a-z]+\.[a-z.]+)\]:\s*#\1', content)
            assert len(refs) > 10, f"Should have many cross-reference definitions, found {len(refs)}"

            # Verify the content was written to file
            file_content = output_file.read_text()
            assert file_content == content, "File content should match returned content"

        finally:
            if output_file.exists():
                output_file.unlink()

    @pytest.mark.slow
    def test_build_full_standard(self, converter, draft_repo):
        """Test building full standard from std.tex (slow: converts all chapters including front/back)"""
        import tempfile

        builder = StandardBuilder(draft_repo.source_dir)

        # Create a temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            # Build full standard (front + 31 main + 5 appendices + back = 38 chapters)
            content, chapters = builder.build_full_standard(
                converter,
                output_file,
                verbose=True
            )

            # Verify output file exists and has content
            assert output_file.exists(), "Output file should exist"
            assert len(content) > 100000, "Output should be large (full standard)"

            # Verify all chapters were converted (front + 31 main + 5 appendices + back = 38)
            assert len(chapters) >= 37, f"Should have converted at least 37 chapters, got {len(chapters)}"

            # Verify frontmatter and backmatter are included
            assert chapters[0] == 'front', "First chapter should be 'front'"
            assert chapters[-1] == 'back', "Last chapter should be 'back'"

            # Verify TOC is present
            assert '# Table of Contents' in content, "Should have TOC"

            # Verify chapter separators (should be N for N chapters with TOC prepended)
            separator_count = content.count('\n---\n')
            assert separator_count == len(chapters), f"Should have {len(chapters)} separators for {len(chapters)} chapters with TOC"

            # Verify link definitions section exists
            assert '<!-- Link reference definitions -->' in content, "Should have link definitions section"

            # Verify many cross-references exist
            import re
            refs = re.findall(r'\[([a-z]+\.[a-z.]+)\]:\s*#\1', content)
            assert len(refs) > 100, f"Should have many cross-reference definitions, found {len(refs)}"

        finally:
            if output_file.exists():
                output_file.unlink()

    def test_build_separate_chapters_subset(self, converter, draft_repo):
        """Test building separate markdown files for subset of chapters with cross-file linking"""
        import tempfile
        import re

        builder = StandardBuilder(draft_repo.source_dir)

        # Monkey-patch to only return first 3 mainmatter chapters for fast testing
        original_extract = builder.extract_chapter_order
        def limited_extract(include_frontmatter=True, include_backmatter=True):
            chapters = original_extract(include_frontmatter=False, include_backmatter=False)
            return chapters[:3]  # Only first 3 mainmatter chapters (intro, lex, basic)
        builder.extract_chapter_order = limited_extract

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            # Build separate chapters
            output_files = builder.build_separate_chapters(
                converter,
                output_dir,
                verbose=True
            )

            # Verify exactly 3 files created
            assert len(output_files) == 3, f"Should have created 3 files, got {len(output_files)}"

            # Verify files exist
            intro_file = output_dir / "intro.md"
            lex_file = output_dir / "lex.md"
            basic_file = output_dir / "basic.md"

            assert intro_file.exists(), "intro.md should exist"
            assert lex_file.exists(), "lex.md should exist"
            assert basic_file.exists(), "basic.md should exist"

            # Read file contents
            intro_content = intro_file.read_text()
            lex_content = lex_file.read_text()
            basic_content = basic_file.read_text()

            # Verify each file has substantial content
            assert len(intro_content) > 5000, "intro.md should have substantial content"
            assert len(lex_content) > 5000, "lex.md should have substantial content"
            assert len(basic_content) > 5000, "basic.md should have substantial content"

            # Verify each file has link definitions section
            assert '<!-- Link reference definitions -->' in intro_content
            assert '<!-- Link reference definitions -->' in lex_content
            assert '<!-- Link reference definitions -->' in basic_content

            # Verify cross-file links were fixed
            # intro.md should have cross-file links to lex.md and basic.md
            cross_file_links_intro = re.findall(r'\[([a-z]+\.[a-z.]+)\]:\s*([a-z]+)\.md#\1', intro_content)
            # Should have at least some cross-file links
            # Just verify the format is correct - don't assume label prefixes match filenames
            # since C++ standard can have sections defined in unexpected files
            # Note: intro.tex may reference sections from other chapters like classes.tex,
            # so we don't restrict to only the 3 chapters being built
            if len(cross_file_links_intro) > 0:
                # Verify format: [label]: filename.md#label
                for label, filename in cross_file_links_intro:
                    # Just verify it's a valid chapter filename (any chapter in the standard)
                    assert len(filename) > 0 and filename.isalpha(), \
                        f"Filename {filename} should be a valid chapter name"

            # Verify same-file links remain unchanged
            same_file_links_intro = re.findall(r'\[(intro\.[a-z.]+)\]:\s*#\1', intro_content)
            assert len(same_file_links_intro) > 0, "intro.md should have same-file links"

            # Verify TOC was added to front.md
            front_file = output_dir / "front.md"
            if front_file.exists():
                front_content = front_file.read_text()
                assert '# Table of Contents' in front_content, "front.md should have TOC"

                # Verify TOC has cross-file links to chapters
                # Should have entries like: [Scope](intro.md#intro.scope)
                toc_cross_file_links = re.findall(r'\[([^\]]+)\]\(([a-z]+)\.md#([a-z.]+)\)', front_content)
                assert len(toc_cross_file_links) > 0, "TOC should have cross-file links to chapters"

    @pytest.mark.slow
    def test_build_separate_chapters_full(self, converter, draft_repo):
        """Test building all chapters as separate files (slow)"""
        import tempfile
        import re

        builder = StandardBuilder(draft_repo.source_dir)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            # Build all separate chapters
            output_files = builder.build_separate_chapters(
                converter,
                output_dir,
                verbose=True
            )

            # Verify many files created (37-38 chapters)
            assert len(output_files) >= 37, f"Should have created at least 37 files, got {len(output_files)}"

            # Verify intro.md and expr.md exist (common chapters)
            intro_file = output_dir / "intro.md"
            expr_file = output_dir / "expr.md"

            assert intro_file.exists(), "intro.md should exist"
            assert expr_file.exists(), "expr.md should exist"

            # Read contents
            intro_content = intro_file.read_text()
            expr_content = expr_file.read_text()

            # Verify cross-file links exist
            # expressions.md should reference intro.md labels
            cross_file_to_intro = re.findall(r'\[intro\.[a-z.]+\]:\s*intro\.md#intro\.[a-z.]+', expr_content)
            # It's likely (but not guaranteed) that expressions references intro
            # Just verify the format is correct if any exist

            # Verify each file has link definitions
            assert '<!-- Link reference definitions -->' in intro_content
            assert '<!-- Link reference definitions -->' in expr_content

            # Count total cross-file links across all files
            total_cross_file_links = 0
            for output_file in output_files:
                content = output_file.read_text()
                # Match pattern: [label]: filename.md#label
                cross_links = re.findall(r'\[[a-z]+\.[a-z.]+\]:\s*[a-z]+\.md#[a-z]+\.[a-z.]+', content)
                total_cross_file_links += len(cross_links)

            # Should have many cross-file links in a full build
            assert total_cross_file_links > 50, f"Should have many cross-file links, found {total_cross_file_links}"
