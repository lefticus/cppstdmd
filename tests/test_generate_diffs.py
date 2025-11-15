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

"""Tests for generate_diffs.py script."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path to import generate_diffs
sys.path.insert(0, str(Path(__file__).parent.parent))

import generate_diffs


class TestPureFunctions:
    """Test pure functions with no side effects."""

    def test_format_size_bytes(self):
        """Test byte formatting for small sizes."""
        assert generate_diffs.format_size(0) == "0.0 B"
        assert generate_diffs.format_size(500) == "500.0 B"
        assert generate_diffs.format_size(1023) == "1023.0 B"

    def test_format_size_kilobytes(self):
        """Test byte formatting for KB sizes."""
        assert generate_diffs.format_size(1024) == "1.0 KB"
        assert generate_diffs.format_size(2048) == "2.0 KB"
        assert generate_diffs.format_size(1536) == "1.5 KB"
        assert generate_diffs.format_size(1024 * 100) == "100.0 KB"

    def test_format_size_megabytes(self):
        """Test byte formatting for MB sizes."""
        assert generate_diffs.format_size(1024 * 1024) == "1.0 MB"
        assert generate_diffs.format_size(1024 * 1024 * 2) == "2.0 MB"
        assert generate_diffs.format_size(1024 * 1024 * 1.5) == "1.5 MB"

    def test_format_size_gigabytes(self):
        """Test byte formatting for GB sizes."""
        assert generate_diffs.format_size(1024 * 1024 * 1024) == "1.0 GB"
        assert generate_diffs.format_size(1024 * 1024 * 1024 * 2) == "2.0 GB"

    def test_generate_all_version_pairs(self):
        """Test generating all version pairs in order."""
        pairs = generate_diffs.generate_all_version_pairs()

        # Should generate 15 pairs total (6 choose 2)
        assert len(pairs) == 15

        # First pair should be n3337 -> n4140
        assert pairs[0] == ("n3337", "n4140")

        # Last pair should be n4950 -> trunk
        assert pairs[-1] == ("n4950", "trunk")

        # All pairs should be chronologically ordered
        version_order = ["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"]
        for from_v, to_v in pairs:
            from_idx = version_order.index(from_v)
            to_idx = version_order.index(to_v)
            assert from_idx < to_idx, f"Pair {from_v} -> {to_v} not in order"

    def test_generate_all_version_pairs_includes_all_combinations(self):
        """Test that all valid combinations are generated."""
        pairs = generate_diffs.generate_all_version_pairs()

        # Should include C++11 -> C++23
        assert ("n3337", "n4950") in pairs

        # Should include C++11 -> trunk
        assert ("n3337", "trunk") in pairs

        # Should include C++20 -> C++23
        assert ("n4861", "n4950") in pairs

        # Should NOT include reverse pairs
        assert ("n4950", "n3337") not in pairs
        assert ("trunk", "n4950") not in pairs


class TestFileIO:
    """Test functions that involve file I/O."""

    def test_get_file_stats_nonexistent(self):
        """Test getting stats for a file that doesn't exist."""
        result = generate_diffs.get_file_stats(Path("/nonexistent/file.md"))
        assert result == {"size": 0, "lines": 0}

    def test_get_file_stats_empty_file(self):
        """Test getting stats for an empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = Path(f.name)

        try:
            result = generate_diffs.get_file_stats(temp_path)
            assert result["size"] == 0
            assert result["lines"] == 0
        finally:
            temp_path.unlink()

    def test_get_file_stats_small_file(self):
        """Test getting stats for a small file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.get_file_stats(temp_path)
            assert result["lines"] == 3
            assert result["size"] > 0
            # Should be around 21 bytes (7 chars per line * 3 lines)
            assert 15 < result["size"] < 30
        finally:
            temp_path.unlink()

    def test_get_file_stats_unicode(self):
        """Test getting stats for a file with Unicode content."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("C++ standard λ\n")
            f.write("Template <typename T>\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.get_file_stats(temp_path)
            assert result["lines"] == 2
            assert result["size"] > 0
        finally:
            temp_path.unlink()


class TestParseStableNames:
    """Test stable name parsing from markdown files."""

    def test_parse_stable_names_empty_file(self):
        """Test parsing an empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = Path(f.name)

        try:
            result = generate_diffs.parse_stable_names(temp_path)
            assert result == {}
        finally:
            temp_path.unlink()

    def test_parse_stable_names_no_anchors(self):
        """Test parsing a file with no stable name anchors."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Some Heading\n")
            f.write("Some content\n")
            f.write("## Another Heading\n")
            f.write("More content\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.parse_stable_names(temp_path)
            assert result == {}
        finally:
            temp_path.unlink()

    def test_parse_stable_names_single_anchor(self):
        """Test parsing a file with one stable name anchor."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write('# Introduction <a id="intro">[[intro]]</a>\n')
            f.write("This is the introduction.\n")
            f.write("It has multiple lines.\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.parse_stable_names(temp_path)
            assert "intro" in result
            content, start, end = result["intro"]
            assert "This is the introduction" in content
            assert start == 1
            assert end == 3
        finally:
            temp_path.unlink()

    def test_parse_stable_names_multiple_anchors(self):
        """Test parsing a file with multiple stable name anchors."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write('# Introduction <a id="intro">[[intro]]</a>\n')
            f.write("Introduction content.\n")
            f.write("\n")
            f.write('## Scope <a id="intro.scope">[[intro.scope]]</a>\n')
            f.write("Scope content.\n")
            f.write("\n")
            f.write('# References <a id="refs">[[refs]]</a>\n')
            f.write("References content.\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.parse_stable_names(temp_path)
            assert len(result) == 3
            assert "intro" in result
            assert "intro.scope" in result
            assert "refs" in result

            # Check content extraction
            intro_content, _, _ = result["intro"]
            assert "Introduction content" in intro_content

            scope_content, _, _ = result["intro.scope"]
            assert "Scope content" in scope_content

            refs_content, _, _ = result["refs"]
            assert "References content" in refs_content
        finally:
            temp_path.unlink()

    def test_parse_stable_names_nested_hierarchy(self):
        """Test parsing with nested heading hierarchy."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write('# Algorithms <a id="alg">[[alg]]</a>\n')
            f.write("Algorithm chapter.\n")
            f.write("\n")
            f.write('## Copy <a id="alg.copy">[[alg.copy]]</a>\n')
            f.write("Copy algorithm.\n")
            f.write("\n")
            f.write('### std::copy <a id="alg.copy.std">[[alg.copy.std]]</a>\n')
            f.write("std::copy details.\n")
            f.write("\n")
            f.write('## Find <a id="alg.find">[[alg.find]]</a>\n')
            f.write("Find algorithm.\n")
            temp_path = Path(f.name)

        try:
            result = generate_diffs.parse_stable_names(temp_path)
            assert len(result) == 4
            assert "alg" in result
            assert "alg.copy" in result
            assert "alg.copy.std" in result
            assert "alg.find" in result
        finally:
            temp_path.unlink()


class TestFindCommonChapters:
    """Test finding common chapters between versions."""

    def test_find_common_chapters_with_temp_directories(self):
        """Test finding common chapters with temporary test directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create version directories
            from_dir = tmpdir / "n3337"
            to_dir = tmpdir / "n4950"
            from_dir.mkdir()
            to_dir.mkdir()

            # Create common files
            (from_dir / "intro.md").write_text("intro")
            (to_dir / "intro.md").write_text("intro")
            (from_dir / "class.md").write_text("class")
            (to_dir / "class.md").write_text("class")

            # Create removed file (only in from)
            (from_dir / "removed.md").write_text("removed")

            # Create added file (only in to)
            (to_dir / "added.md").write_text("added")

            # Mock the version directories
            with patch("generate_diffs.Path") as mock_path:
                # Configure mock to return our temp directories
                def path_side_effect(arg):
                    if arg == "n3337":
                        return from_dir
                    elif arg == "n4950":
                        return to_dir
                    return Path(arg)

                mock_path.side_effect = path_side_effect

                common, removed, added = generate_diffs.find_common_chapters("n3337", "n4950")

                assert "intro" in common
                assert "class" in common
                assert "removed" in removed
                assert "added" in added

    def test_find_common_chapters_nonexistent_from_dir(self):
        """Test error handling when from directory doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Version directory not found"):
            generate_diffs.find_common_chapters("nonexistent", "n4950")

    def test_find_common_chapters_nonexistent_to_dir(self):
        """Test error handling when to directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            from_dir = tmpdir / "n3337"
            from_dir.mkdir()

            with patch("generate_diffs.Path") as mock_path:

                def path_side_effect(arg):
                    if arg == "n3337":
                        return from_dir
                    return Path(arg)

                mock_path.side_effect = path_side_effect

                with pytest.raises(FileNotFoundError, match="Version directory not found"):
                    generate_diffs.find_common_chapters("n3337", "nonexistent")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
